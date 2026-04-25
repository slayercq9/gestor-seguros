"""Controlled reader for modernized workbooks.

This service loads workbook data into memory without saving the source file,
creating reports, or printing row values. Console-facing summaries use safe
technical column identifiers unless a `GS_*` auxiliary column is detected.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from app.core.exceptions import WorkbookLoadError
from app.domain.workbook_records import (
    EXPECTED_GS_COLUMNS,
    WorkbookColumn,
    WorkbookLoadResult,
    WorkbookLoadSummary,
    WorkbookRowRecord,
)


MAIN_SHEET_NAME = "CONTROLCARTERA"


def load_modernized_workbook(input_path: str | Path) -> WorkbookLoadResult:
    """Load a modernized workbook in read-only mode and return safe metadata.

    The function does not modify, save, or create files. Real row values are
    stored only in returned in-memory records for future controlled phases.
    """
    workbook_path = _validate_workbook_path(input_path)
    workbook = load_workbook(workbook_path, read_only=True, data_only=False)
    try:
        if MAIN_SHEET_NAME not in workbook.sheetnames:
            raise WorkbookLoadError(f"No existe la hoja requerida: {MAIN_SHEET_NAME}")

        worksheet = workbook[MAIN_SHEET_NAME]
        header_row = _detect_header_row(worksheet)
        columns = _read_columns(worksheet, header_row)
        records, rows_skipped = _load_records(worksheet, header_row, columns)
        summary = _build_summary(workbook_path, worksheet, header_row, columns, records, rows_skipped)
        return WorkbookLoadResult(summary=summary, records=tuple(records))
    finally:
        workbook.close()


def _validate_workbook_path(input_path: str | Path) -> Path:
    workbook_path = Path(input_path).resolve()
    if not workbook_path.exists():
        raise WorkbookLoadError(f"No existe el workbook indicado: {workbook_path}")
    if workbook_path.suffix.lower() != ".xlsx":
        raise WorkbookLoadError("El lector controlado solo acepta archivos .xlsx.")
    return workbook_path


def _detect_header_row(worksheet: Worksheet, scan_rows: int = 50) -> int:
    """Prefer the row containing expected `GS_*` columns."""
    best_row = 1
    best_score = -1
    max_scan = min(worksheet.max_row or 1, scan_rows)
    expected = set(EXPECTED_GS_COLUMNS)

    for row_index in range(1, max_scan + 1):
        values = [str(cell.value).strip() for cell in worksheet[row_index] if cell.value is not None]
        gs_matches = sum(1 for value in values if value in expected)
        non_empty = len(values)
        score = gs_matches * 100 + non_empty
        if score > best_score:
            best_score = score
            best_row = row_index

    return best_row


def _read_columns(worksheet: Worksheet, header_row: int) -> list[WorkbookColumn]:
    expected = set(EXPECTED_GS_COLUMNS)
    header_values = [cell.value for cell in worksheet[header_row]]
    header_is_trusted = any(str(value).strip() in expected for value in header_values if value is not None)
    columns: list[WorkbookColumn] = []

    for index in range(1, (worksheet.max_column or 0) + 1):
        raw_header = header_values[index - 1] if index <= len(header_values) else None
        header_text = str(raw_header).strip() if raw_header is not None else ""
        is_gs_column = header_text in expected
        technical_name = f"COL_{get_column_letter(index)}"
        display_name = header_text if is_gs_column else technical_name
        original_header = header_text if header_is_trusted and header_text else None

        columns.append(
            WorkbookColumn(
                index=index,
                technical_name=technical_name,
                display_name=display_name,
                original_header=original_header,
                is_gs_column=is_gs_column,
            )
        )

    return columns


def _load_records(
    worksheet: Worksheet,
    header_row: int,
    columns: list[WorkbookColumn],
) -> tuple[list[WorkbookRowRecord], int]:
    records: list[WorkbookRowRecord] = []
    rows_skipped = 0

    for row_number, row in enumerate(
        worksheet.iter_rows(
            min_row=header_row + 1,
            max_row=worksheet.max_row,
            max_col=worksheet.max_column,
            values_only=True,
        ),
        start=header_row + 1,
    ):
        if not _row_has_values(row):
            rows_skipped += 1
            continue

        values_by_column: dict[str, Any] = {}
        gs_values: dict[str, Any] = {}
        for column, value in zip(columns, row, strict=False):
            values_by_column[column.technical_name] = value
            if column.is_gs_column:
                gs_values[column.display_name] = value

        records.append(
            WorkbookRowRecord(
                row_number=row_number,
                values_by_column=values_by_column,
                gs_values=gs_values,
            )
        )

    return records, rows_skipped


def _build_summary(
    workbook_path: Path,
    worksheet: Worksheet,
    header_row: int,
    columns: list[WorkbookColumn],
    records: list[WorkbookRowRecord],
    rows_skipped: int,
) -> WorkbookLoadSummary:
    present = tuple(column.display_name for column in columns if column.is_gs_column)
    missing = tuple(column for column in EXPECTED_GS_COLUMNS if column not in present)
    warnings = _build_warnings(missing)

    return WorkbookLoadSummary(
        source_name=workbook_path.name,
        sheet_name=worksheet.title,
        header_row=header_row,
        total_rows=worksheet.max_row or 0,
        total_columns=worksheet.max_column or 0,
        data_rows_detected=max((worksheet.max_row or header_row) - header_row, 0),
        records_loaded=len(records),
        rows_skipped=rows_skipped,
        detected_columns=tuple(column.display_name for column in columns),
        gs_columns_present=present,
        gs_columns_missing=missing,
        structure_complete=not missing,
        warnings=warnings,
    )


def _build_warnings(missing_gs_columns: tuple[str, ...]) -> tuple[str, ...]:
    warnings = [
        "Carga de solo lectura; no se modifico ni guardo el workbook.",
        "Los registros quedan solo en memoria para fases futuras.",
    ]
    if missing_gs_columns:
        warnings.append("Estructura incompleta: faltan columnas auxiliares GS_*.")
    return tuple(warnings)


def _row_has_values(row: tuple[Any, ...]) -> bool:
    return any(value is not None and (not isinstance(value, str) or value.strip() != "") for value in row)
