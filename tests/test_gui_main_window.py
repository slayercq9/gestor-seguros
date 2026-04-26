import os
import subprocess
import sys
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel, QPlainTextEdit

from app import __version__
from app.core.exceptions import WorkbookLoadError
from app.domain.workbook_records import WorkbookLoadResult, WorkbookLoadSummary
from app.ui.main_window import MainWindow


@contextmanager
def workspace_tempdir():
    base_dir = Path("data/output")
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"tmp-gui-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def build_result(structure_complete: bool = True) -> WorkbookLoadResult:
    missing = () if structure_complete else ("GS_MOTIVO_REVISION",)
    detected_columns = tuple(f"COL_{index}" for index in range(1, 50)) + ("GS_ES_DM",)
    summary = WorkbookLoadSummary(
        source_name="control_cartera_ficticio.xlsx",
        sheet_name="CONTROLCARTERA",
        header_row=1,
        total_rows=3,
        total_columns=12,
        data_rows_detected=2,
        records_loaded=2,
        rows_skipped=0,
        detected_columns=detected_columns,
        gs_columns_present=("GS_ES_DM",),
        gs_columns_missing=missing,
        structure_complete=structure_complete,
        warnings=("Carga de solo lectura; no se modifico ni guardo el workbook.",),
    )
    return WorkbookLoadResult(summary=summary, records=())


def test_ventana_principal_se_instancia_con_textos_base(qapp):
    window = MainWindow(loader=lambda path: build_result())

    assert window.windowTitle() == "Gestor de Seguros- Dagoberto Quirós Madriz"
    assert window.findChild(QLabel, "versionLabel").text() == "Versión 1.8.0"
    assert window.findChild(type(window.select_button), "selectWorkbookButton").text() == "Seleccionar Control Cartera"
    assert window.findChild(type(window.load_button), "loadWorkbookButton").text() == "Cargar Control Cartera"
    assert __version__ == "1.8.0"
    assert "seleccione un control cartera" in window.statusBar().currentMessage().lower()


def test_carga_simulada_muestra_resumen_sin_registros(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result())
        window.path_edit.setText(str(source))

        window.load_selected_workbook()

        assert window._summary_labels["archivo"].text() == "control_cartera_ficticio.xlsx"
        assert window._summary_labels["hoja"].text() == "CONTROLCARTERA"
        assert window._summary_labels["filas_cargadas"].text() == "2"
        assert "GS_ES_DM" in window._summary_texts["gs_presentes"].toPlainText()
        assert "COL_49" in window._summary_texts["columnas"].toPlainText()
        assert "Ana Segura" not in window.warnings_text.toPlainText()


def test_error_sin_archivo_se_muestra_amigablemente(qapp):
    window = MainWindow(loader=lambda path: build_result())

    window.load_selected_workbook()

    assert "Seleccione un archivo Control Cartera" in window.warnings_text.toPlainText()
    assert "No se pudo cargar el Control Cartera" in window.statusBar().currentMessage()


def test_error_por_extension_no_admitida_no_invoca_loader(qapp):
    called = {"value": False}

    def loader(path):
        called["value"] = True
        return build_result()

    window = MainWindow(loader=loader)
    window.path_edit.setText("control_cartera.txt")

    window.load_selected_workbook()

    assert called["value"] is False
    assert "Formato no admitido" in window.warnings_text.toPlainText()


def test_error_por_archivo_xlsx_inexistente_no_invoca_loader(qapp):
    called = {"value": False}

    def loader(path):
        called["value"] = True
        return build_result()

    window = MainWindow(loader=loader)
    window.path_edit.setText("control_cartera_inexistente.xlsx")

    window.load_selected_workbook()

    assert called["value"] is False
    assert "El archivo seleccionado no existe" in window.warnings_text.toPlainText()


def test_ruta_xlsx_existente_pasa_a_carga(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_valido.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        received = {"path": ""}

        def loader(path):
            received["path"] = str(path)
            return build_result()

        window = MainWindow(loader=loader)
        window.path_edit.setText(str(source))

        window.load_selected_workbook()

        assert received["path"] == str(source)
        assert "Control Cartera cargado correctamente" in window.statusBar().currentMessage()


def test_error_del_loader_no_rompe_la_ventana(qapp):
    def failing_loader(path):
        raise WorkbookLoadError("No existe la hoja requerida: CONTROLCARTERA")

    with workspace_tempdir() as temp_dir:
        source = temp_dir / "archivo.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=failing_loader)
        window.path_edit.setText(str(source))

        window.load_selected_workbook()

        assert "No fue posible cargar el Control Cartera" in window.warnings_text.toPlainText()
        assert "CONTROLCARTERA" in window.warnings_text.toPlainText()
        assert "No se pudo cargar el Control Cartera" in window.statusBar().currentMessage()


def test_estructura_incompleta_se_muestra_como_advertencia(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(structure_complete=False))
        window.path_edit.setText(str(source))

        window.load_selected_workbook()

        assert window._summary_labels["estructura"].text() == "No"
        assert "GS_MOTIVO_REVISION" in window._summary_texts["gs_faltantes"].toPlainText()


def test_areas_de_resumen_y_advertencias_soportan_texto_largo(qapp):
    window = MainWindow(loader=lambda path: build_result())

    assert window.findChild(type(window._summary_texts["columnas"]), "summary_columnas") is not None
    assert window.findChild(type(window.warnings_text), "warningsText") is not None
    assert window._summary_texts["columnas"].lineWrapMode() == QPlainTextEdit.LineWrapMode.WidgetWidth
    assert window.warnings_text.lineWrapMode() == QPlainTextEdit.LineWrapMode.WidgetWidth


def test_entrypoint_tecnico_secundario_sigue_ejecutable():
    completed = subprocess.run(
        [sys.executable, "-m", "app", "--check"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "gestor-seguros 1.8.0" in completed.stdout
