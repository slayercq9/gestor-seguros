from datetime import date

from PySide6.QtCore import Qt

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.table_model import RecordsTableModel


def build_records() -> tuple[WorkbookRowRecord, ...]:
    return (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={"Columna A": "Dato Ficticio Uno", "Columna B": None, "Fecha": date(2026, 5, 1)},
        ),
        WorkbookRowRecord(
            row_number=3,
            values_by_column={"Columna A": "Dato Ficticio Dos", "Columna B": "Texto", "Fecha": None},
        ),
    )


def test_modelo_reporta_filas_columnas_y_encabezados():
    model = RecordsTableModel(build_records(), ("Columna A", "Columna B", "Fecha"))

    assert model.rowCount() == 2
    assert model.columnCount() == 3
    assert model.headerData(0, Qt.Orientation.Horizontal) == "Columna A"
    assert model.headerData(1, Qt.Orientation.Vertical) == "2"


def test_modelo_devuelve_valores_como_texto_seguro():
    model = RecordsTableModel(build_records(), ("Columna A", "Columna B", "Fecha"))

    assert model.data(model.index(0, 0)) == "Dato Ficticio Uno"
    assert model.data(model.index(0, 1)) == ""
    assert model.data(model.index(0, 2)) == "2026-05-01"


def test_modelo_es_solo_lectura():
    model = RecordsTableModel(build_records(), ("Columna A",))
    flags = model.flags(model.index(0, 0))

    assert flags & Qt.ItemFlag.ItemIsEnabled
    assert flags & Qt.ItemFlag.ItemIsSelectable
    assert not flags & Qt.ItemFlag.ItemIsEditable


def test_modelo_puede_limpiarse_sin_modificar_registros_originales():
    records = build_records()
    model = RecordsTableModel(records, ("Columna A",))

    model.clear()

    assert model.rowCount() == 0
    assert records[0].values_by_column["Columna A"] == "Dato Ficticio Uno"


def test_modelo_expone_registro_fuente_para_detalle():
    records = build_records()
    model = RecordsTableModel(records, ("Columna A", "Columna B"))

    assert model.headers() == ("Columna A", "Columna B")
    assert model.record_at(1) == records[1]
    assert model.record_at(99) is None


def test_modelo_actualiza_valor_en_memoria_y_marca_pendiente():
    model = RecordsTableModel(build_records(), ("Columna A", "Columna B", "Fecha"))

    updated = model.update_record(0, {"Columna A": " Dato Editado ", "Columna B": ""})

    assert updated is True
    assert model.data(model.index(0, 0)) == "Dato Editado"
    assert model.data(model.index(0, 1)) == ""
    assert model.record_at(1).values_by_column["Columna A"] == "Dato Ficticio Dos"
    assert model.has_pending_changes()
    assert model.pending_changes_count() == 1


def test_modelo_revierte_marca_pendiente_si_vuelve_al_valor_original():
    model = RecordsTableModel(build_records(), ("Columna A",))

    assert model.update_record(0, {"Columna A": "Dato Editado"}) is True
    assert model.pending_changes_count() == 1
    assert model.update_record(0, {"Columna A": "Dato Ficticio Uno"}) is True

    assert model.pending_changes_count() == 0
    assert not model.has_pending_changes()
