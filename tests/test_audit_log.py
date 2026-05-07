from datetime import datetime

from app.domain.audit_log import (
    AUDIT_ORIGIN_MANUAL_EDIT,
    AUDIT_STATUS_PENDING_SAVE,
    RecordFieldChange,
    build_audit_entries,
)


def test_bitacora_crea_entrada_con_fecha_origen_y_estado():
    timestamp = datetime(2026, 5, 7, 10, 30, 0)

    entries = build_audit_entries(
        12,
        (RecordFieldChange("Cliente", "Valor anterior", "Valor nuevo"),),
        changed_at=timestamp,
    )

    assert len(entries) == 1
    assert entries[0].changed_at == timestamp
    assert entries[0].record_number == 12
    assert entries[0].record_label == "Fila 12"
    assert entries[0].field_name == "Cliente"
    assert entries[0].previous_value == "Valor anterior"
    assert entries[0].new_value == "Valor nuevo"
    assert entries[0].origin == AUDIT_ORIGIN_MANUAL_EDIT
    assert entries[0].status == AUDIT_STATUS_PENDING_SAVE


def test_bitacora_no_registra_cambios_inexistentes():
    entries = build_audit_entries(
        8,
        (
            RecordFieldChange("Cliente", "Sin cambio", "Sin cambio"),
            RecordFieldChange("Correo", "", "correo@example.test"),
        ),
        changed_at=datetime(2026, 5, 7, 10, 30, 0),
    )

    assert len(entries) == 1
    assert entries[0].field_name == "Correo"
