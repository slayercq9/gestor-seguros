from datetime import date

from PySide6.QtCore import Qt

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.detail_model import RecordDetailModel


def test_detalle_muestra_campos_en_orden_visible():
    model = RecordDetailModel()
    record = WorkbookRowRecord(
        row_number=2,
        values_by_column={"Cliente": "Persona Ficticia", "Poliza": "01-FICTICIA", "Fecha": date(2026, 5, 1)},
    )

    model.set_record(record, ("Cliente", "Poliza", "Fecha"))

    assert model.rowCount() == 3
    assert model.columnCount() == 2
    assert model.headerData(0, Qt.Orientation.Horizontal) == "Campo"
    assert model.headerData(1, Qt.Orientation.Horizontal) == "Valor"
    assert model.data(model.index(0, 0)) == "Cliente"
    assert model.data(model.index(0, 1)) == "Persona Ficticia"
    assert model.data(model.index(2, 1)) == "2026-05-01"


def test_detalle_omite_campos_vacios():
    model = RecordDetailModel()
    record = WorkbookRowRecord(
        row_number=2,
        values_by_column={"Cliente": None, "Telefono": "", "Correo": "   ", "Estado": "Activo"},
    )

    model.set_record(record, ("Cliente", "Telefono", "Correo", "Estado"))

    assert model.rowCount() == 1
    assert model.data(model.index(0, 0)) == "Estado"
    assert model.data(model.index(0, 1)) == "Activo"


def test_detalle_es_solo_lectura_y_puede_limpiarse():
    model = RecordDetailModel()
    record = WorkbookRowRecord(row_number=2, values_by_column={"Cliente": "Dato Ficticio"})

    model.set_record(record, ("Cliente",))
    flags = model.flags(model.index(0, 1))
    model.clear()

    assert flags & Qt.ItemFlag.ItemIsEnabled
    assert flags & Qt.ItemFlag.ItemIsSelectable
    assert not flags & Qt.ItemFlag.ItemIsEditable
    assert model.rowCount() == 0
