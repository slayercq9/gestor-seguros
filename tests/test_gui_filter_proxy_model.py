import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.filter_proxy_model import ALL_COLUMNS_INDEX, RecordsFilterProxyModel
from app.ui.table_model import RecordsTableModel


def build_proxy() -> tuple[RecordsFilterProxyModel, RecordsTableModel, tuple[WorkbookRowRecord, ...]]:
    app = QApplication.instance() or QApplication([])
    assert app is not None
    records = (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={"Cliente": "José Ficticio", "Póliza": "01-ABC", "Placa": "ABC123"},
        ),
        WorkbookRowRecord(
            row_number=3,
            values_by_column={"Cliente": "Cliente Dos", "Póliza": "02-XYZ", "Placa": None},
        ),
    )
    source_model = RecordsTableModel(records, ("Cliente", "Póliza", "Placa"))
    proxy = RecordsFilterProxyModel()
    proxy.setSourceModel(source_model)
    return proxy, source_model, records


def test_busqueda_vacia_muestra_todos_los_registros():
    proxy, source_model, _ = build_proxy()

    proxy.set_search_text("")

    assert source_model.rowCount() == 2
    assert proxy.rowCount() == 2


def test_busqueda_general_ignora_mayusculas_y_tildes():
    proxy, _, _ = build_proxy()

    proxy.set_search_text(" jose ")

    assert proxy.rowCount() == 1


def test_busqueda_por_columna_especifica():
    proxy, _, _ = build_proxy()

    proxy.set_search_column(1)
    proxy.set_search_text("02")

    assert proxy.rowCount() == 1

    proxy.set_search_column(0)
    proxy.set_search_text("02")

    assert proxy.rowCount() == 0


def test_busqueda_sin_coincidencias_y_valores_vacios():
    proxy, _, _ = build_proxy()

    proxy.set_search_column(2)
    proxy.set_search_text("sin coincidencia")

    assert proxy.rowCount() == 0


def test_filtrado_no_modifica_registros_originales():
    proxy, _, records = build_proxy()

    proxy.set_search_column(ALL_COLUMNS_INDEX)
    proxy.set_search_text("cliente")

    assert proxy.rowCount() == 1
    assert records[0].values_by_column["Cliente"] == "José Ficticio"
    assert records[1].values_by_column["Placa"] is None
