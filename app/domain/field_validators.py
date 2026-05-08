"""Validaciones suaves para campos editados del Control Cartera.

Estas reglas no corrigen ni bloquean datos históricos por sí mismas. Devuelven
advertencias para que la interfaz pida revisión antes de aplicar cambios en
memoria.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from app.domain.workbook_rules import normalize_text


VIGENCIA_VALUES = ("Mensual", "Trimestral", "Semestral", "Anual", "D.M.")
DAY_VALUES = tuple(str(value) for value in range(1, 32))
MONTH_VALUES = tuple(str(value) for value in range(1, 13))
YEAR_MIN = 2000
YEAR_MAX = 2100


@dataclass(frozen=True)
class FieldValidationWarning:
    """Advertencia no bloqueante para un campo editado."""

    field_name: str
    message: str
    critical: bool = False


def validate_edited_fields(values_by_column: Mapping[str, str]) -> tuple[FieldValidationWarning, ...]:
    """Valida valores editados y devuelve advertencias suaves."""
    warnings: list[FieldValidationWarning] = []
    for column_name, value in values_by_column.items():
        normalized = normalize_text(column_name)
        text = "" if value is None else str(value).strip()

        if normalized == "no poliza":
            if not text:
                warnings.append(_warning(column_name, "El número de póliza no debería quedar vacío.", critical=True))
        elif normalized == "nombre del asegurado":
            if not text:
                warnings.append(_warning(column_name, "El nombre del asegurado no debería quedar vacío.", critical=True))
        elif normalized == "vigencia":
            warnings.extend(_validate_vigencia(column_name, text))
        elif normalized == "dia":
            warnings.extend(_validate_range(column_name, text, 1, 31, "El día debe estar entre 1 y 31."))
        elif normalized == "mes":
            warnings.extend(_validate_range(column_name, text, 1, 12, "El mes debe estar entre 1 y 12."))
        elif normalized == "ano":
            warnings.extend(_validate_year(column_name, text))
        elif normalized == "correo":
            if text and "@" not in text:
                warnings.append(_warning(column_name, "El correo ingresado no contiene @."))
        elif normalized == "emision":
            warnings.extend(_validate_emission(column_name, text))
        elif normalized in {"monto asegurado", "prima"}:
            warnings.extend(_validate_money_like(column_name, text))
        elif normalized == "telefono":
            warnings.extend(_validate_phone_like(column_name, text))
        elif normalized == "tipo de poliza":
            if not text:
                warnings.append(_warning(column_name, "El tipo de póliza no debería quedar vacío."))
    return tuple(warnings)


def _validate_vigencia(column_name: str, text: str) -> tuple[FieldValidationWarning, ...]:
    if not text:
        return (_warning(column_name, "La vigencia no debería quedar vacía.", critical=True),)
    allowed = {normalize_text(value) for value in VIGENCIA_VALUES}
    if normalize_text(text) not in allowed:
        return (_warning(column_name, "La vigencia está fuera del catálogo sugerido."),)
    return ()


def _validate_range(
    column_name: str,
    text: str,
    minimum: int,
    maximum: int,
    message: str,
) -> tuple[FieldValidationWarning, ...]:
    if not text:
        return ()
    if not text.isdigit():
        return (_warning(column_name, message),)
    value = int(text)
    if not minimum <= value <= maximum:
        return (_warning(column_name, message),)
    return ()


def _validate_year(column_name: str, text: str) -> tuple[FieldValidationWarning, ...]:
    if not text:
        return ()
    if not re.fullmatch(r"\d{4}", text):
        return (_warning(column_name, "El año debería tener cuatro dígitos."),)
    value = int(text)
    if not YEAR_MIN <= value <= YEAR_MAX:
        return (_warning(column_name, f"El año está fuera del rango sugerido {YEAR_MIN}-{YEAR_MAX}."),)
    return ()


def _validate_emission(column_name: str, text: str) -> tuple[FieldValidationWarning, ...]:
    if not text:
        return ()
    if _looks_like_date(text):
        return ()
    return (_warning(column_name, "La emisión no parece una fecha reconocible."),)


def _validate_money_like(column_name: str, text: str) -> tuple[FieldValidationWarning, ...]:
    if not text:
        return ()
    if re.fullmatch(r"[\d\s.,₡$¢CRCUSD+-]+", text, flags=re.IGNORECASE):
        return ()
    return (_warning(column_name, "El monto contiene un formato poco usual."),)


def _validate_phone_like(column_name: str, text: str) -> tuple[FieldValidationWarning, ...]:
    if not text:
        return ()
    if re.fullmatch(r"[\d\s()+\-./,;extEXT]+", text):
        return ()
    return (_warning(column_name, "El teléfono contiene caracteres poco usuales."),)


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


def _warning(field_name: str, message: str, critical: bool = False) -> FieldValidationWarning:
    return FieldValidationWarning(field_name=field_name, message=message, critical=critical)
