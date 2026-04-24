import pytest

from app.domain import CANONICAL_FIELDS, CanonicalField, Editability, FieldOrigin, Sensitivity, get_canonical_field


def test_canonical_fields_have_unique_names():
    names = [field.name for field in CANONICAL_FIELDS]

    assert len(names) == len(set(names))


def test_canonical_field_classifications_match_documented_intent():
    assert get_canonical_field("numero_poliza_original").origin == FieldOrigin.ORIGINAL
    assert get_canonical_field("numero_poliza_original").sensitivity == Sensitivity.SENSITIVE
    assert get_canonical_field("numero_poliza_original").editability == Editability.READ_ONLY

    assert get_canonical_field("frecuencia_normalizada").origin == FieldOrigin.NORMALIZED
    assert get_canonical_field("es_dm").origin == FieldOrigin.DERIVED
    assert get_canonical_field("estado_gestion_vencimiento").editability == Editability.EDITABLE


def test_contracts_include_all_origin_categories():
    origins = {field.origin for field in CANONICAL_FIELDS}

    assert FieldOrigin.ORIGINAL in origins
    assert FieldOrigin.NORMALIZED in origins
    assert FieldOrigin.DERIVED in origins
    assert FieldOrigin.OPERATIONAL in origins


def test_canonical_field_requires_name_and_description():
    with pytest.raises(ValueError):
        CanonicalField(
            name="",
            origin=FieldOrigin.OPERATIONAL,
            sensitivity=Sensitivity.NON_SENSITIVE,
            editability=Editability.READ_ONLY,
            description="Campo tecnico.",
        )

    with pytest.raises(ValueError):
        CanonicalField(
            name="campo_tecnico",
            origin=FieldOrigin.OPERATIONAL,
            sensitivity=Sensitivity.NON_SENSITIVE,
            editability=Editability.READ_ONLY,
            description="",
        )


def test_unknown_canonical_field_raises_key_error():
    with pytest.raises(KeyError):
        get_canonical_field("campo_inexistente")
