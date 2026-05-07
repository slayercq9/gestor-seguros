"""Modelo Qt de solo lectura para la bitácora en memoria."""

from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from app.domain.audit_log import AuditEntry


AUDIT_TABLE_HEADERS = (
    "Fecha y hora",
    "Registro",
    "Campo",
    "Valor anterior",
    "Valor nuevo",
    "Origen",
    "Estado",
)


class AuditTableModel(QAbstractTableModel):
    """Expone entradas de bitácora de sesión sin permitir edición."""

    def __init__(self, entries: tuple[AuditEntry, ...] = ()) -> None:
        super().__init__()
        self._entries: list[AuditEntry] = list(entries)

    def add_entries(self, entries: tuple[AuditEntry, ...]) -> None:
        """Agrega entradas nuevas al final de la bitácora."""
        if not entries:
            return
        start_row = len(self._entries)
        end_row = start_row + len(entries) - 1
        self.beginInsertRows(QModelIndex(), start_row, end_row)
        self._entries.extend(entries)
        self.endInsertRows()

    def clear(self) -> None:
        """Limpia la bitácora de la sesión actual."""
        self.beginResetModel()
        self._entries = []
        self.endResetModel()

    def entries(self) -> tuple[AuditEntry, ...]:
        """Devuelve una copia inmutable de las entradas registradas."""
        return tuple(self._entries)

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(self._entries)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(AUDIT_TABLE_HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        entry = self._entries[index.row()]
        values = (
            entry.changed_at.strftime("%Y-%m-%d %H:%M:%S"),
            entry.record_label,
            entry.field_name,
            entry.previous_value,
            entry.new_value,
            entry.origin,
            entry.status,
        )
        return values[index.column()]

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal and 0 <= section < len(AUDIT_TABLE_HEADERS):
            return AUDIT_TABLE_HEADERS[section]
        if orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
