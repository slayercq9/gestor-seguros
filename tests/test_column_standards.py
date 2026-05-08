from app.domain.column_standards import get_column_visibility, is_coverage_column, visible_column_names


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
