"""Validaciones de edición para campos del Control Cartera.

La validación distingue errores bloqueantes de advertencias suaves. Ninguna regla
corrige, normaliza ni guarda datos: solo decide si la edición en memoria puede
continuar o si requiere revisión del usuario.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Mapping

from app.domain.workbook_rules import normalize_text


VIGENCIA_VALUES = ("Mensual", "Trimestral", "Semestral", "Anual", "D.M.")
DAY_VALUES = tuple(str(value) for value in range(1, 32))
MONTH_VALUES = tuple(str(value) for value in range(1, 13))
YEAR_MIN = 2000
YEAR_MAX = 2100

ERROR = "error"
WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    """Problema detectado durante la validación de un campo editado."""

    field_name: str
    message: str
    severity: str = WARNING

    @property
    def is_error(self) -> bool:
        """Indica si la validación debe bloquear la aplicación del cambio."""
        return self.severity == ERROR


@dataclass(frozen=True)
class ValidationResult:
    """Resultado de validación separado en errores y advertencias."""

    issues: tuple[ValidationIssue, ...] = ()

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.is_error)

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if not issue.is_error)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)


def validate_edited_fields(values_by_column: Mapping[str, str]) -> ValidationResult:
    """Valida valores editados y separa errores bloqueantes de advertencias."""
    issues: list[ValidationIssue] = []
    normalized_values = {_normalize_column_name(column_name): _clean(value) for column_name, value in values_by_column.items()}

    _validate_required_text(values_by_column, issues)
    _validate_vigencia(values_by_column, issues)
    _validate_due_date(values_by_column, normalized_values, issues)
    _validate_money_fields(values_by_column, issues)
    _validate_soft_fields(values_by_column, issues)

    return ValidationResult(tuple(issues))


def _validate_required_text(values_by_column: Mapping[str, str], issues: list[ValidationIssue]) -> None:
    required_fields = {
        "no poliza": "El número de póliza es obligatorio.",
        "nombre del asegurado": "El nombre del asegurado es obligatorio.",
    }
    for column_name, value in values_by_column.items():
        normalized = _normalize_column_name(column_name)
        if normalized in required_fields and not _clean(value):
            issues.append(_error(column_name, required_fields[normalized]))


def _validate_vigencia(values_by_column: Mapping[str, str], issues: list[ValidationIssue]) -> None:
    column_name = _find_column(values_by_column, "vigencia")
    if column_name is None:
        return
    text = _clean(values_by_column[column_name])
    if not text:
        issues.append(_error(column_name, "La vigencia es obligatoria."))
        return
    allowed = {normalize_text(value) for value in VIGENCIA_VALUES}
    if normalize_text(text) not in allowed:
        issues.append(_error(column_name, "La vigencia debe pertenecer al catálogo permitido."))


def _validate_due_date(
    values_by_column: Mapping[str, str],
    normalized_values: Mapping[str, str],
    issues: list[ValidationIssue],
) -> None:
    day_name = _find_column(values_by_column, "dia")
    month_name = _find_column(values_by_column, "mes")
    year_name = _find_column(values_by_column, "ano")
    if day_name is None and month_name is None and year_name is None:
        return

    day = normalized_values.get("dia", "")
    month = normalized_values.get("mes", "")
    year = normalized_values.get("ano", "")
    vigencia = normalized_values.get("vigencia", "")
    is_dm = normalize_text(vigencia) == normalize_text("D.M.")

    if is_dm and not any((day, month, year)):
        return

    if not is_dm and not all((day, month, year)):
        issues.append(_error("DÍA/MES/AÑO", "DÍA, MES y AÑO son obligatorios cuando la vigencia requiere vencimiento."))
        return
    if is_dm and any((day, month, year)) and not all((day, month, year)):
        issues.append(_error("DÍA/MES/AÑO", "La fecha de vencimiento está incompleta."))
        return

    if not _is_int_between(day, 1, 31):
        issues.append(_error(day_name or "DÍA", "El día debe estar entre 1 y 31."))
        return
    if not _is_int_between(month, 1, 12):
        issues.append(_error(month_name or "MES", "El mes debe estar entre 1 y 12."))
        return
    if not re.fullmatch(r"\d{4}", year):
        issues.append(_error(year_name or "AÑO", "El año debe tener cuatro dígitos."))
        return

    try:
        date(int(year), int(month), int(day))
    except ValueError:
        issues.append(_error("DÍA/MES/AÑO", "La fecha de vencimiento no existe."))


def _validate_money_fields(values_by_column: Mapping[str, str], issues: list[ValidationIssue]) -> None:
    for column_name, value in values_by_column.items():
        if _normalize_column_name(column_name) not in {"monto asegurado", "prima"}:
            continue
        text = _clean(value)
        if text and not is_valid_money_text(text):
            issues.append(_error(column_name, "El monto tiene un formato inválido."))


def _validate_soft_fields(values_by_column: Mapping[str, str], issues: list[ValidationIssue]) -> None:
    for column_name, value in values_by_column.items():
        normalized = _normalize_column_name(column_name)
        text = _clean(value)
        if normalized == "cedula" and not text:
            issues.append(_warning(column_name, "La cédula está vacía."))
        elif normalized == "correo" and text and "@" not in text:
            issues.append(_warning(column_name, "El correo ingresado no contiene @."))
        elif normalized == "emision" and text and not _looks_like_date(text):
            issues.append(_warning(column_name, "La emisión no parece una fecha reconocible."))
        elif normalized == "telefono" and text and not _looks_like_phone(text):
            issues.append(_warning(column_name, "El teléfono contiene caracteres poco usuales."))
        elif normalized == "tipo de poliza" and not text:
            issues.append(_warning(column_name, "El tipo de póliza no debería quedar vacío."))


def is_valid_money_text(text: str) -> bool:
    """Valida formato monetario sin convertir ni normalizar el valor."""
    value = text.strip()
    if not value:
        return True
    if re.search(r"[A-Za-z]", value):
        cleaned_letters = re.sub(r"\b(CRC|USD)\b", "", value, flags=re.IGNORECASE)
        if re.search(r"[A-Za-z]", cleaned_letters):
            return False
    if re.search(r"[^\d\s.,₡$¢A-Za-z]", value):
        return False

    compact = re.sub(r"\s+", "", value)
    compact = re.sub(r"^(CRC|USD)", "", compact, flags=re.IGNORECASE)
    compact = re.sub(r"(CRC|USD)$", "", compact, flags=re.IGNORECASE)
    compact = compact.strip("₡$¢")
    if not compact or not re.fullmatch(r"\d[\d.,]*", compact):
        return False
    if ".." in compact or ",," in compact:
        return False

    separator_count = compact.count(".") + compact.count(",")
    if separator_count == 0:
        return True
    if "." in compact and "," in compact:
        return _valid_mixed_separators(compact)
    return _valid_single_separator(compact, "." if "." in compact else ",")


def _valid_mixed_separators(value: str) -> bool:
    last_dot = value.rfind(".")
    last_comma = value.rfind(",")
    decimal_separator = "." if last_dot > last_comma else ","
    thousands_separator = "," if decimal_separator == "." else "."
    integer_part, decimal_part = value.rsplit(decimal_separator, 1)
    if not decimal_part.isdigit() or len(decimal_part) > 2:
        return False
    groups = integer_part.split(thousands_separator)
    return _valid_grouped_integer(groups)


def _valid_single_separator(value: str, separator: str) -> bool:
    parts = value.split(separator)
    if len(parts) == 2 and 1 <= len(parts[1]) <= 2:
        return parts[0].isdigit() and parts[1].isdigit()
    return _valid_grouped_integer(parts)


def _valid_grouped_integer(groups: list[str]) -> bool:
    if not groups or not groups[0].isdigit() or not 1 <= len(groups[0]) <= 3:
        return False
    return all(group.isdigit() and len(group) == 3 for group in groups[1:])


def _looks_like_date(text: str) -> bool:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return True
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.0+)?", text):
        return True
    if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", text):
        return True
    try:
        datetime.fromisoformat(text)
        return True
    except ValueError:
        return False


def _looks_like_phone(text: str) -> bool:
    return bool(re.fullmatch(r"[\d\s()+\-./,;extEXT]+", text))


def _find_column(values_by_column: Mapping[str, str], normalized_name: str) -> str | None:
    for column_name in values_by_column:
        if _normalize_column_name(column_name) == normalized_name:
            return column_name
    return None


def _normalize_column_name(column_name: object) -> str:
    return normalize_text(column_name)


def _clean(value: object) -> str:
    return "" if value is None else str(value).strip()


def _is_int_between(text: str, minimum: int, maximum: int) -> bool:
    return text.isdigit() and minimum <= int(text) <= maximum


def _error(field_name: str, message: str) -> ValidationIssue:
    return ValidationIssue(field_name=field_name, message=message, severity=ERROR)


def _warning(field_name: str, message: str) -> ValidationIssue:
    return ValidationIssue(field_name=field_name, message=message, severity=WARNING)
