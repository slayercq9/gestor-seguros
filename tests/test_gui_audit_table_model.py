from datetime import datetime

from PySide6.QtCore import Qt

from app.domain.audit_log import AuditEntry
from app.ui.audit_table_model import AuditTableModel


def build_entries() -> tuple[AuditEntry, ...]:
    return (
        AuditEntry(
            changed_at=datetime(2026, 5, 7, 11, 0, 0),
            record_number=2,
            field_name="Cliente",
            previous_value="Valor anterior",
            new_value="Valor nuevo",
        ),
    )


def test_modelo_de_bitacora_muestra_columnas_y_valores():
    model = AuditTableModel(build_entries())

    assert model.rowCount() == 1
    assert model.columnCount() == 7
    assert model.headerData(0, Qt.Orientation.Horizontal) == "Fecha y hora"
    assert model.headerData(1, Qt.Orientation.Horizontal) == "Registro"
    assert model.data(model.index(0, 0)) == "2026-05-07 11:00:00"
    assert model.data(model.index(0, 1)) == "Fila 2"
    assert model.data(model.index(0, 2)) == "Cliente"
    assert model.data(model.index(0, 3)) == "Valor anterior"
    assert model.data(model.index(0, 4)) == "Valor nuevo"
    assert model.data(model.index(0, 5)) == "Edición manual en app"
    assert model.data(model.index(0, 6)) == "Pendiente de guardado"


def test_modelo_de_bitacora_es_solo_lectura_y_puede_limpiarse():
    model = AuditTableModel(build_entries())
    flags = model.flags(model.index(0, 0))

    assert flags & Qt.ItemFlag.ItemIsEnabled
    assert flags & Qt.ItemFlag.ItemIsSelectable
    assert not flags & Qt.ItemFlag.ItemIsEditable

    model.clear()

    assert model.rowCount() == 0
