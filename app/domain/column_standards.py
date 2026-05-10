"""Registro central de columnas del Control Cartera.

Este módulo concentra alias, claves canónicas, visibilidad, editabilidad y
formato visual. No elimina encabezados originales ni modifica valores cargados.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from app.domain.workbook_rules import normalize_text


POLICY_NUMBER = "policy_number"
INSURED_NAME = "insured_name"
IDENTIFICATION = "identification"
PLATE_OR_PROPERTY = "plate_or_property"
ISSUE_DATE = "issue_date"
TERM = "term"
DUE_DAY = "due_day"
DUE_MONTH = "due_month"
DUE_YEAR = "due_year"
INSURED_AMOUNT = "insured_amount"
PREMIUM = "premium"
PHONE = "phone"
EMAIL = "email"
POLICY_TYPE = "policy_type"
DETAIL = "detail"
COVERAGE = "coverage"


@dataclass(frozen=True)
class ColumnDefinition:
    """Metadatos internos para una columna conocida."""

    key: str
    label: str
    aliases: tuple[str, ...]
    required: bool = False
    editable: bool = True
    visible: bool = True
    searchable: bool = True
    special_date: bool = False
    control: str = "text"


@dataclass(frozen=True)
class ColumnVisibility:
    """Clasificación mínima de visibilidad para una columna cargada."""

    display_name: str
    is_coverage: bool
    visible_in_table: bool
    visible_in_detail: bool
    visible_in_edit: bool
    searchable: bool


_COLUMN_DEFINITIONS: tuple[ColumnDefinition, ...] = (
    ColumnDefinition(POLICY_NUMBER, "Nº Póliza", ("Nº Póliza", "No Póliza", "N° Póliza", "Numero Poliza", "Número Póliza", "Póliza", "Poliza"), required=True),
    ColumnDefinition(INSURED_NAME, "Nombre del Asegurado", ("Nombre del Asegurado", "Asegurado", "Cliente", "Nombre", "Nombre Cliente"), required=True),
    ColumnDefinition(IDENTIFICATION, "Cédula", ("Cédula", "Cedula", "Identificación", "Identificacion", "ID")),
    ColumnDefinition(PLATE_OR_PROPERTY, "Nº Placa / Finca", ("Nº Placa / Finca", "Placa", "Finca", "Nº Placa", "No Placa", "Placa / Finca")),
    ColumnDefinition(ISSUE_DATE, "Emisión", ("Emisión", "Emision", "Fecha Emisión", "Fecha Emision"), special_date=True),
    ColumnDefinition(TERM, "Vigencia", ("Vigencia", "Frecuencia", "Periodicidad"), required=True, control="combo"),
    ColumnDefinition(DUE_DAY, "DÍA", ("DÍA", "DIA", "Día", "Dia"), control="combo"),
    ColumnDefinition(DUE_MONTH, "MES", ("MES", "Mes"), control="combo"),
    ColumnDefinition(DUE_YEAR, "AÑO", ("AÑO", "ANO", "Año", "Ano")),
    ColumnDefinition(INSURED_AMOUNT, "Monto Asegurado", ("Monto Asegurado", "Suma Asegurada", "Monto", "Valor Asegurado")),
    ColumnDefinition(PREMIUM, "Prima", ("Prima", "Monto Prima")),
    ColumnDefinition(PHONE, "Teléfono", ("Teléfono", "Telefono", "Tel", "Celular")),
    ColumnDefinition(EMAIL, "Correo", ("Correo", "Email", "E-mail", "Correo Electrónico", "Correo Electronico")),
    ColumnDefinition(POLICY_TYPE, "Tipo de Póliza", ("Tipo de Póliza", "Tipo de Poliza", "Tipo", "Ramo")),
    ColumnDefinition(DETAIL, "Detalle", ("Detalle", "Observaciones", "Nota", "Notas"), control="multiline"),
)

_DEFINITIONS_BY_KEY = {definition.key: definition for definition in _COLUMN_DEFINITIONS}
_ALIASES_BY_NORMALIZED_HEADER = {
    normalize_text(alias): definition.key
    for definition in _COLUMN_DEFINITIONS
    for alias in definition.aliases
}


def normalize_header(text: object) -> str:
    """Normaliza encabezados para resolver alias sin cambiar el origen."""
    return normalize_text(text)


def resolve_column_key(header_or_key: object) -> str | None:
    """Resuelve una clave canónica a partir de un encabezado, alias o clave."""
    text = "" if header_or_key is None else str(header_or_key)
    if text in _DEFINITIONS_BY_KEY:
        return text
    if is_coverage_column(text):
        return COVERAGE
    return _ALIASES_BY_NORMALIZED_HEADER.get(normalize_header(text))


def get_column_label(header_or_key: object) -> str:
    """Devuelve la etiqueta principal para una clave o conserva el encabezado."""
    key = resolve_column_key(header_or_key)
    if key in _DEFINITIONS_BY_KEY:
        return _DEFINITIONS_BY_KEY[key].label
    return "" if header_or_key is None else str(header_or_key)


def is_coverage_column(column_name: object) -> bool:
    """Identifica columnas de coberturas con criterio conservador."""
    normalized = normalize_header(column_name)
    return "cobertura" in normalized or "coberturas" in normalized


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


def is_visible_column(header_or_key: object) -> bool:
    """Indica si una columna debe aparecer en el flujo visible."""
    return get_column_visibility(header_or_key).visible_in_table


def get_visible_columns(headers: tuple[str, ...]) -> tuple[str, ...]:
    """Filtra columnas visibles sin eliminar datos cargados en memoria."""
    return tuple(header for header in headers if is_visible_column(header))


def visible_column_names(column_names: tuple[str, ...]) -> tuple[str, ...]:
    """Compatibilidad con llamadas existentes a columnas visibles."""
    return get_visible_columns(column_names)


def get_editable_columns(headers: tuple[str, ...]) -> tuple[str, ...]:
    """Filtra columnas editables según los estándares vigentes."""
    return tuple(header for header in headers if get_column_visibility(header).visible_in_edit)


def get_required_columns() -> tuple[str, ...]:
    """Devuelve claves canónicas obligatorias."""
    return tuple(definition.key for definition in _COLUMN_DEFINITIONS if definition.required)


def is_required_column(header_or_key: object) -> bool:
    """Indica si una columna corresponde a un campo obligatorio."""
    key = resolve_column_key(header_or_key)
    return key in get_required_columns()


def is_special_date_column(header_or_key: object) -> bool:
    """Indica si una columna requiere formato visual de fecha."""
    key = resolve_column_key(header_or_key)
    return bool(key and key in _DEFINITIONS_BY_KEY and _DEFINITIONS_BY_KEY[key].special_date)


def get_column_control(header_or_key: object) -> str:
    """Devuelve el tipo de control recomendado para edición."""
    key = resolve_column_key(header_or_key)
    if key in _DEFINITIONS_BY_KEY:
        return _DEFINITIONS_BY_KEY[key].control
    return "text"


def format_display_value(header_or_key: object, value: Any) -> str:
    """Formatea valores para visualización sin transformar el dato interno."""
    if value is None:
        return ""
    if is_special_date_column(header_or_key):
        return _issue_date_to_display_text(value)
    if isinstance(value, datetime):
        return value.isoformat(sep=" ", timespec="seconds")
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _issue_date_to_display_text(value: Any) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})[ T]00:00:00(?:\.0+)?", text)
    if match:
        return match.group(1)
    return text
