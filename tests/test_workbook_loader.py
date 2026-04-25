import subprocess
import sys
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest
from openpyxl import Workbook, load_workbook

from app.core.exceptions import WorkbookLoadError
from app.domain.workbook_records import EXPECTED_GS_COLUMNS
from app.services.workbook_loader import MAIN_SHEET_NAME, load_modernized_workbook


@contextmanager
def workspace_tempdir():
    base_dir = Path("data/output")
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"tmp-loader-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def build_modernized_workbook(path: Path, include_sheet: bool = True, missing_gs: bool = False) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = MAIN_SHEET_NAME if include_sheet else "OTRA_HOJA"

    gs_columns = EXPECTED_GS_COLUMNS[:-2] if missing_gs else EXPECTED_GS_COLUMNS
    worksheet.append(["Cliente", "Poliza", "Vigencia", *gs_columns])
    worksheet.append(["Ana Segura", "01-ABC-123", "D.M.", "dm", "si", "no", "prefijo_01", "CRC", "fisica", "2026-05-01", "no", ""])
    worksheet.append(["Bruno Prueba", "02-XYZ-999", "Anual", "anual", "no", "preliminar", "prefijo_02", "USD", "pasaporte", None, "si", "fecha"])
    workbook.save(path)


def test_carga_workbook_modernizado_ficticio_sin_modificar_fuente():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "modernizado.xlsx"
        build_modernized_workbook(source)
        original_bytes = source.read_bytes()

        result = load_modernized_workbook(source)

        assert source.read_bytes() == original_bytes
        assert result.summary.sheet_name == MAIN_SHEET_NAME
        assert result.summary.structure_complete is True
        assert result.summary.records_loaded == 2
        assert result.summary.rows_skipped == 0
        assert set(result.summary.gs_columns_present) == set(EXPECTED_GS_COLUMNS)
        assert result.records[0].gs_values["GS_ES_DM"] == "si"


def test_valida_archivo_inexistente_y_extension_incorrecta():
    with workspace_tempdir() as temp_dir:
        with pytest.raises(WorkbookLoadError):
            load_modernized_workbook(temp_dir / "no_existe.xlsx")

        invalid = temp_dir / "modernizado.txt"
        invalid.write_text("no es excel", encoding="utf-8")

        with pytest.raises(WorkbookLoadError):
            load_modernized_workbook(invalid)


def test_requiere_hoja_principal_controles():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "sin_hoja.xlsx"
        build_modernized_workbook(source, include_sheet=False)

        with pytest.raises(WorkbookLoadError):
            load_modernized_workbook(source)


def test_reporta_columnas_gs_faltantes_sin_fallar():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "modernizado_incompleto.xlsx"
        build_modernized_workbook(source, missing_gs=True)

        result = load_modernized_workbook(source)

        assert result.summary.structure_complete is False
        assert result.summary.records_loaded == 2
        assert "GS_REQUIERE_REVISION" in result.summary.gs_columns_missing
        assert "Estructura incompleta" in " ".join(result.summary.warnings)


def test_script_imprime_resumen_sin_valores_sensibles_ficticios():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "modernizado.xlsx"
        build_modernized_workbook(source)

        completed = subprocess.run(
            [sys.executable, "scripts/cargar_workbook_modernizado.py", str(source)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0
        assert "Carga controlada completada" in completed.stdout
        assert "Ana Segura" not in completed.stdout
        assert "01-ABC-123" not in completed.stdout
        assert "Bruno Prueba" not in completed.stdout
        assert "02-XYZ-999" not in completed.stdout


def test_no_crea_outputs_permanentes():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "modernizado.xlsx"
        build_modernized_workbook(source)
        before = {path.name for path in temp_dir.iterdir()}

        load_modernized_workbook(source)

        after = {path.name for path in temp_dir.iterdir()}
        assert after == before

        workbook = load_workbook(source, read_only=True)
        try:
            assert workbook.sheetnames == [MAIN_SHEET_NAME]
        finally:
            workbook.close()
