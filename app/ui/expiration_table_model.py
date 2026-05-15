"""Modelo de solo lectura para la vista inicial de vencimientos."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Mapping

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from app.domain.column_standards import (
    EMAIL,
    INSURED_NAME,
    PHONE,
    POLICY_NUMBER,
    POLICY_TYPE,
    PREMIUM,
    TERM,
    format_display_value,
    resolve_column_key,
)
from app.domain.policy_expirations import (
    STATUS_ACTIVE,
    STATUS_EXPIRED,
    STATUS_EXPIRING_SOON,
    STATUS_INVALID_DATE,
    STATUS_NOTICE_NOT_APPLICABLE,
    classify_policy_expiration,
)
from app.domain.workbook_records import WorkbookRowRecord


EXPIRATION_TABLE_HEADERS = (
    "Nº Póliza",
    "Nombre del asegurado",
    "Tipo de póliza",
    "Vigencia",
    "Fecha de vencimiento",
    "Estado",
    "Días restantes",
    "Prima",
    "Teléfono",
    "Correo",
)

_STATUS_LABELS = {
    STATUS_ACTIVE: "Vigente",
    STATUS_EXPIRING_SOON: "Próxima a vencer",
    STATUS_EXPIRED: "Vencida",
    STATUS_INVALID_DATE: "Sin fecha válida",
    STATUS_NOTICE_NOT_APPLICABLE: "No aplica aviso",
}


@dataclass(frozen=True)
class ExpirationTableRow:
    """Fila presentada en la tabla de vencimientos."""

    policy_number: str
    insured_name: str
    policy_type: str
    term: str
    due_date: str
    status: str
    days_remaining: str
    premium: str
    phone: str
    email: str


@dataclass(frozen=True)
class ExpirationSummary:
    """Resumen agregado de estados de vencimiento."""

    total: int
    active: int
    expiring_soon: int
    expired: int
    invalid_date: int
    notice_not_applicable: int


def build_expiration_rows(
    records: tuple[WorkbookRowRecord, ...],
    reference_date: date | None = None,
    alert_days: int = 30,
) -> tuple[ExpirationTableRow, ...]:
    """Construye filas visuales usando la lógica de dominio de vencimientos."""
    rows: list[ExpirationTableRow] = []
    for record in records:
        values = _values_by_key(record.values_by_column)
        evaluation = classify_policy_expiration(record.values_by_column, reference_date=reference_date, alert_days=alert_days)
        due_date = _due_date_text(evaluation.status, evaluation.due_date)
        days_remaining = "-" if evaluation.due_date is None else str((evaluation.due_date - evaluation.reference_date).days)
        rows.append(
            ExpirationTableRow(
                policy_number=_display_value(values, POLICY_NUMBER),
                insured_name=_display_value(values, INSURED_NAME),
                policy_type=_display_value(values, POLICY_TYPE),
                term=_display_value(values, TERM),
                due_date=due_date,
                status=_STATUS_LABELS[evaluation.status],
                days_remaining=days_remaining,
                premium=_display_value(values, PREMIUM),
                phone=_display_value(values, PHONE),
                email=_display_value(values, EMAIL),
            )
        )
    return tuple(rows)


def summarize_expiration_rows(rows: tuple[ExpirationTableRow, ...]) -> ExpirationSummary:
    """Cuenta estados de vencimiento ya adaptados para la vista."""
    return ExpirationSummary(
        total=len(rows),
        active=sum(row.status == "Vigente" for row in rows),
        expiring_soon=sum(row.status == "Próxima a vencer" for row in rows),
        expired=sum(row.status == "Vencida" for row in rows),
        invalid_date=sum(row.status == "Sin fecha válida" for row in rows),
        notice_not_applicable=sum(row.status == "No aplica aviso" for row in rows),
    )


class ExpirationTableModel(QAbstractTableModel):
    """Expone vencimientos calculados sin permitir edición."""

    def __init__(self, rows: tuple[ExpirationTableRow, ...] = ()) -> None:
        super().__init__()
        self._rows = rows

    def set_rows(self, rows: tuple[ExpirationTableRow, ...]) -> None:
        """Reemplaza las filas evaluadas."""
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        if parent and parent.isValid():
            return 0
        return len(EXPIRATION_TABLE_HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid() or role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
            return None
        row = self._rows[index.row()]
        return (
            row.policy_number,
            row.insured_name,
            row.policy_type,
            row.term,
            row.due_date,
            row.status,
            row.days_remaining,
            row.premium,
            row.phone,
            row.email,
        )[index.column()]

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
            return None
        if orientation == Qt.Orientation.Horizontal and 0 <= section < len(EXPIRATION_TABLE_HEADERS):
            return EXPIRATION_TABLE_HEADERS[section]
        if orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled


def _values_by_key(values_by_column: Mapping[str, object]) -> dict[str, object]:
    values: dict[str, object] = {}
    for header, value in values_by_column.items():
        key = resolve_column_key(header)
        if key is not None and key not in values:
            values[key] = value
    return values


def _display_value(values_by_key: Mapping[str, object], key: str) -> str:
    return format_display_value(key, values_by_key.get(key)).strip()


def _due_date_text(status: str, due_date: date | None) -> str:
    if status == STATUS_NOTICE_NOT_APPLICABLE:
        return "No aplica aviso"
    if due_date is None:
        return "Sin fecha válida"
    return due_date.isoformat()
