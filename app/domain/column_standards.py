"""Estándares funcionales de columnas del Control Cartera.

La fase 1.10.2 usa estos metadatos solo para decidir visibilidad de columnas.
No valida, corrige, elimina ni transforma valores del Excel.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.workbook_rules import normalize_text


@dataclass(frozen=True)
class ColumnVisibility:
    """Clasificación mínima de visibilidad para una columna cargada."""

    display_name: str
    is_coverage: bool
    visible_in_table: bool
    visible_in_detail: bool
    visible_in_edit: bool
    searchable: bool


def is_coverage_column(column_name: object) -> bool:
    """Identifica columnas de coberturas con criterio conservador."""
    normalized = normalize_text(column_name)
    return "cobertura" in normalized


def get_column_visibility(column_name: object) -> ColumnVisibility:
    """Devuelve la visibilidad vigente de una columna del Control Cartera."""
    display_name = "" if column_name is None else str(column_name)
    is_coverage = is_coverage_column(display_name)
    return ColumnVisibility(
        display_name=display_name,
        is_coverage=is_coverage,
        visible_in_table=not is_coverage,
        visible_in_detail=not is_coverage,
        visible_in_edit=not is_coverage,
        searchable=not is_coverage,
    )


def visible_column_names(column_names: tuple[str, ...]) -> tuple[str, ...]:
    """Filtra columnas visibles sin eliminar datos cargados en memoria."""
    return tuple(
        column_name
        for column_name in column_names
        if get_column_visibility(column_name).visible_in_table
    )
