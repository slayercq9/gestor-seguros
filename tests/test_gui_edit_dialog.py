import os
from datetime import datetime

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QDialogButtonBox, QLineEdit

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.edit_dialog import RecordEditDialog
from app.ui.theme import LIGHT_THEME


def test_dialogo_de_edicion_muestra_campos_editables():
    app = QApplication.instance() or QApplication([])
    record = WorkbookRowRecord(row_number=2, values_by_column={"Cliente": "Persona Ficticia", "Telefono": ""})

    dialog = RecordEditDialog(record, ("Cliente", "Telefono"), LIGHT_THEME, confirm_changes=False)
    fields = dialog.findChildren(QLineEdit, "editRecordField")

    assert app is not None
    assert dialog.windowTitle() == "Editar registro"
    assert len(fields) == 2
    assert fields[0].text() == "Persona Ficticia"
    assert fields[1].text() == ""
    assert dialog.findChild(QDialogButtonBox, "editRecordButtons") is not None


def test_dialogo_de_edicion_expone_valores_modificados():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Cliente": "Persona Ficticia"})
    dialog = RecordEditDialog(record, ("Cliente",), LIGHT_THEME, confirm_changes=False)
    field = dialog.findChildren(QLineEdit, "editRecordField")[0]

    field.setText(" Persona Editada ")

    assert dialog.edited_values() == {"Cliente": " Persona Editada "}


def test_dialogo_de_edicion_no_muestra_coberturas_si_no_son_visibles():
    record = WorkbookRowRecord(
        row_number=2,
        values_by_column={"Cliente": "Persona Ficticia", "Cobertura A": "Cobertura Ficticia"},
    )

    dialog = RecordEditDialog(record, ("Cliente",), LIGHT_THEME, confirm_changes=False)
    fields = dialog.findChildren(QLineEdit, "editRecordField")

    assert len(fields) == 1
    assert dialog.edited_values() == {"Cliente": "Persona Ficticia"}


def test_dialogo_de_edicion_muestra_emision_sin_hora():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Emisión": datetime(2022, 3, 8, 0, 0, 0)})

    dialog = RecordEditDialog(record, ("Emisión",), LIGHT_THEME, confirm_changes=False)
    field = dialog.findChildren(QLineEdit, "editRecordField")[0]

    assert field.text() == "2022-03-08"
