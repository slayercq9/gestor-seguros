"""Internal records returned by the controlled workbook loader.

The structures in this module keep workbook row values in memory for later
phases, while summaries and display names remain safe for console output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EXPECTED_GS_COLUMNS = (
    "GS_FRECUENCIA_OBSERVADA",
    "GS_ES_DM",
    "GS_GENERA_AVISO_PRELIMINAR",
    "GS_PATRON_POLIZA",
    "GS_MONEDA_PRELIMINAR",
    "GS_TIPO_IDENTIFICACION_PROBABLE",
    "GS_FECHA_VENCIMIENTO_TECNICA",
    "GS_REQUIERE_REVISION",
    "GS_MOTIVO_REVISION",
)


@dataclass(frozen=True)
class WorkbookColumn:
    """Column metadata with a safe technical name for reporting."""

    index: int
    technical_name: str
    display_name: str
    original_header: str | None
    is_gs_column: bool


@dataclass(frozen=True)
class WorkbookRowRecord:
    """Preliminary in-memory representation of one loaded workbook row."""

    row_number: int
    values_by_column: Mapping[str, Any]
    gs_values: Mapping[str, Any]


@dataclass(frozen=True)
class WorkbookLoadSummary:
    """Safe technical summary of a workbook load."""

    source_name: str
    sheet_name: str
    header_row: int
    total_rows: int
    total_columns: int
    data_rows_detected: int
    records_loaded: int
    rows_skipped: int
    detected_columns: tuple[str, ...]
    gs_columns_present: tuple[str, ...]
    gs_columns_missing: tuple[str, ...]
    structure_complete: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class WorkbookLoadResult:
    """Records and safe summary returned by the controlled loader."""

    summary: WorkbookLoadSummary
    records: tuple[WorkbookRowRecord, ...]
