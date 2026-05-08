from app.domain.field_validators import validate_edited_fields


def warning_messages(values):
    return tuple(warning.message for warning in validate_edited_fields(values))


def test_poliza_vacia_genera_advertencia():
    warnings = validate_edited_fields({"Nº Póliza": ""})

    assert len(warnings) == 1
    assert warnings[0].critical
    assert "póliza" in warnings[0].message


def test_vigencia_vacia_o_fuera_de_catalogo_genera_advertencia():
    assert "vigencia" in warning_messages({"Vigencia": ""})[0].lower()
    assert "catálogo" in warning_messages({"Vigencia": "Bimestral"})[0]
    assert validate_edited_fields({"Vigencia": "Mensual"}) == ()


def test_dia_y_mes_fuera_de_rango_generan_advertencia():
    assert "día" in warning_messages({"DÍA": "32"})[0].lower()
    assert "mes" in warning_messages({"MES": "13"})[0].lower()
    assert validate_edited_fields({"DÍA": "", "MES": ""}) == ()


def test_ano_invalido_genera_advertencia():
    assert "cuatro dígitos" in warning_messages({"AÑO": "abc"})[0]
    assert "rango sugerido" in warning_messages({"AÑO": "2199"})[0]
    assert validate_edited_fields({"AÑO": "2026"}) == ()


def test_correo_sin_arroba_genera_advertencia_si_no_esta_vacio():
    assert "@" in warning_messages({"Correo": "correo.example.test"})[0]
    assert validate_edited_fields({"Correo": ""}) == ()


def test_emision_texto_invalido_genera_advertencia_suave():
    assert "fecha reconocible" in warning_messages({"Emisión": "fecha dudosa"})[0]
    assert validate_edited_fields({"Emisión": "2022-03-08"}) == ()


def test_montos_con_formato_raro_generan_advertencia():
    assert "formato poco usual" in warning_messages({"Monto Asegurado": "monto raro ?"})[0]
    assert "formato poco usual" in warning_messages({"Prima": "prima rara ?"})[0]
    assert validate_edited_fields({"Monto Asegurado": "₡ 1,250.50", "Prima": "USD 10.00"}) == ()
