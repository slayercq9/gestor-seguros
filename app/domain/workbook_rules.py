"""Preliminary workbook classification rules.

These helpers are intentionally conservative. They classify values for future
internal review workflows, but they do not correct, overwrite, or expose
original workbook data.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date
from typing import Any


FREQUENCY_DM = "dm"
FREQUENCY_MONTHLY = "mensual"
FREQUENCY_QUARTERLY = "trimestral"
FREQUENCY_SEMIANNUAL = "semestral"
FREQUENCY_ANNUAL = "anual"
FREQUENCY_OTHER = "otro"
FREQUENCY_EMPTY = "vacio"

POLICY_EMPTY = "vacio"
POLICY_WORKERS_RISK = "riesgos_trabajo_probable"
POLICY_PREFIX_01 = "prefijo_01"
POLICY_PREFIX_02 = "prefijo_02"
POLICY_OTHER = "otro"

CURRENCY_CRC = "CRC"
CURRENCY_USD = "USD"
CURRENCY_NOT_APPLICABLE = "no_aplica_riesgo_trabajo"
CURRENCY_PENDING = "pendiente"

ID_EMPTY = "vacio"
ID_PHYSICAL = "cedula_fisica_probable"
ID_LEGAL_OR_NUMERIC = "cedula_juridica_u_otro_numerico_probable"
ID_PASSPORT_OR_FOREIGN = "pasaporte_o_extranjero_probable"
ID_OTHER_NUMERIC = "otro_formato_numerico"
ID_OTHER = "otro"


def safe_text(value: Any) -> str:
    """Return a compact text representation for internal classification."""
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def normalize_text(value: Any) -> str:
    """Normalize text for matching without changing source values."""
    text = safe_text(value).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("\u00ba", "o").replace("\u00b0", "o")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def classify_frequency(value: Any) -> str:
    """Classify observed payment frequency conservatively."""
    normalized = normalize_text(value)
    compact = normalized.replace(" ", "")

    if not normalized:
        return FREQUENCY_EMPTY
    if compact in {"dm", "dms"} or "deduccion mensual" in normalized:
        return FREQUENCY_DM
    if "trimes" in normalized or compact in {"trim", "trimestral"}:
        return FREQUENCY_QUARTERLY
    if "semes" in normalized or compact in {"semi", "semestral"}:
        return FREQUENCY_SEMIANNUAL
    if "mensual" in normalized or compact in {"mens", "mensuales"}:
        return FREQUENCY_MONTHLY
    if "anual" in normalized or compact in {"anuales", "annual"}:
        return FREQUENCY_ANNUAL
    return FREQUENCY_OTHER


def classify_policy_number(value: Any) -> str:
    """Classify policy number patterns without validating the policy."""
    text = safe_text(value)
    compact = re.sub(r"\s+", "", text)

    if not compact:
        return POLICY_EMPTY
    if compact.isdigit():
        return POLICY_WORKERS_RISK
    if compact.startswith("01"):
        return POLICY_PREFIX_01
    if compact.startswith("02"):
        return POLICY_PREFIX_02
    return POLICY_OTHER


def infer_currency(policy_number: Any) -> str:
    """Infer currency preliminarily from policy number pattern."""
    policy_type = classify_policy_number(policy_number)
    if policy_type == POLICY_WORKERS_RISK:
        return CURRENCY_NOT_APPLICABLE
    if policy_type == POLICY_PREFIX_01:
        return CURRENCY_CRC
    if policy_type == POLICY_PREFIX_02:
        return CURRENCY_USD
    return CURRENCY_PENDING


def classify_identification_format(value: Any) -> str:
    """Classify identification formats without rejecting records."""
    text = safe_text(value)
    compact = re.sub(r"[^A-Za-z0-9]+", "", text).upper()

    if not compact:
        return ID_EMPTY
    if any(ch.isalpha() for ch in compact):
        return ID_PASSPORT_OR_FOREIGN
    if compact.isdigit() and len(compact) == 9:
        return ID_PHYSICAL
    if compact.isdigit() and len(compact) >= 10:
        return ID_LEGAL_OR_NUMERIC
    if compact.isdigit():
        return ID_OTHER_NUMERIC
    return ID_OTHER


def consolidate_due_date(day: Any, month: Any, year: Any) -> date | None:
    """Build a date only when day, month and year are valid."""
    try:
        if day is None or month is None or year is None:
            return None
        return date(int(year), int(month), int(day))
    except (TypeError, ValueError):
        return None
