from app.domain.field_validators import validate_edited_fields


def errors(values):
    return validate_edited_fields(values).errors


def warnings(values):
    return validate_edited_fields(values).warnings


def test_poliza_y_nombre_vacios_bloquean():
    result = validate_edited_fields({"Nº Póliza": "", "Nombre del Asegurado": ""})

    assert len(result.errors) == 2
    assert "póliza" in result.errors[0].message
    assert "asegurado" in result.errors[1].message


def test_vigencia_vacia_o_fuera_de_catalogo_bloquea():
    assert "obligatoria" in errors({"Vigencia": ""})[0].message
    assert "catálogo" in errors({"Vigencia": "Bimestral"})[0].message
    assert validate_edited_fields({"Vigencia": "D.M."}).errors == ()


def test_fecha_incompleta_bloquea_si_vigencia_requiere_vencimiento():
    result = validate_edited_fields({"Vigencia": "Anual", "DÍA": "1", "MES": "", "AÑO": "2026"})

    assert result.has_errors
    assert "obligatorios" in result.errors[0].message


def test_dia_mes_y_ano_invalidos_bloquean():
    assert "día" in errors({"Vigencia": "Mensual", "DÍA": "32", "MES": "1", "AÑO": "2026"})[0].message.lower()
    assert "mes" in errors({"Vigencia": "Mensual", "DÍA": "1", "MES": "13", "AÑO": "2026"})[0].message.lower()
    assert "cuatro dígitos" in errors({"Vigencia": "Mensual", "DÍA": "1", "MES": "1", "AÑO": "abc"})[0].message


def test_fechas_imposibles_bloquean_y_bisiesto_valido_permite():
    assert "no existe" in errors({"Vigencia": "Anual", "DÍA": "30", "MES": "2", "AÑO": "2025"})[0].message
    assert "no existe" in errors({"Vigencia": "Anual", "DÍA": "31", "MES": "2", "AÑO": "2025"})[0].message
    assert "no existe" in errors({"Vigencia": "Anual", "DÍA": "31", "MES": "4", "AÑO": "2025"})[0].message
    assert "no existe" in errors({"Vigencia": "Anual", "DÍA": "29", "MES": "2", "AÑO": "2025"})[0].message
    assert validate_edited_fields({"Vigencia": "Anual", "DÍA": "29", "MES": "2", "AÑO": "2024"}).errors == ()


def test_dm_permite_fecha_vacia_pero_no_fecha_invalida():
    assert validate_edited_fields({"Vigencia": "D.M.", "DÍA": "", "MES": "", "AÑO": ""}).errors == ()
    assert validate_edited_fields({"Vigencia": "D.M.", "DÍA": "31", "MES": "2", "AÑO": "2025"}).has_errors


def test_montos_invalidos_bloquean_y_vacios_permiten():
    valid_values = ("1000", "1000.50", "1000,50", "1,000.50", "1.000,50", "1 000,50", "₡1000", "$1000")
    for value in valid_values:
        assert validate_edited_fields({"Monto Asegurado": value, "Prima": value}).errors == ()

    invalid_values = ("abc", "100abc", "1..000", "1,,000", "10-20", "texto libre", "1000?")
    for value in invalid_values:
        assert validate_edited_fields({"Monto Asegurado": value}).has_errors

    assert validate_edited_fields({"Monto Asegurado": "", "Prima": ""}).errors == ()


def test_advertencias_suaves_no_bloquean():
    result = validate_edited_fields(
        {
            "Cédula": "",
            "Correo": "correo.example.test",
            "Emisión": "fecha dudosa",
            "Tipo de Póliza": "",
        }
    )

    assert result.errors == ()
    assert len(result.warnings) == 4
