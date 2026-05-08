from datetime import date, datetime

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


def test_modelo_expone_tooltips_con_valor_completo():
    record = WorkbookRowRecord(
        row_number=2,
        values_by_column={"Nombre del Asegurado": "Nombre Ficticio Muy Largo Para Revisar Tooltip"},
    )
    model = RecordsTableModel((record,), ("Nombre del Asegurado",))

    index = model.index(0, 0)

    assert model.data(index, Qt.ItemDataRole.DisplayRole) == "Nombre Ficticio Muy Largo Para Revisar Tooltip"
    assert model.data(index, Qt.ItemDataRole.ToolTipRole) == "Nombre Ficticio Muy Largo Para Revisar Tooltip"
    assert model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.ToolTipRole) == "Nombre del Asegurado"


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

    changes = model.preview_update_changes(0, {"Columna A": " Dato Editado ", "Columna B": ""})
    updated = model.update_record(0, {"Columna A": " Dato Editado ", "Columna B": ""})

    assert len(changes) == 1
    assert changes[0].field_name == "Columna A"
    assert changes[0].previous_value == "Dato Ficticio Uno"
    assert changes[0].new_value == "Dato Editado"
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


def test_modelo_no_reporta_cambios_si_valores_son_iguales():
    model = RecordsTableModel(build_records(), ("Columna A", "Columna B"))

    changes = model.preview_update_changes(0, {"Columna A": "Dato Ficticio Uno", "Columna B": ""})

    assert changes == ()
    assert model.update_record(0, {"Columna A": "Dato Ficticio Uno", "Columna B": ""}) is False
    assert model.pending_changes_count() == 0


def test_modelo_muestra_emision_datetime_sin_hora():
    record = WorkbookRowRecord(
        row_number=2,
        values_by_column={"Emisión": datetime(2022, 3, 8, 0, 0, 0), "Otro Campo": datetime(2022, 3, 8, 0, 0, 0)},
    )
    model = RecordsTableModel((record,), ("Emisión", "Otro Campo"))

    assert model.data(model.index(0, 0)) == "2022-03-08"
    assert model.data(model.index(0, 1)) == "2022-03-08 00:00:00"
    assert model.data(model.index(0, 0), Qt.ItemDataRole.ToolTipRole) == "2022-03-08"


def test_modelo_muestra_emision_texto_iso_sin_hora_cero():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Emisión": "2022-03-08 00:00:00"})
    model = RecordsTableModel((record,), ("Emisión",))

    assert model.data(model.index(0, 0)) == "2022-03-08"


def test_modelo_conserva_emision_no_reconocible():
    record = WorkbookRowRecord(row_number=2, values_by_column={"Emisión": "08/03/2022 7 p.m."})
    model = RecordsTableModel((record,), ("Emisión",))

    assert model.data(model.index(0, 0)) == "08/03/2022 7 p.m."
