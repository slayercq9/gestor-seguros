import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QDialogButtonBox, QPushButton, QTableView

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.detail_dialog import RecordDetailDialog
from app.ui.theme import LIGHT_THEME


def test_dialogo_de_detalle_muestra_solo_campos_con_informacion():
    app = QApplication.instance() or QApplication([])
    record = WorkbookRowRecord(
        row_number=2,
        values_by_column={"Cliente": "Persona Ficticia", "Telefono": "", "Correo": None},
    )

    dialog = RecordDetailDialog(record, ("Cliente", "Telefono", "Correo"), LIGHT_THEME)

    assert app is not None
    assert dialog.windowTitle() == "Detalle del registro"
    assert dialog.detail_model.rowCount() == 1
    assert dialog.findChild(QTableView, "recordDetailDialogTable").editTriggers() == QTableView.EditTrigger.NoEditTriggers
    assert dialog.findChild(QPushButton, "editRecordButton").text() == "Editar registro"
    assert dialog.findChild(QDialogButtonBox, "recordDetailCloseButtons").button(QDialogButtonBox.StandardButton.Close).text() == "Cerrar"


def test_dialogo_de_detalle_muestra_mensaje_si_no_hay_campos():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Cliente": None})

    dialog = RecordDetailDialog(record, ("Cliente",), LIGHT_THEME)

    assert dialog.detail_model.rowCount() == 0
    assert not dialog.empty_label.isHidden()
    assert "No hay campos con información" in dialog.empty_label.text()


def test_boton_editar_invoca_callback():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Cliente": "Persona Ficticia"})
    dialog = RecordDetailDialog(record, ("Cliente",), LIGHT_THEME)
    called = {"value": False}

    dialog.set_edit_callback(lambda detail_dialog: called.update(value=detail_dialog is dialog) or True)
    dialog.edit_button.click()

    assert called["value"] is True
