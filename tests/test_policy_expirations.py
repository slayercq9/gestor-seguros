from datetime import date

import pytest

from app.domain.policy_expirations import (
    STATUS_ACTIVE,
    STATUS_EXPIRED,
    STATUS_EXPIRING_SOON,
    STATUS_INVALID_DATE,
    STATUS_NOTICE_NOT_APPLICABLE,
    calculate_due_date,
    classify_policy_expiration,
)


REFERENCE_DATE = date(2026, 5, 14)


def test_calculate_due_date_uses_day_month_and_year() -> None:
    assert calculate_due_date({"DÍA": "15", "MES": "6", "AÑO": "2026"}) == date(2026, 6, 15)


def test_calculate_due_date_supports_column_aliases() -> None:
    assert calculate_due_date({"Dia": "29", "Mes": "2", "Ano": "2024"}) == date(2024, 2, 29)


def test_calculate_due_date_returns_none_for_impossible_date() -> None:
    assert calculate_due_date({"DÍA": "31", "MES": "2", "AÑO": "2026"}) is None


def test_classifies_expired_policy() -> None:
    result = classify_policy_expiration(
        {"Vigencia": "Anual", "DÍA": "13", "MES": "5", "AÑO": "2026"},
        reference_date=REFERENCE_DATE,
    )

    assert result.status == STATUS_EXPIRED
    assert result.due_date == date(2026, 5, 13)


def test_classifies_policy_expiring_soon_with_default_threshold() -> None:
    result = classify_policy_expiration(
        {"Vigencia": "Mensual", "DÍA": "13", "MES": "6", "AÑO": "2026"},
        reference_date=REFERENCE_DATE,
    )

    assert result.status == STATUS_EXPIRING_SOON
    assert result.alert_days == 30


def test_classifies_active_policy_outside_alert_threshold() -> None:
    result = classify_policy_expiration(
        {"Vigencia": "Trimestral", "DÍA": "14", "MES": "6", "AÑO": "2026"},
        reference_date=REFERENCE_DATE,
    )

    assert result.status == STATUS_ACTIVE


def test_uses_configurable_alert_threshold() -> None:
    result = classify_policy_expiration(
        {"Vigencia": "Semestral", "DÍA": "3", "MES": "6", "AÑO": "2026"},
        reference_date=REFERENCE_DATE,
        alert_days=10,
    )

    assert result.status == STATUS_ACTIVE
    assert result.alert_days == 10


def test_classifies_empty_due_date_as_invalid_when_notice_applies() -> None:
    result = classify_policy_expiration(
        {"Vigencia": "Anual", "DÍA": "", "MES": "", "AÑO": ""},
        reference_date=REFERENCE_DATE,
    )

    assert result.status == STATUS_INVALID_DATE
    assert result.due_date is None


def test_classifies_dm_as_notice_not_applicable_without_requiring_date() -> None:
    result = classify_policy_expiration(
        {"Vigencia": "D.M.", "DÍA": "31", "MES": "2", "AÑO": "2026"},
        reference_date=REFERENCE_DATE,
    )

    assert result.status == STATUS_NOTICE_NOT_APPLICABLE
    assert result.due_date is None


def test_rejects_negative_alert_threshold() -> None:
    with pytest.raises(ValueError, match="alert_days"):
        classify_policy_expiration(
            {"Vigencia": "Anual", "DÍA": "1", "MES": "1", "AÑO": "2027"},
            reference_date=REFERENCE_DATE,
            alert_days=-1,
        )
