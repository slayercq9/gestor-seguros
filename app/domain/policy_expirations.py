"""Cálculo base de vencimientos de pólizas del Control Cartera.

La lógica de este módulo es pura: no lee Excel, no escribe archivos y no
depende de la interfaz. Trabaja con encabezados originales o alias soportados
por el registro central de columnas.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Mapping

from app.domain.column_standards import DUE_DAY, DUE_MONTH, DUE_YEAR, TERM, resolve_column_key
from app.domain.workbook_rules import normalize_text, safe_text


STATUS_ACTIVE = "vigente"
STATUS_EXPIRING_SOON = "próxima a vencer"
STATUS_EXPIRED = "vencida"
STATUS_INVALID_DATE = "sin fecha válida"
STATUS_NOTICE_NOT_APPLICABLE = "no aplica aviso"

DISPLAY_STATUS_BY_KEY = {
    STATUS_ACTIVE: "vigente",
    STATUS_EXPIRING_SOON: "próxima a vencer",
    STATUS_EXPIRED: "vencida",
    STATUS_INVALID_DATE: "sin fecha válida",
    STATUS_NOTICE_NOT_APPLICABLE: "no aplica aviso",
}


@dataclass(frozen=True)
class ExpirationEvaluation:
    """Resultado de clasificar el vencimiento de una póliza."""

    status: str
    due_date: date | None
    reference_date: date
    alert_days: int
    message: str

    @property
    def display_status(self) -> str:
        """Etiqueta legible del estado calculado."""
        return DISPLAY_STATUS_BY_KEY[self.status]


def calculate_due_date(values_by_column: Mapping[str, object]) -> date | None:
    """Construye la fecha de vencimiento desde DÍA, MES y AÑO si es válida."""
    values = _values_by_key(values_by_column)
    day = _parse_positive_int(values.get(DUE_DAY))
    month = _parse_positive_int(values.get(DUE_MONTH))
    year = _parse_year(values.get(DUE_YEAR))
    if day is None or month is None or year is None:
        return None
    try:
        return date(year, month, day)
    except ValueError:
        return None


def classify_policy_expiration(
    values_by_column: Mapping[str, object],
    reference_date: date | None = None,
    alert_days: int = 30,
) -> ExpirationEvaluation:
    """Clasifica el estado de vencimiento de una póliza cargada en memoria."""
    if alert_days < 0:
        raise ValueError("alert_days no puede ser negativo.")

    active_reference_date = reference_date or date.today()
    values = _values_by_key(values_by_column)
    term = safe_text(values.get(TERM))
    if _is_dm_term(term):
        return ExpirationEvaluation(
            status=STATUS_NOTICE_NOT_APPLICABLE,
            due_date=None,
            reference_date=active_reference_date,
            alert_days=alert_days,
            message="La vigencia D.M. no requiere aviso de vencimiento.",
        )

    due_date = calculate_due_date(values_by_column)
    if due_date is None:
        return ExpirationEvaluation(
            status=STATUS_INVALID_DATE,
            due_date=None,
            reference_date=active_reference_date,
            alert_days=alert_days,
            message="No hay fecha de vencimiento válida.",
        )

    if due_date < active_reference_date:
        status = STATUS_EXPIRED
        message = "La póliza está vencida."
    elif due_date <= active_reference_date + timedelta(days=alert_days):
        status = STATUS_EXPIRING_SOON
        message = "La póliza está próxima a vencer."
    else:
        status = STATUS_ACTIVE
        message = "La póliza está vigente."

    return ExpirationEvaluation(
        status=status,
        due_date=due_date,
        reference_date=active_reference_date,
        alert_days=alert_days,
        message=message,
    )


def _values_by_key(values_by_column: Mapping[str, object]) -> dict[str, object]:
    values: dict[str, object] = {}
    for column_name, value in values_by_column.items():
        key = resolve_column_key(column_name)
        if key is not None and key not in values:
            values[key] = value
    return values


def _is_dm_term(value: object) -> bool:
    normalized = normalize_text(value).replace(" ", "")
    return normalized in {"dm", "dms"} or normalize_text(value) == "deduccion mensual"


def _parse_positive_int(value: object) -> int | None:
    text = safe_text(value)
    if not text.isdigit():
        return None
    return int(text)


def _parse_year(value: object) -> int | None:
    text = safe_text(value)
    if not text.isdigit() or len(text) != 4:
        return None
    return int(text)
