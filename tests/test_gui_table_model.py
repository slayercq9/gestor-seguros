from datetime import date

from PySide6.QtCore import Qt

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.table_model import RecordsTableModel


def build_records() -> tuple[WorkbookRowRecord, ...]:
    return (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={"COL_A": "Cliente Ficticio", "COL_B": None},
            gs_values={"GS_ES_DM": "si", "GS_FECHA_VENCIMIENTO_TECNICA": date(2026, 5, 1)},
        ),
        WorkbookRowRecord(
            row_number=3,
            values_by_column={"COL_A": "Cliente Ejemplo", "COL_B": "Texto"},
            gs_values={"GS_ES_DM": "no", "GS_FECHA_VENCIMIENTO_TECNICA": None},
        ),
    )


def test_modelo_reporta_filas_columnas_y_encabezados():
    model = RecordsTableModel(build_records(), ("COL_A", "COL_B", "GS_ES_DM"))

    assert model.rowCount() == 2
    assert model.columnCount() == 3
    assert model.headerData(0, Qt.Orientation.Horizontal) == "COL_A"
    assert model.headerData(1, Qt.Orientation.Vertical) == "2"


def test_modelo_devuelve_valores_como_texto_seguro():
    model = RecordsTableModel(build_records(), ("COL_A", "COL_B", "GS_ES_DM", "GS_FECHA_VENCIMIENTO_TECNICA"))

    assert model.data(model.index(0, 0)) == "Cliente Ficticio"
    assert model.data(model.index(0, 1)) == ""
    assert model.data(model.index(0, 2)) == "si"
    assert model.data(model.index(0, 3)) == "2026-05-01"


def test_modelo_es_solo_lectura():
    model = RecordsTableModel(build_records(), ("COL_A",))
    flags = model.flags(model.index(0, 0))

    assert flags & Qt.ItemFlag.ItemIsEnabled
    assert flags & Qt.ItemFlag.ItemIsSelectable
    assert not flags & Qt.ItemFlag.ItemIsEditable


def test_modelo_puede_limpiarse_sin_modificar_registros_originales():
    records = build_records()
    model = RecordsTableModel(records, ("COL_A",))

    model.clear()

    assert model.rowCount() == 0
    assert records[0].values_by_column["COL_A"] == "Cliente Ficticio"
