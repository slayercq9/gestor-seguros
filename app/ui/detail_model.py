"""Modelo Qt de solo lectura para el detalle de un registro seleccionado."""

from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.table_model import value_to_display_text


class RecordDetailModel(QAbstractTableModel):
    """Expone campos y valores de un registro seleccionado sin permitir edición."""

    def __init__(self) -> None:
        super().__init__()
        self._rows: tuple[tuple[str, str], ...] = ()

    def set_record(self, record: WorkbookRowRecord, headers: tuple[str, ...]) -> None:
        """Carga solo campos con información siguiendo el orden visible de la tabla."""
        rows: list[tuple[str, str]] = []
        for header in headers:
            value = value_to_display_text(record.values_by_column.get(header), header).strip()
            if value and value != "—":
                rows.append((header, value))

        self.beginResetModel()
        self._rows = tuple(rows)
        self.endResetModel()

    def clear(self) -> None:
        """Limpia el detalle cuando no hay selección válida."""
        self.beginResetModel()
        self._rows = ()
        self.endResetModel()

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return 2

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        return self._rows[index.row()][index.column()]

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return ("Campo", "Valor")[section] if section in (0, 1) else None
        if orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
