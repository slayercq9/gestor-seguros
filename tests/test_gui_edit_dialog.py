import os
from datetime import datetime

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QComboBox, QDialogButtonBox, QLineEdit, QPlainTextEdit

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


def test_dialogo_de_edicion_muestra_alias_de_emision_sin_hora():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Fecha Emision": datetime(2022, 3, 8, 0, 0, 0)})

    dialog = RecordEditDialog(record, ("Fecha Emision",), LIGHT_THEME, confirm_changes=False)
    field = dialog.findChildren(QLineEdit, "editRecordField")[0]

    assert field.text() == "2022-03-08"


def test_dialogo_de_edicion_bloquea_emision_invalida(monkeypatch):
    record = WorkbookRowRecord(row_number=2, values_by_column={"Emisión": "2022-03-08"})
    dialog = RecordEditDialog(record, ("Emisión",), LIGHT_THEME, confirm_changes=True)
    field = dialog.findChild(QLineEdit, "editRecordField")
    field.setText("fds")
    shown_errors = []
    monkeypatch.setattr(dialog, "_show_validation_errors", lambda errors: shown_errors.extend(errors))
    monkeypatch.setattr(dialog, "_confirm_apply_changes", lambda: True)

    dialog._confirm_and_accept()

    assert shown_errors
    assert "fecha válida" in shown_errors[0].message
    assert dialog.result() == RecordEditDialog.DialogCode.Rejected


def test_dialogo_de_edicion_usa_combobox_para_vigencia_dia_y_mes():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Vigencia": "D.M.", "DÍA": "15", "MES": "7"})

    dialog = RecordEditDialog(record, ("Vigencia", "DÍA", "MES"), LIGHT_THEME, confirm_changes=False)
    combos = dialog.findChildren(QComboBox, "editRecordComboField")

    assert len(combos) == 3
    assert combos[0].currentText() == "D.M."
    assert combos[0].findText("Mensual") >= 0
    assert combos[1].currentText() == "15"
    assert combos[1].findText("") >= 0
    assert combos[1].findText("31") >= 0
    assert combos[2].currentText() == "7"
    assert combos[2].findText("12") >= 0


def test_dialogo_de_edicion_conserva_vigencia_no_reconocida():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Vigencia": "Bimestral"})

    dialog = RecordEditDialog(record, ("Vigencia",), LIGHT_THEME, confirm_changes=False)
    combo = dialog.findChild(QComboBox, "editRecordComboField")

    assert combo.currentText() == "Bimestral"
    assert dialog.edited_values() == {"Vigencia": "Bimestral"}


def test_dialogo_de_edicion_usa_controles_con_alias():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Frecuencia": "Mensual", "Dia": "1", "Mes": "2"})

    dialog = RecordEditDialog(record, ("Frecuencia", "Dia", "Mes"), LIGHT_THEME, confirm_changes=False)
    combos = dialog.findChildren(QComboBox, "editRecordComboField")

    assert len(combos) == 3
    assert combos[0].currentText() == "Mensual"
    assert combos[1].currentText() == "1"
    assert combos[2].currentText() == "2"


def test_dialogo_de_edicion_usa_area_multilinea_para_detalle():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Detalle": "Línea ficticia 1\nLínea ficticia 2"})

    dialog = RecordEditDialog(record, ("Detalle",), LIGHT_THEME, confirm_changes=False)
    detail_field = dialog.findChild(QPlainTextEdit, "editRecordTextArea")

    assert detail_field is not None
    assert detail_field.toPlainText() == "Línea ficticia 1\nLínea ficticia 2"
    detail_field.setPlainText("Detalle editado")
    assert dialog.edited_values() == {"Detalle": "Detalle editado"}


def test_dialogo_de_edicion_bloquea_errores_sin_aplicar(monkeypatch):
    record = WorkbookRowRecord(row_number=2, values_by_column={"Nº Póliza": "01-ABC"})
    dialog = RecordEditDialog(record, ("Nº Póliza",), LIGHT_THEME, confirm_changes=True)
    field = dialog.findChild(QLineEdit, "editRecordField")
    field.setText("")
    shown_errors = []
    monkeypatch.setattr(dialog, "_show_validation_errors", lambda errors: shown_errors.extend(errors))
    monkeypatch.setattr(dialog, "_confirm_apply_changes", lambda: True)

    dialog._confirm_and_accept()

    assert shown_errors
    assert dialog.result() == RecordEditDialog.DialogCode.Rejected


def test_dialogo_de_edicion_permite_cancelar_advertencias(monkeypatch):
    record = WorkbookRowRecord(row_number=2, values_by_column={"Correo": "correo@example.test"})
    dialog = RecordEditDialog(record, ("Correo",), LIGHT_THEME, confirm_changes=True)
    field = dialog.findChild(QLineEdit, "editRecordField")
    field.setText("correo.example.test")
    monkeypatch.setattr(dialog, "_confirm_validation_warnings", lambda warnings: False)
    monkeypatch.setattr(dialog, "_confirm_apply_changes", lambda: True)

    dialog._confirm_and_accept()

    assert dialog.result() == RecordEditDialog.DialogCode.Rejected


def test_dialogo_de_edicion_permite_aplicar_con_advertencias(monkeypatch):
    record = WorkbookRowRecord(row_number=2, values_by_column={"Correo": "correo@example.test"})
    dialog = RecordEditDialog(record, ("Correo",), LIGHT_THEME, confirm_changes=True)
    field = dialog.findChild(QLineEdit, "editRecordField")
    field.setText("correo.example.test")
    monkeypatch.setattr(dialog, "_confirm_validation_warnings", lambda warnings: True)
    monkeypatch.setattr(dialog, "_confirm_apply_changes", lambda: True)

    dialog._confirm_and_accept()

    assert dialog.result() == RecordEditDialog.DialogCode.Accepted
