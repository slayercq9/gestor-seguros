import os
import shutil
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from openpyxl import Workbook
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QLineEdit, QPlainTextEdit

from app.services.workbook_loader import load_control_cartera
from app.ui.detail_model import RecordDetailModel
from app.ui.edit_dialog import RecordEditDialog
from app.ui.main_window import MainWindow
from app.ui.table_model import RecordsTableModel


def test_flujo_integral_con_alias_validacion_y_bitacora(monkeypatch):
    app = QApplication.instance() or QApplication([])
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "control_cartera_alias.xlsx"
        _build_alias_workbook(source)

        result = load_control_cartera(source)

        assert app is not None
        assert "Cobertura Ficticia" not in result.summary.visible_columns
        assert "Cobertura Ficticia" in result.records[0].values_by_column

        table_model = RecordsTableModel(result.records, result.summary.visible_columns)
        issue_column = result.summary.visible_columns.index("Fecha Emision")
        assert table_model.data(table_model.index(0, issue_column)) == "2022-03-08"
        assert table_model.data(table_model.index(0, issue_column), Qt.ItemDataRole.ToolTipRole) == "2022-03-08"

        detail_model = RecordDetailModel()
        detail_model.set_record(result.records[0], result.summary.visible_columns)
        detail_values = {
            detail_model.data(detail_model.index(row, 0)): detail_model.data(detail_model.index(row, 1))
            for row in range(detail_model.rowCount())
        }
        assert detail_values["Fecha Emision"] == "2022-03-08"

        window = MainWindow(loader=load_control_cartera, default_path=source, show_dialogs=False)
        window.load_selected_workbook()
        assert window.search_column_combo.findText("Cobertura Ficticia") == -1

        monkeypatch.setattr(RecordEditDialog, "exec", _edit_with({"Poliza": ""}))
        assert window.edit_record_at_source_row(0) is False
        assert window.audit_table.model().rowCount() == 0

        monkeypatch.setattr(RecordEditDialog, "exec", _edit_with({"Dia": "31", "Mes": "4", "Ano": "2026"}))
        assert window.edit_record_at_source_row(0) is False
        assert window.audit_table.model().rowCount() == 0

        monkeypatch.setattr(RecordEditDialog, "exec", _edit_with({"Monto Prima": "abc"}))
        assert window.edit_record_at_source_row(0) is False
        assert window.audit_table.model().rowCount() == 0

        monkeypatch.setattr(RecordEditDialog, "exec", _edit_with({"Cliente": "Persona Ficticia Editada"}))
        assert window.edit_record_at_source_row(0) is True
        assert window._records_model.record_at(0).values_by_column["Cliente"] == "Persona Ficticia Editada"
        assert window.audit_table.model().rowCount() == 1
        assert window.audit_table.model().data(window.audit_table.model().index(0, 2)) == "Cliente"


@contextmanager
def workspace_tempdir():
    base_dir = Path("data/output")
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"tmp-integral-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _build_alias_workbook(path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "CONTROLCARTERA"
    sheet.append(
        (
            "Poliza",
            "Cliente",
            "Frecuencia",
            "Dia",
            "Mes",
            "Ano",
            "Fecha Emision",
            "Monto Prima",
            "Email",
            "Cobertura Ficticia",
        )
    )
    sheet.append(
        (
            "01-ABC",
            "Persona Ficticia",
            "Anual",
            "29",
            "2",
            "2024",
            datetime(2022, 3, 8, 0, 0, 0),
            "1000.50",
            "correo@example.test",
            "Dato de cobertura conservado",
        )
    )
    workbook.save(path)


def _edit_with(values_by_column):
    def fake_exec(dialog):
        for column_name, value in values_by_column.items():
            _set_field_text(dialog._inputs[column_name], value)
        dialog._confirm_and_accept()
        return dialog.result()

    return fake_exec


def _set_field_text(field, value):
    if isinstance(field, QLineEdit):
        field.setText(value)
    elif isinstance(field, QComboBox):
        field.setCurrentText(value)
    elif isinstance(field, QPlainTextEdit):
        field.setPlainText(value)
