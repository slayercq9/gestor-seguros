from pathlib import Path


SPEC_PATH = Path("GestorSeguros.spec")


def test_spec_de_pyinstaller_existe_y_usa_entrypoint_actual():
    assert SPEC_PATH.exists()
    content = SPEC_PATH.read_text(encoding="utf-8")

    assert '"app/__main__.py"' in content
    assert 'name="GestorSeguros"' in content
    assert "console=False" in content


def test_spec_incluye_icono_svg_y_no_incluye_datos_reales():
    content = SPEC_PATH.read_text(encoding="utf-8")

    assert "assets/app_icon.svg" in content
    assert "data/input" not in content
    assert "data/output" not in content
    assert "data/backups" not in content
    assert "CONTROLCARTERA_V2.xlsx" not in content
