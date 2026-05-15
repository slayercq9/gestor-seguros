from datetime import date

from PySide6.QtCore import Qt

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.expiration_table_model import (
    ExpirationTableModel,
    build_expiration_rows,
    summarize_expiration_rows,
)


REFERENCE_DATE = date(2026, 5, 15)


def build_records() -> tuple[WorkbookRowRecord, ...]:
    return (
        WorkbookRowRecord(
            row_number=2,
            values_by_column={
                "Poliza": "01-ACTIVA",
                "Nombre": "Persona Vigente",
                "Tipo": "Auto",
                "Vigencia": "Anual",
                "Dia": "30",
                "Mes": "6",
                "Ano": "2026",
                "Prima": "1000",
                "Telefono": "8888-0001",
                "Correo": "vigente@example.test",
            },
        ),
        WorkbookRowRecord(
            row_number=3,
            values_by_column={
                "Poliza": "01-PROXIMA",
                "Nombre": "Persona Proxima",
                "Tipo": "Incendio",
                "Vigencia": "Mensual",
                "Dia": "30",
                "Mes": "5",
                "Ano": "2026",
                "Prima": "2000",
                "Telefono": "8888-0002",
                "Correo": "proxima@example.test",
            },
        ),
        WorkbookRowRecord(
            row_number=4,
            values_by_column={
                "Poliza": "01-VENCIDA",
                "Nombre": "Persona Vencida",
                "Tipo": "Vida",
                "Vigencia": "Trimestral",
                "Dia": "14",
                "Mes": "5",
                "Ano": "2026",
                "Prima": "3000",
                "Telefono": "8888-0003",
                "Correo": "vencida@example.test",
            },
        ),
        WorkbookRowRecord(
            row_number=5,
            values_by_column={
                "Poliza": "01-INVALIDA",
                "Nombre": "Persona Sin Fecha",
                "Tipo": "Otro",
                "Vigencia": "Anual",
                "Dia": "31",
                "Mes": "2",
                "Ano": "2026",
                "Prima": "",
                "Telefono": "",
                "Correo": "",
            },
        ),
        WorkbookRowRecord(
            row_number=6,
            values_by_column={
                "Poliza": "01-DM",
                "Nombre": "Persona DM",
                "Tipo": "Deduccion",
                "Vigencia": "D.M.",
                "Dia": "",
                "Mes": "",
                "Ano": "",
                "Prima": "5000",
                "Telefono": "8888-0005",
                "Correo": "dm@example.test",
            },
        ),
    )


def test_build_expiration_rows_uses_domain_statuses() -> None:
    rows = build_expiration_rows(build_records(), reference_date=REFERENCE_DATE, alert_days=30)

    assert [row.status for row in rows] == [
        "Vigente",
        "Próxima a vencer",
        "Vencida",
        "Sin fecha válida",
        "No aplica aviso",
    ]
    assert rows[0].due_date == "2026-06-30"
    assert rows[1].days_remaining == "15"
    assert rows[2].days_remaining == "-1"
    assert rows[3].due_date == "Sin fecha válida"
    assert rows[4].due_date == "No aplica aviso"


def test_summarize_expiration_rows_counts_all_statuses() -> None:
    rows = build_expiration_rows(build_records(), reference_date=REFERENCE_DATE, alert_days=30)
    summary = summarize_expiration_rows(rows)

    assert summary.total == 5
    assert summary.active == 1
    assert summary.expiring_soon == 1
    assert summary.expired == 1
    assert summary.invalid_date == 1
    assert summary.notice_not_applicable == 1


def test_expiration_table_model_is_read_only() -> None:
    rows = build_expiration_rows(build_records(), reference_date=REFERENCE_DATE, alert_days=30)
    model = ExpirationTableModel(rows)

    assert model.rowCount() == 5
    assert model.columnCount() == 10
    assert model.headerData(0, Qt.Orientation.Horizontal) == "Nº Póliza"
    assert model.data(model.index(0, 0)) == "01-ACTIVA"
    assert model.data(model.index(1, 5)) == "Próxima a vencer"
    assert model.data(model.index(3, 4), Qt.ItemDataRole.ToolTipRole) == "Sin fecha válida"
    assert model.flags(model.index(0, 0)) == (Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
