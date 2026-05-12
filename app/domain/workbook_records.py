"""Registros internos devueltos por el lector controlado del Control Cartera.

Las estructuras mantienen valores de filas en memoria para la GUI. Los
resúmenes para consola y documentación son estructurales y evitan muestras de filas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class WorkbookColumn:
    """Metadatos de columna con un nombre técnico seguro para reportes."""

    index: int
    technical_name: str
    display_name: str
    original_header: str | None


@dataclass(frozen=True)
class WorkbookRowRecord:
    """Representación preliminar en memoria de una fila cargada."""

    row_number: int
    values_by_column: Mapping[str, Any]


@dataclass(frozen=True)
class WorkbookLoadSummary:
    """Resumen técnico seguro de una carga del Control Cartera."""

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
    column_indexes_by_name: Mapping[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkbookLoadResult:
    """Registros y resumen seguro devueltos por el lector controlado."""

    summary: WorkbookLoadSummary
    records: tuple[WorkbookRowRecord, ...]
