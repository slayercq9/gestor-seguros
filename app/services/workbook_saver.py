"""Guardado seguro de copias del Control Cartera.

El servicio escribe cambios aplicados en memoria sobre una copia `.xlsx`. No
sobrescribe el archivo cargado ni modifica el Excel fuente.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from openpyxl import load_workbook

from app.core.exceptions import WorkbookSaveError
from app.domain.column_standards import ISSUE_DATE, resolve_column_key
from app.services.workbook_loader import MAIN_SHEET_NAME, _detect_header_row, _read_columns


@dataclass(frozen=True)
class WorkbookCellUpdate:
    """Cambio puntual que debe escribirse en una copia del Control Cartera."""

    row_number: int
    column_name: str
    value: object


def save_control_cartera_as(
    source_path: str | Path,
    destination_path: str | Path,
    updates: Iterable[WorkbookCellUpdate],
    *,
    sheet_name: str = MAIN_SHEET_NAME,
    header_row: int | None = None,
) -> Path:
    """Guarda una copia `.xlsx` aplicando cambios de memoria.

    El archivo fuente se abre solo como plantilla de lectura/escritura en memoria
    y se guarda exclusivamente en `destination_path`.
    """
    source = _validate_source_path(source_path)
    destination = _validate_destination_path(source, destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    workbook = load_workbook(source)
    try:
        if sheet_name not in workbook.sheetnames:
            raise WorkbookSaveError(f"No existe la hoja requerida: {sheet_name}")

        worksheet = workbook[sheet_name]
        effective_header_row = header_row or _detect_header_row(worksheet)
        column_map = _column_index_by_display_name(worksheet, effective_header_row)
        for update in updates:
            if update.column_name not in column_map:
                raise WorkbookSaveError(f"No se encontro la columna para guardar: {update.column_name}")
            worksheet.cell(
                row=update.row_number,
                column=column_map[update.column_name],
                value=_value_for_save(update.column_name, update.value),
            )

        workbook.save(destination)
    finally:
        workbook.close()

    return destination


def _validate_source_path(source_path: str | Path) -> Path:
    source = Path(source_path).resolve()
    if not source.exists() or not source.is_file():
        raise WorkbookSaveError("El archivo fuente no existe.")
    if source.suffix.lower() != ".xlsx":
        raise WorkbookSaveError("El archivo fuente debe tener extension .xlsx.")
    return source


def _validate_destination_path(source: Path, destination_path: str | Path) -> Path:
    destination = Path(destination_path).resolve()
    if destination.suffix.lower() != ".xlsx":
        raise WorkbookSaveError("La ruta de destino debe tener extension .xlsx.")
    if destination == source:
        raise WorkbookSaveError("Guardar como no puede sobrescribir el archivo cargado.")
    return destination


def _column_index_by_display_name(worksheet: object, header_row: int) -> dict[str, int]:
    columns = _read_columns(worksheet, header_row)
    return {column.display_name: column.index for column in columns}


def _value_for_save(column_name: str, value: object) -> object:
    if resolve_column_key(column_name) != ISSUE_DATE:
        return value
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})(?:[ T].*)?", text)
    if match:
        return match.group(1)
    return text
