import os
import subprocess
import sys

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel

from app import __version__
from app.core.exceptions import WorkbookLoadError
from app.domain.workbook_records import WorkbookLoadResult, WorkbookLoadSummary
from app.ui.main_window import MainWindow


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def build_result(structure_complete: bool = True) -> WorkbookLoadResult:
    missing = () if structure_complete else ("GS_MOTIVO_REVISION",)
    summary = WorkbookLoadSummary(
        source_name="workbook_ficticio.xlsx",
        sheet_name="CONTROLCARTERA",
        header_row=1,
        total_rows=3,
        total_columns=12,
        data_rows_detected=2,
        records_loaded=2,
        rows_skipped=0,
        detected_columns=("COL_A", "COL_B", "GS_ES_DM"),
        gs_columns_present=("GS_ES_DM",),
        gs_columns_missing=missing,
        structure_complete=structure_complete,
        warnings=("Carga de solo lectura; no se modifico ni guardo el workbook.",),
    )
    return WorkbookLoadResult(summary=summary, records=())


def test_ventana_principal_se_instancia_con_textos_base(qapp):
    window = MainWindow(loader=lambda path: build_result())

    assert window.windowTitle() == "Gestor de Seguros"
    assert window.findChild(QLabel, "versionLabel").text() == "Versión 1.8.0"
    assert window.findChild(type(window.select_button), "selectWorkbookButton").text() == "Seleccionar workbook"
    assert window.findChild(type(window.load_button), "loadWorkbookButton").text() == "Cargar workbook"
    assert __version__ == "1.8.0"
    assert "seleccione un workbook" in window.statusBar().currentMessage().lower()


def test_carga_simulada_muestra_resumen_sin_registros(qapp):
    window = MainWindow(loader=lambda path: build_result())
    window.path_edit.setText("workbook_ficticio.xlsx")

    window.load_selected_workbook()

    assert window._summary_labels["archivo"].text() == "workbook_ficticio.xlsx"
    assert window._summary_labels["hoja"].text() == "CONTROLCARTERA"
    assert window._summary_labels["filas_cargadas"].text() == "2"
    assert "GS_ES_DM" in window._summary_labels["gs_presentes"].text()
    assert "Ana Segura" not in window.warnings_text.toPlainText()


def test_error_sin_archivo_se_muestra_amigablemente(qapp):
    window = MainWindow(loader=lambda path: build_result())

    window.load_selected_workbook()

    assert "Debe seleccionar" in window.warnings_text.toPlainText()
    assert "No se pudo cargar" in window.statusBar().currentMessage()


def test_error_del_loader_no_rompe_la_ventana(qapp):
    def failing_loader(path):
        raise WorkbookLoadError("No existe la hoja requerida: CONTROLCARTERA")

    window = MainWindow(loader=failing_loader)
    window.path_edit.setText("archivo.xlsx")

    window.load_selected_workbook()

    assert "CONTROLCARTERA" in window.warnings_text.toPlainText()
    assert "No se pudo cargar" in window.statusBar().currentMessage()


def test_estructura_incompleta_se_muestra_como_advertencia(qapp):
    window = MainWindow(loader=lambda path: build_result(structure_complete=False))
    window.path_edit.setText("workbook_ficticio.xlsx")

    window.load_selected_workbook()

    assert window._summary_labels["estructura"].text() == "No"
    assert "GS_MOTIVO_REVISION" in window._summary_labels["gs_faltantes"].text()


def test_entrypoint_tecnico_secundario_sigue_ejecutable():
    completed = subprocess.run(
        [sys.executable, "-m", "app", "--check"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "gestor-seguros 1.8.0" in completed.stdout
