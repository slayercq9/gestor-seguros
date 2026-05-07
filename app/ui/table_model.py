"""Modelo de tabla Qt de solo lectura para registros cargados del Control Cartera."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Mapping

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from app.domain.audit_log import RecordFieldChange
from app.domain.workbook_records import WorkbookRowRecord


class RecordsTableModel(QAbstractTableModel):
    """Expone los registros cargados a Qt sin permitir edición."""

    def __init__(
        self,
        records: tuple[WorkbookRowRecord, ...] = (),
        headers: tuple[str, ...] = (),
    ) -> None:
        super().__init__()
        self._records: list[WorkbookRowRecord] = []
        self._headers = headers
        self._original_values: dict[tuple[int, str], str] = {}
        self._changed_cells: set[tuple[int, str]] = set()
        self._set_records_without_reset(records, headers)

    def set_records(self, records: tuple[WorkbookRowRecord, ...], headers: tuple[str, ...]) -> None:
        """Reemplaza los datos visibles en un único reinicio del modelo."""
        self.beginResetModel()
        self._set_records_without_reset(records, headers)
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

    def update_record(self, row: int, values_by_column: Mapping[str, str]) -> bool:
        """Actualiza una fila en memoria sin habilitar edición directa en la tabla."""
        record = self.record_at(row)
        if record is None:
            return False

        updated_values = dict(record.values_by_column)
        changed_columns: list[int] = []
        changes = self.preview_update_changes(row, values_by_column)
        changed_fields = {change.field_name for change in changes}
        for column_index, header in enumerate(self._headers):
            if header not in changed_fields:
                self._update_pending_marker(row, header, value_to_display_text(updated_values.get(header)))
                continue
            new_value = values_by_column[header].strip()
            updated_values[header] = new_value
            changed_columns.append(column_index)
            self._update_pending_marker(row, header, new_value)

        if not changed_columns:
            return False

        self._records[row] = WorkbookRowRecord(row_number=record.row_number, values_by_column=updated_values)
        self.dataChanged.emit(
            self.index(row, min(changed_columns)),
            self.index(row, max(changed_columns)),
            [Qt.ItemDataRole.DisplayRole],
        )
        return True

    def preview_update_changes(self, row: int, values_by_column: Mapping[str, str]) -> tuple[RecordFieldChange, ...]:
        """Calcula cambios reales sin modificar el modelo."""
        record = self.record_at(row)
        if record is None:
            return ()

        changes: list[RecordFieldChange] = []
        for header in self._headers:
            if header not in values_by_column:
                continue
            previous_value = value_to_display_text(record.values_by_column.get(header))
            new_value = values_by_column[header].strip()
            if previous_value == new_value:
                continue
            changes.append(
                RecordFieldChange(
                    field_name=header,
                    previous_value=previous_value,
                    new_value=new_value,
                )
            )
        return tuple(changes)

    def has_pending_changes(self) -> bool:
        """Indica si hay cambios en memoria sin guardar."""
        return bool(self._changed_cells)

    def pending_changes_count(self) -> int:
        """Cuenta campos modificados en memoria."""
        return len(self._changed_cells)

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

    def _set_records_without_reset(self, records: tuple[WorkbookRowRecord, ...], headers: tuple[str, ...]) -> None:
        self._records = [_copy_record(record) for record in records]
        self._headers = headers
        self._changed_cells = set()
        self._original_values = {
            (row, header): value_to_display_text(record.values_by_column.get(header))
            for row, record in enumerate(self._records)
            for header in self._headers
        }

    def _update_pending_marker(self, row: int, header: str, new_value: str) -> None:
        cell_key = (row, header)
        if self._original_values.get(cell_key, "") == new_value:
            self._changed_cells.discard(cell_key)
        else:
            self._changed_cells.add(cell_key)


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


def _copy_record(record: WorkbookRowRecord) -> WorkbookRowRecord:
    return WorkbookRowRecord(row_number=record.row_number, values_by_column=dict(record.values_by_column))
