import json
import shutil
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

from openpyxl import Workbook, load_workbook

from app.core.exceptions import WorkbookModernizationError
from app.services.workbook_modernizer import (
    AUXILIARY_COLUMNS,
    REPORT_JSON_NAME,
    REPORT_MD_NAME,
    REVIEW_CSV_NAME,
    modernize_workbook,
)


@contextmanager
def workspace_tempdir():
    base_dir = Path("data/output")
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"tmp-modernizer-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def build_fake_workbook(path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Cartera"
    sheet.append(
        [
            "Nombre Cliente",
            "Identificacion",
            "Numero de Poliza",
            "Vigencia",
            "Dia",
            "Mes",
            "Ano",
            "Detalle",
            "Numero de Placa / Finca",
        ]
    )
    sheet.append(["Ana Segura", "101110111", "01-ABC-999", "D.M.", 1, 5, 2026, "Nota familiar", "ABC123"])
    sheet.append(["Luis Prueba", "A1234567", "02-USD-456", "Mensual", 15, 8, 2026, "Otra nota", "XYZ987"])
    sheet.append(["Caso Riesgo", "3101123456", "123456789", "Trimestral", 20, 10, 2026, "", ""])
    sheet.append(["Caso Revision", "", "", "", 31, 2, 2026, "Privado", "ZZZ999"])
    workbook.save(path)


def test_moderniza_copia_sin_alterar_fuente():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "base_ficticia.xlsx"
        output_dir = temp_dir / "salida"
        build_fake_workbook(source)
        original_bytes = source.read_bytes()

        result = modernize_workbook(source, output_dir)

        assert source.read_bytes() == original_bytes
        assert result.output_workbook.parent == output_dir.resolve()
        assert result.output_workbook.name.startswith("base_ficticia_modernizado_")
        assert result.output_workbook.name.endswith(".xlsx")
        assert result.output_workbook.exists()
        assert result.markdown_report.exists()
        assert result.json_report.exists()
        assert result.review_csv.exists()


def test_agrega_columnas_auxiliares_y_valores_preliminares():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "base_ficticia.xlsx"
        output_dir = temp_dir / "salida"
        build_fake_workbook(source)

        result = modernize_workbook(source, output_dir)
        workbook = load_workbook(result.output_workbook)
        try:
            sheet = workbook["Cartera"]
            headers = [cell.value for cell in sheet[1]]
            assert headers[-len(AUXILIARY_COLUMNS) :] == list(AUXILIARY_COLUMNS)

            positions = {header: index + 1 for index, header in enumerate(headers)}
            assert sheet.cell(row=2, column=positions["GS_ES_DM"]).value == "si"
            assert sheet.cell(row=2, column=positions["GS_GENERA_AVISO_PRELIMINAR"]).value == "no"
            assert sheet.cell(row=2, column=positions["GS_MONEDA_PRELIMINAR"]).value == "CRC"
            assert sheet.cell(row=3, column=positions["GS_MONEDA_PRELIMINAR"]).value == "USD"
            assert sheet.cell(row=4, column=positions["GS_PATRON_POLIZA"]).value == "riesgos_trabajo_probable"
            assert sheet.cell(row=4, column=positions["GS_MONEDA_PRELIMINAR"]).value == "no_aplica_riesgo_trabajo"
            assert sheet.cell(row=2, column=positions["GS_FECHA_VENCIMIENTO_TECNICA"]).value.date().isoformat() == "2026-05-01"
            assert sheet.cell(row=5, column=positions["GS_REQUIERE_REVISION"]).value == "si"
        finally:
            workbook.close()


def test_reportes_no_exponen_datos_sensibles_ficticios():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "base_ficticia.xlsx"
        output_dir = temp_dir / "salida"
        build_fake_workbook(source)

        modernize_workbook(source, output_dir)
        combined = (output_dir / REPORT_MD_NAME).read_text(encoding="utf-8")
        combined += (output_dir / REPORT_JSON_NAME).read_text(encoding="utf-8")
        combined += (output_dir / REVIEW_CSV_NAME).read_text(encoding="utf-8")

        for token in ["Ana Segura", "101110111", "01-ABC-999", "ABC123", "Nota familiar"]:
            assert token not in combined

        data = json.loads((output_dir / REPORT_JSON_NAME).read_text(encoding="utf-8"))
        assert data["dm_count"] == 1
        assert data["review_rows"] >= 1
        assert data["privacy"]["contains_row_samples"] is False
        assert data["privacy"]["contains_sensitive_values"] is False
        assert (output_dir / REVIEW_CSV_NAME).exists()


def test_formato_visual_basico_y_hoja_control():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "base_ficticia.xlsx"
        output_dir = temp_dir / "salida"
        build_fake_workbook(source)

        result = modernize_workbook(source, output_dir)
        workbook = load_workbook(result.output_workbook)
        try:
            sheet = workbook["Cartera"]
            assert sheet.freeze_panes == "A2"
            assert sheet.auto_filter.ref is not None
            assert "CONTROL_MODERNIZACION" in workbook.sheetnames
        finally:
            workbook.close()


def test_script_falla_de_forma_controlada_si_no_existe_entrada():
    with workspace_tempdir() as temp_dir:
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/modernizar_workbook_local.py",
                str(temp_dir / "no_existe.xlsx"),
                str(temp_dir / "salida"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 1
        assert "Error de modernizacion" in completed.stdout


def test_rechaza_salida_igual_al_archivo_original():
    with workspace_tempdir() as temp_dir:
        source = temp_dir / "base_ficticia.xlsx"
        build_fake_workbook(source)

        try:
            modernize_workbook(source, source)
        except WorkbookModernizationError as exc:
            assert "archivo original" in str(exc)
        else:
            raise AssertionError("Se esperaba WorkbookModernizationError")
