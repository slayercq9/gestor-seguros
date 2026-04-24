"""Preliminary canonical dataset contracts.

These contracts describe field intent and classification only. They do not
transform source data, validate real records, or read confidential workbooks.
"""

from dataclasses import dataclass
from enum import Enum


class FieldOrigin(str, Enum):
    """Origin category for a canonical field."""

    ORIGINAL = "original"
    NORMALIZED = "normalized"
    DERIVED = "derived"
    OPERATIONAL = "operational"


class Sensitivity(str, Enum):
    """Sensitivity category for a canonical field."""

    SENSITIVE = "sensitive"
    NON_SENSITIVE = "non_sensitive"


class Editability(str, Enum):
    """Future editability category for a canonical field."""

    EDITABLE = "editable"
    READ_ONLY = "read_only"


@dataclass(frozen=True)
class CanonicalField:
    """Describes a canonical field without binding it to real data."""

    name: str
    origin: FieldOrigin
    sensitivity: Sensitivity
    editability: Editability
    description: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("El nombre del campo canonico no puede estar vacio.")
        if not self.description.strip():
            raise ValueError("La descripcion del campo canonico no puede estar vacia.")


CANONICAL_FIELDS: tuple[CanonicalField, ...] = (
    CanonicalField(
        name="cliente_id",
        origin=FieldOrigin.OPERATIONAL,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Identificador interno futuro del cliente.",
    ),
    CanonicalField(
        name="nombre_original",
        origin=FieldOrigin.ORIGINAL,
        sensitivity=Sensitivity.SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Nombre o razon social preservado desde el origen.",
    ),
    CanonicalField(
        name="identificacion_original",
        origin=FieldOrigin.ORIGINAL,
        sensitivity=Sensitivity.SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Identificacion preservada desde el origen.",
    ),
    CanonicalField(
        name="identificacion_normalizada",
        origin=FieldOrigin.NORMALIZED,
        sensitivity=Sensitivity.SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Representacion tecnica futura de la identificacion.",
    ),
    CanonicalField(
        name="poliza_id",
        origin=FieldOrigin.OPERATIONAL,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Identificador interno futuro de la poliza.",
    ),
    CanonicalField(
        name="numero_poliza_original",
        origin=FieldOrigin.ORIGINAL,
        sensitivity=Sensitivity.SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Numero de poliza preservado desde el origen.",
    ),
    CanonicalField(
        name="vigencia_original",
        origin=FieldOrigin.ORIGINAL,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Vigencia o frecuencia tal como llega del origen.",
    ),
    CanonicalField(
        name="frecuencia_normalizada",
        origin=FieldOrigin.NORMALIZED,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Categoria tecnica futura para frecuencia.",
    ),
    CanonicalField(
        name="es_dm",
        origin=FieldOrigin.DERIVED,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Indicador preliminar de deduccion mensual.",
    ),
    CanonicalField(
        name="genera_aviso",
        origin=FieldOrigin.DERIVED,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Indicador futuro documentado, sin logica funcional en esta fase.",
    ),
    CanonicalField(
        name="moneda_normalizada",
        origin=FieldOrigin.DERIVED,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Moneda inferida o validada en fases futuras.",
    ),
    CanonicalField(
        name="fecha_vencimiento_normalizada",
        origin=FieldOrigin.DERIVED,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Fecha consolidada futura desde origen completo o partes.",
    ),
    CanonicalField(
        name="detalle_original",
        origin=FieldOrigin.ORIGINAL,
        sensitivity=Sensitivity.SENSITIVE,
        editability=Editability.READ_ONLY,
        description="Texto libre preservado desde origen y tratado como sensible.",
    ),
    CanonicalField(
        name="estado_gestion_vencimiento",
        origin=FieldOrigin.OPERATIONAL,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.EDITABLE,
        description="Estado operativo futuro del seguimiento.",
    ),
    CanonicalField(
        name="observacion_revision_poliza",
        origin=FieldOrigin.OPERATIONAL,
        sensitivity=Sensitivity.NON_SENSITIVE,
        editability=Editability.EDITABLE,
        description="Nota operativa futura separada del dato original.",
    ),
)


def get_canonical_field(name: str) -> CanonicalField:
    """Return a canonical field by name."""
    for field in CANONICAL_FIELDS:
        if field.name == name:
            return field
    raise KeyError(f"Campo canonico no registrado: {name}")
