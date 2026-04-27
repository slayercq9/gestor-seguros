"""Internal records returned by the controlled workbook loader.

The structures keep workbook row values in memory for the GUI. Console and
documentation-facing summaries remain structural and avoid row samples.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class WorkbookColumn:
    """Column metadata with a safe technical name for reporting."""

    index: int
    technical_name: str
    display_name: str
    original_header: str | None


@dataclass(frozen=True)
class WorkbookRowRecord:
    """Preliminary in-memory representation of one loaded workbook row."""

    row_number: int
    values_by_column: Mapping[str, Any]


@dataclass(frozen=True)
class WorkbookLoadSummary:
    """Safe technical summary of a workbook load."""

    source_name: str
    sheet_name: str
    header_row: int
    total_rows: int
    total_columns: int
    useful_rows_detected: int
    records_loaded: int
    rows_skipped: int
    detected_columns: tuple[str, ...]
    visible_columns: tuple[str, ...]
    read_only: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class WorkbookLoadResult:
    """Records and safe summary returned by the controlled loader."""

    summary: WorkbookLoadSummary
    records: tuple[WorkbookRowRecord, ...]
