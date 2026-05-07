"""Modelo de tabla Qt de solo lectura para registros cargados del Control Cartera."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from app.domain.workbook_records import WorkbookRowRecord


class RecordsTableModel(QAbstractTableModel):
    """Expone los registros cargados a Qt sin permitir edición."""

    def __init__(
        self,
        records: tuple[WorkbookRowRecord, ...] = (),
        headers: tuple[str, ...] = (),
    ) -> None:
        super().__init__()
        self._records = records
        self._headers = headers

    def set_records(self, records: tuple[WorkbookRowRecord, ...], headers: tuple[str, ...]) -> None:
        """Reemplaza los datos visibles en un único reinicio del modelo."""
        self.beginResetModel()
        self._records = records
        self._headers = headers
        self.endResetModel()

    def clear(self) -> None:
        """Limpia el modelo después de un error o antes de una nueva carga."""
        self.set_records((), ())

    def headers(self) -> tuple[str, ...]:
        """Devuelve los encabezados visibles en el orden actual del modelo."""
        return self._headers

    def record_at(self, row: int) -> WorkbookRowRecord | None:
        """Devuelve el registro de una fila fuente o None si no existe."""
        if 0 <= row < len(self._records):
            return self._records[row]
        return None

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(self._records)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        record = self._records[index.row()]
        header = self._headers[index.column()]
        value = record.values_by_column.get(header)
        return value_to_display_text(value)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal and 0 <= section < len(self._headers):
            return self._headers[section]
        if orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled


def value_to_display_text(value: Any) -> str:
    """Convierte valores de celda a texto seguro para vistas de solo lectura."""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat(sep=" ", timespec="seconds")
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _value_to_text(value: Any) -> str:
    return value_to_display_text(value)
