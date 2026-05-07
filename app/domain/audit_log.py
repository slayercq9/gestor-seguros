"""Contratos para bitácoras de cambios mantenidas solo en memoria."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


AUDIT_ORIGIN_MANUAL_EDIT = "Edición manual en app"
AUDIT_STATUS_PENDING_SAVE = "Pendiente de guardado"


@dataclass(frozen=True)
class RecordFieldChange:
    """Cambio real detectado sobre un campo visible de un registro."""

    field_name: str
    previous_value: str
    new_value: str


@dataclass(frozen=True)
class AuditEntry:
    """Entrada de bitácora de sesión para un cambio aplicado en memoria."""

    changed_at: datetime
    record_number: int
    field_name: str
    previous_value: str
    new_value: str
    origin: str = AUDIT_ORIGIN_MANUAL_EDIT
    status: str = AUDIT_STATUS_PENDING_SAVE

    @property
    def record_label(self) -> str:
        """Etiqueta técnica legible del registro modificado."""
        return f"Fila {self.record_number}"


def build_audit_entries(
    record_number: int,
    changes: Iterable[RecordFieldChange],
    changed_at: datetime | None = None,
) -> tuple[AuditEntry, ...]:
    """Crea entradas de bitácora solo para cambios reales."""
    timestamp = changed_at or datetime.now()
    return tuple(
        AuditEntry(
            changed_at=timestamp,
            record_number=record_number,
            field_name=change.field_name,
            previous_value=change.previous_value,
            new_value=change.new_value,
        )
        for change in changes
        if change.previous_value != change.new_value
    )
