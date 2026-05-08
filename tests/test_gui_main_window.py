import os
import shutil
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QHeaderView,
    QTableView,
    QTabWidget,
)

from app import __version__
from app.core.exceptions import WorkbookLoadError
from app.domain.workbook_records import WorkbookLoadResult, WorkbookLoadSummary, WorkbookRowRecord
from app.ui.assets import app_icon_path, load_app_icon
from app.ui.detail_dialog import RecordDetailDialog
from app.ui.edit_dialog import RecordEditDialog
from app.ui.main_window import APP_DISPLAY_NAME, MainWindow
from app.ui.theme import DARK_THEME, LIGHT_THEME, THEME_SETTING_KEY


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


def build_settings(path: Path) -> QSettings:
    settings = QSettings(str(path), QSettings.Format.IniFormat)
    settings.clear()
    return settings


def build_result() -> WorkbookLoadResult:
    detected_columns = ("Columna A", "Columna B", "Vigencia", "Cobertura A")
    visible_columns = ("Columna A", "Columna B", "Vigencia")
    summary = WorkbookLoadSummary(
        source_name="control_cartera_ficticio.xlsx",
        sheet_name="CONTROLCARTERA",
        header_row=1,
        total_rows=5,
        total_columns=len(detected_columns),
        useful_rows_detected=2,
        records_loaded=2,
        rows_skipped=2,
        detected_columns=detected_columns,
        visible_columns=visible_columns,
        read_only=True,
        warnings=("Carga de solo lectura; no se modifico ni guardo el Control Cartera.",),
    )
    records = (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={
                "Columna A": "Dato Ficticio Uno",
                "Columna B": "A-001",
                "Vigencia": "D.M.",
                "Cobertura A": "Cobertura Ficticia A",
            },
        ),
        WorkbookRowRecord(
            row_number=3,
            values_by_column={
                "Columna A": "Dato Ficticio Dos",
                "Columna B": "A-002",
                "Vigencia": "Anual",
                "Cobertura A": "Cobertura Ficticia B",
            },
        ),
    )
    return WorkbookLoadResult(summary=summary, records=records)


def build_result_with_wide_columns() -> WorkbookLoadResult:
    detected_columns = (
        "Nº Póliza",
        "Nombre del Asegurado",
        "Correo",
        "Tipo de Póliza",
        "Detalle",
        "Cobertura A",
    )
    visible_columns = (
        "Nº Póliza",
        "Nombre del Asegurado",
        "Correo",
        "Tipo de Póliza",
        "Detalle",
    )
    summary = WorkbookLoadSummary(
        source_name="control_cartera_ficticio.xlsx",
        sheet_name="CONTROLCARTERA",
        header_row=1,
        total_rows=2,
        total_columns=len(detected_columns),
        useful_rows_detected=1,
        records_loaded=1,
        rows_skipped=0,
        detected_columns=detected_columns,
        visible_columns=visible_columns,
        read_only=True,
        warnings=(),
    )
    records = (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={
                "Nº Póliza": "01-FICTICIA-0000000001",
                "Nombre del Asegurado": "Nombre Ficticio Largo Para Probar Autoajuste Visual",
                "Correo": "contacto.ficticio.largo@example.test",
                "Tipo de Póliza": "Tipo Ficticio Extenso",
                "Detalle": "Detalle ficticio amplio para validar tooltip y ancho visual de la tabla.",
                "Cobertura A": "Cobertura conservada solo en memoria",
            },
        ),
    )
    return WorkbookLoadResult(summary=summary, records=records)


def build_result_for_validation() -> WorkbookLoadResult:
    columns = ("Nº Póliza", "Nombre del Asegurado", "Vigencia", "DÍA", "MES", "AÑO", "Correo")
    summary = WorkbookLoadSummary(
        source_name="control_cartera_ficticio.xlsx",
        sheet_name="CONTROLCARTERA",
        header_row=1,
        total_rows=2,
        total_columns=len(columns),
        useful_rows_detected=1,
        records_loaded=1,
        rows_skipped=0,
        detected_columns=columns,
        visible_columns=columns,
        read_only=True,
        warnings=(),
    )
    records = (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={
                "Nº Póliza": "01-ABC",
                "Nombre del Asegurado": "Persona Ficticia",
                "Vigencia": "Anual",
                "DÍA": "29",
                "MES": "2",
                "AÑO": "2024",
                "Correo": "correo@example.test",
            },
        ),
    )
    return WorkbookLoadResult(summary=summary, records=records)


def test_ventana_principal_se_instancia_con_textos_base(qapp):
    with workspace_tempdir() as temp_dir:
        window = MainWindow(
            loader=lambda path: build_result(),
            default_path="data/input/CONTROLCARTERA_V2.xlsx",
            show_dialogs=False,
            settings=build_settings(temp_dir / "ui_settings.ini"),
        )
        tabs = window.findChild(QTabWidget, "mainTabs")

        assert window.windowTitle() == APP_DISPLAY_NAME
        assert "Dagoberto Quirós Madriz" in window.windowTitle()
        assert window.findChild(QLabel, "versionLabel").text() == "Versión 1.10.3"
        assert window.findChild(QPushButton, "selectWorkbookButton").text() == "Seleccionar Control Cartera"
        assert window.findChild(QPushButton, "loadDefaultControlButton").text() == "Cargar predeterminado"
        assert window.findChild(QPushButton, "themeToggleButton").toolTip() == "Cambiar tema"
        assert window.findChild(QPushButton, "themeToggleButton").text() == "🌙"
        assert window.findChild(QLineEdit, "recordsSearchText") is not None
        assert window.findChild(QComboBox, "recordsSearchColumn") is not None
        assert window.findChild(QPushButton, "clearSearchButton").text() == "Limpiar"
        assert window.findChild(QLabel, "searchResultsLabel").text() == "Mostrando 0 de 0 registros"
        assert window.findChild(QPushButton, "loadWorkbookButton") is None
        assert __version__ == "1.10.3"
        assert "ruta predeterminada" in window.statusBar().currentMessage().lower()
        assert window.path_edit.text().endswith("CONTROLCARTERA_V2.xlsx")
        assert tabs is not None
        assert tabs.tabText(0) == "Registros"
        assert tabs.tabText(1) == "Resumen"
        assert tabs.tabText(2) == "Bitácora"
        assert window.findChild(QTableView, "recordsTable") is not None
        assert window.findChild(QTableView, "auditTable") is not None
        assert window.findChild(QTableView, "recordDetailTable") is None
        assert window.findChild(QLabel, "pendingChangesLabel").text() == "Cambios pendientes: 0"
        assert window.findChild(QLabel, "auditCountLabel").text() == "Cambios registrados: 0"
        assert window.records_table.model().rowCount() == 0
        assert window.audit_table.model().rowCount() == 0
        assert not window.windowIcon().isNull()


def test_icono_de_aplicacion_existe_y_se_carga(qapp):
    icon_path = app_icon_path()

    assert icon_path.name == "app_icon.svg"
    assert icon_path.exists()
    assert not load_app_icon().isNull()


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
        assert "Cobertura A" not in window._summary_texts["columnas"].toPlainText()
        assert window._summary_labels["modo"].text() == "Solo lectura"
        assert window._summary_labels["estado"].text() == "Cargado correctamente"
        assert "GS_" not in window._summary_texts["columnas"].toPlainText()
        assert window.records_table.model().rowCount() == 2
        assert window.records_table.model().columnCount() == 3
        assert "Cobertura A" not in [
            window.records_table.model().headerData(index, Qt.Orientation.Horizontal)
            for index in range(window.records_table.model().columnCount())
        ]
        assert "Cobertura A" in window._records_model.record_at(0).values_by_column
        assert window.records_rows_label.text() == "Filas cargadas: 2"
        assert window.records_columns_label.text() == "Columnas visibles: 3"
        assert window.search_results_label.text() == "Mostrando 2 de 2 registros"
        assert window.search_column_combo.count() == 4
        assert window.search_column_combo.itemText(0) == "Todas las columnas"
        assert window.search_column_combo.itemText(1) == "Columna A"
        assert window.search_column_combo.findText("Cobertura A") == -1
        assert window.tabs.currentIndex() == 0
        assert "Control Cartera cargado correctamente" in window.statusBar().currentMessage()


def test_tabla_autoajusta_columnas_importantes_y_mantiene_resize_manual(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result_with_wide_columns(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()

        header = window.records_table.horizontalHeader()
        assert header.sectionResizeMode(0) == QHeaderView.ResizeMode.Interactive
        assert window.records_table.columnWidth(0) >= 140
        assert window.records_table.columnWidth(1) >= 220
        assert window.records_table.columnWidth(2) >= 200
        assert window.records_table.columnWidth(3) >= 150
        assert window.records_table.columnWidth(4) >= 200
        assert window.records_table.columnWidth(1) <= 320
        assert window.records_table.columnWidth(2) <= 320
        assert window.records_table.columnWidth(4) <= 360
        assert window.search_column_combo.findText("Cobertura A") == -1
        assert "Cobertura A" in window._records_model.record_at(0).values_by_column


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


def test_busqueda_general_filtra_resultados_y_limpia(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()
        window.search_edit.setText(" uno ")

        assert window.records_table.model().rowCount() == 1
        assert window.search_results_label.text() == "Mostrando 1 de 2 registros"

        window.search_edit.setText("SIN COINCIDENCIAS")

        assert window.records_table.model().rowCount() == 0
        assert window.search_results_label.text() == "Mostrando 0 de 2 registros"

        window.clear_search_button.click()

        assert window.search_edit.text() == ""
        assert window.records_table.model().rowCount() == 2
        assert window.search_results_label.text() == "Mostrando 2 de 2 registros"


def test_busqueda_por_columna_especifica(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()
        window.search_column_combo.setCurrentIndex(window.search_column_combo.findText("Vigencia"))
        window.search_edit.setText("anual")

        assert window.records_table.model().rowCount() == 1
        assert window.search_results_label.text() == "Mostrando 1 de 2 registros"

        window.search_edit.setText("A-001")

        assert window.records_table.model().rowCount() == 0
        assert window.search_results_label.text() == "Mostrando 0 de 2 registros"


def test_doble_clic_abre_detalle_del_registro(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        opened: list[RecordDetailDialog] = []

        def fake_exec(self):
            opened.append(self)
            return 0

        monkeypatch.setattr(RecordDetailDialog, "exec", fake_exec)
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()
        dialog = window.open_record_detail(window.records_table.model().index(0, 0))

        assert dialog is opened[0]
        assert dialog.windowTitle() == "Detalle del registro"
        assert dialog.detail_model.rowCount() == 3
        assert dialog.detail_model.data(dialog.detail_model.index(0, 0)) == "Columna A"
        assert dialog.detail_model.data(dialog.detail_model.index(0, 1)) == "Dato Ficticio Uno"


def test_dialogo_de_detalle_respeta_filtros_activos(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        opened: list[RecordDetailDialog] = []
        monkeypatch.setattr(RecordDetailDialog, "exec", lambda self: opened.append(self) or 0)
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()
        window.search_edit.setText("dos")
        dialog = window.open_record_detail(window.records_table.model().index(0, 0))

        assert window.records_table.model().rowCount() == 1
        assert dialog is opened[0]
        assert dialog.detail_model.data(dialog.detail_model.index(0, 1)) == "Dato Ficticio Dos"


def test_edicion_en_memoria_actualiza_tabla_y_marca_pendiente(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Accepted)
        monkeypatch.setattr(
            RecordEditDialog,
            "edited_values",
            lambda self: {"Columna A": " Dato Ficticio Editado ", "Columna B": "A-001", "Vigencia": "D.M."},
        )

        window.load_selected_workbook()
        assert window.edit_record_at_source_row(0) is True

        assert window.records_table.model().data(window.records_table.model().index(0, 0)) == "Dato Ficticio Editado"
        assert window.pending_changes_label.text() == "Cambios pendientes: 1"
        assert window._records_model.pending_changes_count() == 1
        assert window.audit_count_label.text() == "Cambios registrados: 1"
        assert window.audit_table.model().rowCount() == 1
        assert window.audit_table.model().data(window.audit_table.model().index(0, 1)) == "Fila 2"
        assert window.audit_table.model().data(window.audit_table.model().index(0, 2)) == "Columna A"
        assert window.audit_table.model().data(window.audit_table.model().index(0, 3)) == "Dato Ficticio Uno"
        assert window.audit_table.model().data(window.audit_table.model().index(0, 4)) == "Dato Ficticio Editado"
        assert "Cambios pendientes sin guardar" in window.statusBar().currentMessage()


def test_cancelar_edicion_no_aplica_cambios(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Rejected)
        monkeypatch.setattr(RecordEditDialog, "edited_values", lambda self: {"Columna A": "No aplicar"})

        window.load_selected_workbook()

        assert window.edit_record_at_source_row(0) is False
        assert window.records_table.model().data(window.records_table.model().index(0, 0)) == "Dato Ficticio Uno"
        assert window.pending_changes_label.text() == "Cambios pendientes: 0"
        assert window.audit_table.model().rowCount() == 0


def test_editar_varios_campos_genera_varias_entradas_de_bitacora(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Accepted)
        monkeypatch.setattr(
            RecordEditDialog,
            "edited_values",
            lambda self: {"Columna A": "Dato Editado", "Columna B": "A-009", "Vigencia": "D.M."},
        )

        window.load_selected_workbook()
        assert window.edit_record_at_source_row(0) is True

        assert window.pending_changes_label.text() == "Cambios pendientes: 2"
        assert window.audit_count_label.text() == "Cambios registrados: 2"
        assert window.audit_table.model().rowCount() == 2
        assert window.audit_table.model().data(window.audit_table.model().index(0, 2)) == "Columna A"
        assert window.audit_table.model().data(window.audit_table.model().index(1, 2)) == "Columna B"


def test_aplicar_edicion_sin_cambios_no_registra_bitacora(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Accepted)
        monkeypatch.setattr(
            RecordEditDialog,
            "edited_values",
            lambda self: {"Columna A": "Dato Ficticio Uno", "Columna B": "A-001", "Vigencia": "D.M."},
        )

        window.load_selected_workbook()

        assert window.edit_record_at_source_row(0) is False
        assert window.pending_changes_label.text() == "Cambios pendientes: 0"
        assert window.audit_table.model().rowCount() == 0


def test_edicion_con_error_bloqueante_no_aplica_cambios_ni_bitacora(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result_for_validation(), default_path=source, show_dialogs=False)

        def fake_exec(self):
            self._inputs["Nº Póliza"].setText("")
            self._confirm_and_accept()
            return self.result()

        monkeypatch.setattr(RecordEditDialog, "exec", fake_exec)

        window.load_selected_workbook()

        assert window.edit_record_at_source_row(0) is False
        assert window._records_model.record_at(0).values_by_column["Nº Póliza"] == "01-ABC"
        assert window.pending_changes_label.text() == "Cambios pendientes: 0"
        assert window.audit_table.model().rowCount() == 0


def test_edicion_con_advertencia_cancelada_no_aplica_cambios(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result_for_validation(), default_path=source, show_dialogs=True)

        def fake_exec(self):
            self._inputs["Correo"].setText("correo.example.test")
            self._confirm_and_accept()
            return self.result()

        monkeypatch.setattr(RecordEditDialog, "exec", fake_exec)
        monkeypatch.setattr(RecordEditDialog, "_confirm_validation_warnings", lambda self, warnings: False)

        window.load_selected_workbook()

        assert window.edit_record_at_source_row(0) is False
        assert window._records_model.record_at(0).values_by_column["Correo"] == "correo@example.test"
        assert window.audit_table.model().rowCount() == 0


def test_edicion_con_advertencia_confirmada_aplica_cambios_y_bitacora(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result_for_validation(), default_path=source, show_dialogs=True)

        def fake_exec(self):
            self._inputs["Correo"].setText("correo.example.test")
            self._confirm_and_accept()
            return self.result()

        monkeypatch.setattr(RecordEditDialog, "exec", fake_exec)
        monkeypatch.setattr(RecordEditDialog, "_confirm_validation_warnings", lambda self, warnings: True)
        monkeypatch.setattr(RecordEditDialog, "_confirm_apply_changes", lambda self: True)

        window.load_selected_workbook()

        assert window.edit_record_at_source_row(0) is True
        assert window._records_model.record_at(0).values_by_column["Correo"] == "correo.example.test"
        assert window.pending_changes_label.text() == "Cambios pendientes: 1"
        assert window.audit_table.model().rowCount() == 1


def test_busqueda_se_actualiza_despues_de_editar(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Accepted)
        monkeypatch.setattr(
            RecordEditDialog,
            "edited_values",
            lambda self: {"Columna A": "Dato Cambiado", "Columna B": "A-001", "Vigencia": "D.M."},
        )

        window.load_selected_workbook()
        window.search_edit.setText("uno")
        assert window.records_table.model().rowCount() == 1

        assert window.edit_record_at_source_row(0) is True

        assert window.search_edit.text() == "uno"
        assert window.records_table.model().rowCount() == 0
        assert window.search_results_label.text() == "Mostrando 0 de 2 registros"
        assert window.audit_table.model().rowCount() == 1


def test_detalle_abre_edicion_desde_boton(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)
        edit_calls: list[int] = []

        def fake_edit(source_row, detail_dialog=None):
            edit_calls.append(source_row)
            return True

        monkeypatch.setattr(RecordDetailDialog, "exec", lambda self: 0)
        monkeypatch.setattr(window, "edit_record_at_source_row", fake_edit)

        window.load_selected_workbook()
        dialog = window.open_record_detail(window.records_table.model().index(1, 0))
        dialog.edit_button.click()

        assert edit_calls == [1]


def test_cargar_con_cambios_pendientes_puede_cancelarse(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        load_count = {"value": 0}

        def loader(path):
            load_count["value"] += 1
            return build_result()

        window = MainWindow(loader=loader, default_path=source, show_dialogs=False)
        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Accepted)
        monkeypatch.setattr(
            RecordEditDialog,
            "edited_values",
            lambda self: {"Columna A": "Dato Editado", "Columna B": "A-001", "Vigencia": "D.M."},
        )

        window.load_selected_workbook()
        window.edit_record_at_source_row(0)
        window._show_dialogs = True
        monkeypatch.setattr(window, "_confirm_discard_pending_changes", lambda: False)

        window.load_selected_workbook()

        assert load_count["value"] == 1
        assert window.pending_changes_label.text() == "Cambios pendientes: 1"
        assert window.audit_table.model().rowCount() == 1


def test_cargar_otro_archivo_descartando_cambios_limpia_bitacora(qapp, monkeypatch):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)
        monkeypatch.setattr(RecordEditDialog, "exec", lambda self: RecordEditDialog.DialogCode.Accepted)
        monkeypatch.setattr(
            RecordEditDialog,
            "edited_values",
            lambda self: {"Columna A": "Dato Editado", "Columna B": "A-001", "Vigencia": "D.M."},
        )

        window.load_selected_workbook()
        window.edit_record_at_source_row(0)
        window._show_dialogs = True
        monkeypatch.setattr(window, "_confirm_discard_pending_changes", lambda: True)

        window.load_selected_workbook()

        assert window.pending_changes_label.text() == "Cambios pendientes: 0"
        assert window.audit_count_label.text() == "Cambios registrados: 0"
        assert window.audit_table.model().rowCount() == 0
        assert not window.audit_empty_label.isHidden()


def test_detalle_no_abre_con_indice_invalido(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()

        assert window.open_record_detail(None) is None


def test_cargar_nuevo_control_cartera_limpia_busqueda(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()
        window.search_edit.setText("uno")
        assert window.records_table.model().rowCount() == 1

        window.load_selected_workbook()

        assert window.search_edit.text() == ""
        assert window.search_column_combo.currentText() == "Todas las columnas"
        assert window.records_table.model().rowCount() == 2
        assert window.search_results_label.text() == "Mostrando 2 de 2 registros"
        assert window.audit_table.model().rowCount() == 0
        assert window.audit_count_label.text() == "Cambios registrados: 0"


def test_tema_claro_y_oscuro_pueden_aplicarse(qapp):
    with workspace_tempdir() as temp_dir:
        window = MainWindow(
            loader=lambda path: build_result(),
            default_path="data/input/CONTROLCARTERA_V2.xlsx",
            show_dialogs=False,
            settings=build_settings(temp_dir / "ui_settings.ini"),
        )
        theme_button = window.findChild(QPushButton, "themeToggleButton")

        assert theme_button is not None
        assert window.current_theme == LIGHT_THEME
        assert theme_button.text() == "🌙"

        window.apply_theme(DARK_THEME, persist=False)

        assert window.current_theme == DARK_THEME
        assert theme_button.text() == "☀"
        assert "Tema oscuro aplicado" in window.last_user_message

        window.apply_theme(LIGHT_THEME, persist=False)

        assert window.current_theme == LIGHT_THEME
        assert theme_button.text() == "🌙"
        assert "Tema claro aplicado" in window.last_user_message


def test_boton_compacto_cambia_tema(qapp):
    with workspace_tempdir() as temp_dir:
        window = MainWindow(
            loader=lambda path: build_result(),
            default_path="data/input/CONTROLCARTERA_V2.xlsx",
            show_dialogs=False,
            settings=build_settings(temp_dir / "ui_settings.ini"),
        )
        theme_button = window.findChild(QPushButton, "themeToggleButton")

        assert window.current_theme == LIGHT_THEME
        theme_button.click()

        assert window.current_theme == DARK_THEME
        assert theme_button.text() == "☀"
        assert "Tema oscuro aplicado" in window.last_user_message


def test_preferencia_de_tema_se_recuerda_con_qsettings(qapp):
    with workspace_tempdir() as temp_dir:
        settings_path = temp_dir / "ui_settings.ini"
        settings = build_settings(settings_path)
        window = MainWindow(
            loader=lambda path: build_result(),
            default_path="data/input/CONTROLCARTERA_V2.xlsx",
            show_dialogs=False,
            settings=settings,
        )

        window.apply_theme(DARK_THEME, persist=True)

        assert settings.value(THEME_SETTING_KEY) == DARK_THEME
        remembered_window = MainWindow(
            loader=lambda path: build_result(),
            default_path="data/input/CONTROLCARTERA_V2.xlsx",
            show_dialogs=False,
            settings=QSettings(str(settings_path), QSettings.Format.IniFormat),
        )
        assert remembered_window.current_theme == DARK_THEME
        assert remembered_window.findChild(QPushButton, "themeToggleButton").text() == "☀"


def test_cambiar_tema_no_limpia_registros_cargados(qapp):
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_ficticio.xlsx"
        source.write_bytes(b"archivo ficticio para prueba gui")
        window = MainWindow(loader=lambda path: build_result(), default_path=source, show_dialogs=False)

        window.load_selected_workbook()
        window.search_edit.setText("uno")
        assert window.records_table.model().rowCount() == 1

        window.apply_theme(DARK_THEME, persist=False)

        assert window.search_edit.text() == "uno"
        assert window.records_table.model().rowCount() == 1
        assert window.records_table.model().columnCount() == 3
        assert window._summary_labels["estado"].text() == "Cargado correctamente"


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
    assert "gestor-seguros 1.10.3" in completed.stdout
