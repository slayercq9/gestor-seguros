import importlib.util
import json
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

from openpyxl import Workbook


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "auditar_base_local.py"
SPEC = importlib.util.spec_from_file_location("auditar_base_local", MODULE_PATH)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


@contextmanager
def workspace_tempdir():
    base_dir = Path("data/output")
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"tmp-test-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_detecta_vigencia_dm_y_categorias_observadas():
    summary = audit.summarize_frequency_values(
        ["D.M.", "Deduccion mensual", "Mensual", "Trimestral", "Semestral", "Anual", "Quincenal", None]
    )

    assert summary["has_dm"] is True
    assert summary["categories"][audit.FREQUENCY_DM] == 2
    assert summary["categories"][audit.FREQUENCY_MONTHLY] == 1
    assert summary["categories"][audit.FREQUENCY_QUARTERLY] == 1
    assert summary["categories"][audit.FREQUENCY_SEMIANNUAL] == 1
    assert summary["categories"][audit.FREQUENCY_ANNUAL] == 1
    assert summary["categories"][audit.FREQUENCY_OTHER] == 1
    assert summary["categories"][audit.FREQUENCY_EMPTY] == 1


def test_clasifica_polizas_por_prefijo_con_excepcion_numerica():
    assert audit.classify_policy_number("0100012345") == audit.POLICY_NUMERIC
    assert audit.classify_policy_number("01-ABC-123") == audit.POLICY_PREFIX_01
    assert audit.classify_policy_number("02-USD-456") == audit.POLICY_PREFIX_02
    assert audit.classify_policy_number("RT-ABC") == audit.POLICY_OTHER
    assert audit.classify_policy_number("") == audit.POLICY_EMPTY


def test_detecta_fecha_de_vencimiento_separada():
    columns = audit.build_column_metadata(["Cliente", "Dia", "Mes", "Ano", "No Poliza"], 5, True)
    result = audit.detect_separate_due_date_columns(columns)

    assert result["has_separate_due_date_fields"] is True
    assert result["columns"]["dia"][0]["display_name"] == "Dia"
    assert result["columns"]["mes"][0]["display_name"] == "Mes"
    assert result["columns"]["ano"][0]["display_name"] == "Ano"


def test_clasifica_identificaciones_de_forma_conservadora():
    assert audit.classify_identification_format("101110111") == audit.ID_PHYSICAL
    assert audit.classify_identification_format("3101123456") == audit.ID_LEGAL_OR_NUMERIC
    assert audit.classify_identification_format("A1234567") == audit.ID_PASSPORT_OR_FOREIGN
    assert audit.classify_identification_format("E-1234") == audit.ID_PASSPORT_OR_FOREIGN
    assert audit.classify_identification_format(None) == audit.ID_EMPTY


def test_reporte_no_expone_datos_sensibles_de_filas():
    with workspace_tempdir() as workspace_tmp:
        workbook_path = workspace_tmp / "base_ficticia.xlsx"
        output_dir = workspace_tmp / "auditoria"

        wb = Workbook()
        ws = wb.active
        ws.title = "Cartera"
        ws.append(
            [
                "Nombre Cliente",
                "Identificacion",
                "No Poliza",
                "Vigencia",
                "Dia",
                "Mes",
                "Ano",
                "Detalle",
                "Nro Placa / Finca",
            ]
        )
        ws.append(
            [
                "Ana Segura",
                "101110111",
                "01-ABC-999",
                "D.M.",
                1,
                5,
                2026,
                "Relacion interna familiar",
                "ABC123",
            ]
        )
        ws.append(
            [
                "Luis Prueba",
                "A1234567",
                "123456789",
                "Trimestral",
                15,
                8,
                2026,
                "Anotacion privada",
                "XYZ987",
            ]
        )
        wb.save(workbook_path)

        result = audit.audit_workbook(workbook_path, output_dir)
        markdown_path = Path(result["output_files"]["markdown"])
        json_path = Path(result["output_files"]["json"])

        assert markdown_path.exists()
        assert json_path.exists()

        combined_report = markdown_path.read_text(encoding="utf-8") + json_path.read_text(encoding="utf-8")
        for sensitive_token in [
            "Ana Segura",
            "Luis Prueba",
            "101110111",
            "A1234567",
            "01-ABC-999",
            "123456789",
            "ABC123",
            "XYZ987",
            "Relacion interna familiar",
            "Anotacion privada",
        ]:
            assert sensitive_token not in combined_report

        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["privacy"]["contains_row_samples"] is False
        assert data["privacy"]["contains_sensitive_values"] is False
        assert data["main_sheet"]["business_patterns"]["frequency"]["has_dm"] is True


def test_encabezado_incierto_usa_columnas_seguras_y_no_filtra_pii():
    with workspace_tempdir() as workspace_tmp:
        workbook_path = workspace_tmp / "sin_encabezado_ficticio.xlsx"
        output_dir = workspace_tmp / "auditoria_sin_encabezado"

        wb = Workbook()
        ws = wb.active
        ws.title = "Datos"
        ws.append(
            ["Ana Segura", "101110111", "01-ABC-999", "D.M.", 1, 5, 2026, "Nota privada", "ABC123"]
        )
        ws.append(
            ["Luis Prueba", "A1234567", "02-USD-456", "Mensual", 15, 8, 2026, "Otra nota", "XYZ987"]
        )
        wb.save(workbook_path)

        result = audit.audit_workbook(workbook_path, output_dir)
        markdown = Path(result["output_files"]["markdown"]).read_text(encoding="utf-8")
        data = json.loads(Path(result["output_files"]["json"]).read_text(encoding="utf-8"))
        combined_report = markdown + json.dumps(data, ensure_ascii=False)

        assert data["main_sheet"]["dimensions"]["header_confirmed"] is False
        assert data["main_sheet"]["columns"][0]["display_name"] == "COL_A"
        assert data["main_sheet"]["columns"][1]["display_name"] == "COL_B"
        assert "Calidad por Columna" in markdown
        assert "Vigencias y Frecuencias" in markdown

        for sensitive_token in [
            "Ana Segura",
            "Luis Prueba",
            "101110111",
            "A1234567",
            "01-ABC-999",
            "02-USD-456",
            "ABC123",
            "XYZ987",
            "Nota privada",
            "Otra nota",
        ]:
            assert sensitive_token not in combined_report
