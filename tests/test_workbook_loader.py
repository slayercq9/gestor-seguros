import shutil
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

import pytest
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill

from app.core.exceptions import WorkbookLoadError
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


def build_modernized_workbook(path: Path, include_sheet: bool = True, include_legacy_gs: bool = False) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = MAIN_SHEET_NAME if include_sheet else "OTRA_HOJA"

    headers = ["Cliente", "Poliza", "Vigencia", "Dia", "Mes", "Ano"]
    if include_legacy_gs:
        headers.extend(["GS_ES_DM", "GS_REQUIERE_REVISION"])
    worksheet.append(headers)
    worksheet.append(["Registro Ficticio A", "POL-FICT-001", "D.M.", 1, 5, 2026, "si", "no"])
    worksheet.append(["Registro Ficticio B", "POL-FICT-002", "Anual", 15, 8, 2026, "no", "no"])
    worksheet.cell(row=20, column=1).fill = PatternFill("solid", fgColor="FFFFFF")
    workbook.save(path)


def test_carga_control_cartera_ficticio_sin_modificar_fuente():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "modernizado.xlsx"
        build_modernized_workbook(source)
        original_bytes = source.read_bytes()

        result = load_modernized_workbook(source)

        assert source.read_bytes() == original_bytes
        assert result.summary.sheet_name == MAIN_SHEET_NAME
        assert result.summary.read_only is True
        assert result.summary.useful_rows_detected == 2
        assert result.summary.records_loaded == 2
        assert result.summary.rows_skipped >= 1
        assert result.summary.visible_columns == ("Cliente", "Poliza", "Vigencia", "Dia", "Mes", "Ano")
        assert not any(column.startswith("GS_") for column in result.summary.visible_columns)
        assert result.records[0].values_by_column["Cliente"] == "Registro Ficticio A"


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


def test_ignora_columnas_gs_heredadas_si_existen():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "modernizado_con_gs_heredadas.xlsx"
        build_modernized_workbook(source, include_legacy_gs=True)

        result = load_modernized_workbook(source)

        assert result.summary.records_loaded == 2
        assert "GS_ES_DM" not in result.summary.visible_columns
        assert "GS_REQUIERE_REVISION" not in result.summary.visible_columns
        assert "GS_ES_DM" not in result.records[0].values_by_column


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
        assert "Filas utiles detectadas" in completed.stdout
        assert "Columnas visibles" in completed.stdout
        assert "Columnas GS" not in completed.stdout
        assert "Registro Ficticio A" not in completed.stdout
        assert "POL-FICT-001" not in completed.stdout


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
