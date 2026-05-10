from datetime import datetime

from app.domain.column_standards import (
    DUE_DAY,
    DUE_MONTH,
    DUE_YEAR,
    EMAIL,
    INSURED_NAME,
    ISSUE_DATE,
    POLICY_NUMBER,
    format_display_value,
    get_column_label,
    get_column_visibility,
    is_coverage_column,
    normalize_header,
    resolve_column_key,
    visible_column_names,
)


def test_identifica_columnas_de_cobertura_con_criterio_conservador():
    assert is_coverage_column("Cobertura Responsabilidad Civil")
    assert is_coverage_column("COBERTURAS")
    assert not is_coverage_column("Monto Asegurado")
    assert not is_coverage_column("Columna A")


def test_visibilidad_oculta_coberturas_sin_ocultar_otras_columnas():
    coverage = get_column_visibility("Cobertura Robo")
    regular = get_column_visibility("Nombre del Asegurado")

    assert coverage.is_coverage
    assert not coverage.visible_in_table
    assert not coverage.visible_in_detail
    assert not coverage.visible_in_edit
    assert not coverage.searchable
    assert regular.visible_in_table
    assert regular.visible_in_detail
    assert regular.visible_in_edit
    assert regular.searchable


def test_filtra_columnas_visibles_sin_reordenar():
    columns = ("Cliente", "Cobertura A", "Poliza", "Cobertura B")

    assert visible_column_names(columns) == ("Cliente", "Poliza")


def test_normaliza_encabezados_ignorando_tildes_espacios_y_signos():
    assert normalize_header("  Nº   Póliza ") == normalize_header("No Poliza")
    assert normalize_header("Correo Electrónico") == normalize_header("correo electronico")


def test_resuelve_alias_a_claves_canonicas():
    assert resolve_column_key("Póliza") == POLICY_NUMBER
    assert resolve_column_key("Nombre Cliente") == INSURED_NAME
    assert resolve_column_key("Fecha Emision") == ISSUE_DATE
    assert resolve_column_key("Dia") == DUE_DAY
    assert resolve_column_key("MES") == DUE_MONTH
    assert resolve_column_key("Ano") == DUE_YEAR
    assert resolve_column_key("E-mail") == EMAIL
    assert resolve_column_key("Cobertura Daños") == "coverage"


def test_obtiene_etiqueta_principal_sin_reemplazar_encabezados_desconocidos():
    assert get_column_label(POLICY_NUMBER) == "Nº Póliza"
    assert get_column_label("Poliza") == "Nº Póliza"
    assert get_column_label("Columna Libre") == "Columna Libre"


def test_formato_centralizado_de_emision_sin_hora():
    assert format_display_value("Fecha Emision", datetime(2022, 3, 8, 0, 0, 0)) == "2022-03-08"
    assert format_display_value("Emisión", "2022-03-08 00:00:00") == "2022-03-08"
    assert format_display_value("Emisión", "08/03/2022 noche") == "08/03/2022 noche"
