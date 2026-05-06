import os
import shutil
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPlainTextEdit, QPushButton, QTableView, QTabWidget

from app import __version__
from app.core.exceptions import WorkbookLoadError
from app.domain.workbook_records import WorkbookLoadResult, WorkbookLoadSummary, WorkbookRowRecord
from app.ui.main_window import APP_DISPLAY_NAME, MainWindow


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


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


def build_result() -> WorkbookLoadResult:
    columns = ("Columna A", "Columna B", "Vigencia")
    summary = WorkbookLoadSummary(
        source_name="control_cartera_ficticio.xlsx",
        sheet_name="CONTROLCARTERA",
        header_row=1,
        total_rows=5,
        total_columns=len(columns),
        useful_rows_detected=2,
        records_loaded=2,
        rows_skipped=2,
        detected_columns=columns,
        visible_columns=columns,
        read_only=True,
        warnings=("Carga de solo lectura; no se modifico ni guardo el Control Cartera.",),
    )
    records = (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={"Columna A": "Dato Ficticio Uno", "Columna B": "A-001", "Vigencia": "D.M."},
        ),
        WorkbookRowRecord(
            row_number=3,
            values_by_column={"Columna A": "Dato Ficticio Dos", "Columna B": "A-002", "Vigencia": "Anual"},
        ),
    )
    return WorkbookLoadResult(summary=summary, records=records)


def test_ventana_principal_se_instancia_con_textos_base(qapp):
    window = MainWindow(loader=lambda path: build_result(), default_path="data/input/CONTROLCARTERA_V2.xlsx", show_dialogs=False)
    tabs = window.findChild(QTabWidget, "mainTabs")

    assert window.windowTitle() == APP_DISPLAY_NAME
    assert "Dagoberto Quirós Madriz" in window.windowTitle()
    assert window.findChild(QLabel, "versionLabel").text() == "Versión 1.8.2"
    assert window.findChild(QPushButton, "selectWorkbookButton").text() == "Seleccionar Control Cartera"
    assert window.findChild(QPushButton, "loadDefaultControlButton").text() == "Cargar predeterminado"
    assert window.findChild(QPushButton, "loadWorkbookButton") is None
    assert __version__ == "1.8.2"
    assert "ruta predeterminada" in window.statusBar().currentMessage().lower()
    assert window.path_edit.text().endswith("CONTROLCARTERA_V2.xlsx")
    assert tabs is not None
    assert tabs.tabText(0) == "Registros"
    assert tabs.tabText(1) == "Resumen"
    assert window.findChild(QTableView, "recordsTable") is not None
    assert window.records_table.model().rowCount() == 0


def test_seleccionar_archivo_dispara_carga_automatica(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        received = {"path": ""}

        def loader(path):
            received["path"] = str(path)
            return build_result()

        monkeypatch.setattr(
            "app.ui.main_window.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(source), "Excel (*.xlsx)"),
        )
        window = MainWindow(loader=loader, default_path=source, show_dialogs=False)

        window.select_workbook()

        assert received["path"] == str(source)
        assert window.path_edit.text() == str(source)
        assert window._summary_labels["archivo"].text() == "control_cartera_ficticio.xlsx"
        assert window._summary_labels["hoja"].text() == "CONTROLCARTERA"
        assert window._summary_labels["filas_utiles"].text() == "2"
        assert window._summary_labels["filas_cargadas"].text() == "2"
        assert window._summary_labels["filas_omitidas"].text() == "2"
        assert window._summary_labels["columnas_visibles"].text() == "3"
        assert window._summary_labels["modo"].text() == "Solo lectura"
        assert window._summary_labels["estado"].text() == "Cargado correctamente"
        assert "GS_" not in window._summary_texts["columnas"].toPlainText()
        assert window.records_table.model().rowCount() == 2
        assert window.records_table.model().columnCount() == 3
        assert window.records_rows_label.text() == "Filas cargadas: 2"
        assert window.records_columns_label.text() == "Columnas visibles: 3"
        assert window.tabs.currentIndex() == 0
        assert "Control Cartera cargado correctamente" in window.statusBar().currentMessage()


def test_carga_control_cartera_predeterminado(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "CONTROLCARTERA_V2.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        received = {"path": ""}

        def loader(path):
            received["path"] = str(path)
            return build_result()

        window = MainWindow(loader=loader, default_path=source, show_dialogs=False)

        window.load_default_control_cartera()

        assert received["path"] == str(source)
        assert window.records_table.model().rowCount() == 2


def test_error_sin_archivo_muestra_mensaje_y_dialogo(qapp, monkeypatch):
    messages: list[str] = []
    monkeypatch.setattr(QMessageBox, "warning", lambda parent, title, message: messages.append(message))
    window = MainWindow(loader=lambda path: build_result(), default_path="data/input/CONTROLCARTERA_V2.xlsx", show_dialogs=True)
    window.path_edit.clear()

    window.load_selected_workbook()

    assert "Seleccione un archivo Control Cartera" in window.last_user_message
    assert "Seleccione un archivo Control Cartera" in messages[0]
    assert "No se pudo cargar el Control Cartera" in window.statusBar().currentMessage()
    assert window.records_table.model().rowCount() == 0


def test_error_por_extension_no_admitida_no_invoca_loader(qapp):
    called = {"value": False}

    def loader(path):
        called["value"] = True
        return build_result()

    window = MainWindow(loader=loader, default_path="data/input/CONTROLCARTERA_V2.xlsx", show_dialogs=False)
    window.path_edit.setText("control_cartera.txt")

    window.load_selected_workbook()

    assert called["value"] is False
    assert "Formato no admitido" in window.last_user_message


def test_error_por_archivo_xlsx_inexistente_no_invoca_loader(qapp):
    called = {"value": False}

    def loader(path):
        called["value"] = True
        return build_result()

    window = MainWindow(loader=loader, default_path="data/input/CONTROLCARTERA_V2.xlsx", show_dialogs=False)
    window.path_edit.setText("control_cartera_inexistente.xlsx")

    window.load_selected_workbook()

    assert called["value"] is False
    assert "El archivo seleccionado no existe" in window.last_user_message


def test_ruta_xlsx_existente_pasa_a_carga_con_enter(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_valido.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        received = {"path": ""}

        def loader(path):
            received["path"] = str(path)
            return build_result()

        window = MainWindow(loader=loader, default_path=source, show_dialogs=False)
        window.path_edit.setText(str(source))

        window.load_selected_workbook()

        assert received["path"] == str(source)
        assert "Control Cartera cargado correctamente" in window.statusBar().currentMessage()


def test_error_del_loader_no_expone_traza_tecnica(qapp):
    def failing_loader(path):
        raise WorkbookLoadError("No existe la hoja requerida: CONTROLCARTERA")

    with workspace_tempdir() as temp_dir:
        source = temp_dir / "archivo.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=failing_loader, default_path=source, show_dialogs=False)
        window.path_edit.setText(str(source))

        window.load_selected_workbook()

        assert "No fue posible cargar el Control Cartera" in window.last_user_message
        assert "CONTROLCARTERA" not in window.last_user_message
        assert "Traceback" not in window.last_user_message
        assert "No se pudo cargar el Control Cartera" in window.statusBar().currentMessage()
        assert window.records_table.model().rowCount() == 0


def test_cancelar_selector_no_muestra_mensaje_ni_limpia_datos(qapp, monkeypatch):
    messages: list[str] = []
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        monkeypatch.setattr(
            "app.ui.main_window.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: ("", ""),
        )
        monkeypatch.setattr(QMessageBox, "warning", lambda parent, title, message: messages.append(message))
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=True)

        window.load_selected_workbook()
        previous_path = window.path_edit.text()
        previous_message = window.last_user_message
        previous_status = window.statusBar().currentMessage()

        window.select_workbook()

        assert messages == []
        assert window.path_edit.text() == previous_path
        assert window.last_user_message == previous_message
        assert window.statusBar().currentMessage() == previous_status
        assert window.records_table.model().rowCount() == 2


def test_area_de_resumen_soporta_texto_largo_sin_panel_de_advertencias(qapp):
    window = MainWindow(loader=lambda path: build_result(), default_path="data/input/CONTROLCARTERA_V2.xlsx", show_dialogs=False)

    assert window.findChild(type(window._summary_texts["columnas"]), "summary_columnas") is not None
    assert window.findChild(QPlainTextEdit, "warningsText") is None
    assert window._summary_texts["columnas"].lineWrapMode() == QPlainTextEdit.LineWrapMode.WidgetWidth


def test_entrypoint_tecnico_secundario_sigue_ejecutable():
    completed = subprocess.run(
        [sys.executable, "-m", "app", "--check"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "gestor-seguros 1.8.2" in completed.stdout
