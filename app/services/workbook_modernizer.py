"""Controlled workbook modernization service.

The service creates a local modernized copy and review reports. It never saves
over the original workbook and never deletes records.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from app.core.exceptions import WorkbookModernizationError
from app.domain.workbook_rules import (
    CURRENCY_PENDING,
    FREQUENCY_DM,
    FREQUENCY_EMPTY,
    FREQUENCY_OTHER,
    POLICY_EMPTY,
    classify_frequency,
    classify_identification_format,
    classify_policy_number,
    consolidate_due_date,
    infer_currency,
    normalize_text,
    safe_text,
)


REPORT_MD_NAME = "resumen_modernizacion.md"
REPORT_JSON_NAME = "resumen_modernizacion.json"
REVIEW_CSV_NAME = "control_revision.csv"
CONTROL_SHEET_NAME = "CONTROL_MODERNIZACION"

AUXILIARY_COLUMNS = (
    "GS_FRECUENCIA_OBSERVADA",
    "GS_ES_DM",
    "GS_GENERA_AVISO_PRELIMINAR",
    "GS_PATRON_POLIZA",
    "GS_MONEDA_PRELIMINAR",
    "GS_TIPO_IDENTIFICACION_PROBABLE",
    "GS_FECHA_VENCIMIENTO_TECNICA",
    "GS_REQUIERE_REVISION",
    "GS_MOTIVO_REVISION",
)


@dataclass(frozen=True)
class ModernizationResult:
    """Paths and metadata produced by workbook modernization."""

    output_workbook: Path
    markdown_report: Path
    json_report: Path
    review_csv: Path
    main_sheet: str
    processed_rows: int
    review_rows: int


def modernize_workbook(input_path: str | Path, output_dir: str | Path) -> ModernizationResult:
    """Create a modernized local copy and local control reports."""
    source = Path(input_path).resolve()
    destination_dir = Path(output_dir).resolve()
    if destination_dir == source:
        raise WorkbookModernizationError("La carpeta de salida no puede ser el archivo original.")
    generated_at = datetime.now()
    output_workbook = destination_dir / _build_output_workbook_name(source, generated_at)

    _validate_paths(source, output_workbook)
    destination_dir.mkdir(parents=True, exist_ok=True)

    workbook = load_workbook(source)
    try:
        main_sheet = _select_main_sheet(workbook.worksheets)
        worksheet = workbook[main_sheet]
        header_row = _detect_header_row(worksheet)
        column_map = _build_column_map(worksheet, header_row)
        summary = _apply_auxiliary_columns(worksheet, header_row, column_map)

        _apply_visual_formatting(worksheet, header_row, summary["auxiliary_start_column"])
        _write_control_sheet(workbook, source, output_workbook, main_sheet, summary)

        workbook.save(output_workbook)
    finally:
        workbook.close()

    report = _build_report(
        source,
        output_workbook,
        main_sheet,
        worksheet.max_row,
        worksheet.max_column,
        summary,
        generated_at,
    )
    markdown_report = destination_dir / REPORT_MD_NAME
    json_report = destination_dir / REPORT_JSON_NAME
    review_csv = destination_dir / REVIEW_CSV_NAME
    markdown_report.write_text(_render_markdown_report(report), encoding="utf-8")
    json_report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_review_csv(review_csv, summary["review_items"])

    return ModernizationResult(
        output_workbook=output_workbook,
        markdown_report=markdown_report,
        json_report=json_report,
        review_csv=review_csv,
        main_sheet=main_sheet,
        processed_rows=summary["processed_rows"],
        review_rows=summary["review_rows"],
    )


def _build_output_workbook_name(source: Path, generated_at: datetime) -> str:
    timestamp = generated_at.strftime("%Y%m%d_%H%M%S")
    return f"{source.stem}_modernizado_{timestamp}.xlsx"


def _validate_paths(source: Path, output_workbook: Path) -> None:
    if not source.exists():
        raise WorkbookModernizationError(f"No existe el workbook de entrada: {source}")
    if source.suffix.lower() not in {".xlsx", ".xlsm"}:
        raise WorkbookModernizationError("El workbook de entrada debe ser .xlsx o .xlsm.")
    if source == output_workbook.resolve():
        raise WorkbookModernizationError("La salida no puede ser el mismo archivo original.")


def _select_main_sheet(worksheets: list[Worksheet]) -> str:
    """Select the sheet with the largest useful data footprint."""
    return max(
        worksheets,
        key=lambda sheet: (
            _count_non_empty_rows(sheet),
            sheet.max_column or 0,
            _score_header_row(sheet, _detect_header_row(sheet)),
        ),
    ).title


def _count_non_empty_rows(worksheet: Worksheet) -> int:
    return sum(1 for row in worksheet.iter_rows(values_only=True) if any(not _is_empty(value) for value in row))


def _detect_header_row(worksheet: Worksheet, scan_rows: int = 20) -> int:
    best_row = 1
    best_score = -1
    max_scan = min(worksheet.max_row or 1, scan_rows)
    for row_index in range(1, max_scan + 1):
        score = _score_header_row(worksheet, row_index)
        if score > best_score:
            best_score = score
            best_row = row_index
    return best_row


def _score_header_row(worksheet: Worksheet, row_index: int) -> int:
    keywords = {
        "ano",
        "asegurado",
        "cliente",
        "detalle",
        "dia",
        "finca",
        "identificacion",
        "mes",
        "placa",
        "poliza",
        "venc",
        "vigencia",
    }
    score = 0
    for cell in worksheet[row_index]:
        normalized = normalize_text(cell.value)
        if normalized:
            score += 1
        if any(keyword in normalized for keyword in keywords):
            score += 8
    return score


def _build_column_map(worksheet: Worksheet, header_row: int) -> dict[str, int]:
    column_map: dict[str, int] = {}
    for cell in worksheet[header_row]:
        normalized = normalize_text(cell.value)
        if not normalized:
            continue
        if "poliza" in normalized and "policy" not in column_map:
            column_map["policy"] = cell.column
        if ("vigencia" in normalized or "frecuencia" in normalized) and "frequency" not in column_map:
            column_map["frequency"] = cell.column
        if ("identificacion" in normalized or "cedula" in normalized) and "identification" not in column_map:
            column_map["identification"] = cell.column
        tokens = set(normalized.split())
        if "dia" in tokens and ("venc" in normalized or normalized == "dia"):
            column_map.setdefault("due_day", cell.column)
        if "mes" in tokens and ("venc" in normalized or normalized == "mes"):
            column_map.setdefault("due_month", cell.column)
        if ("ano" in tokens or "anio" in tokens) and ("venc" in normalized or normalized in {"ano", "anio"}):
            column_map.setdefault("due_year", cell.column)
    return column_map


def _apply_auxiliary_columns(worksheet: Worksheet, header_row: int, column_map: dict[str, int]) -> dict[str, Any]:
    auxiliary_start = (worksheet.max_column or 0) + 1
    for offset, name in enumerate(AUXILIARY_COLUMNS):
        worksheet.cell(row=header_row, column=auxiliary_start + offset, value=name)

    frequency_counts: Counter[str] = Counter()
    currency_counts: Counter[str] = Counter()
    policy_counts: Counter[str] = Counter()
    review_counts: Counter[str] = Counter()
    review_items: list[dict[str, Any]] = []
    dm_count = 0
    review_rows = 0
    processed_rows = 0

    for row_index in range(header_row + 1, (worksheet.max_row or header_row) + 1):
        if not _row_has_data(worksheet, row_index, auxiliary_start - 1):
            continue

        processed_rows += 1
        row_result = _build_row_auxiliary_values(worksheet, row_index, column_map)
        frequency_counts[row_result["GS_FRECUENCIA_OBSERVADA"]] += 1
        currency_counts[row_result["GS_MONEDA_PRELIMINAR"]] += 1
        policy_counts[row_result["GS_PATRON_POLIZA"]] += 1

        if row_result["GS_ES_DM"] == "si":
            dm_count += 1
        if row_result["GS_REQUIERE_REVISION"] == "si":
            review_rows += 1
            review_items.append(
                {
                    "hoja": worksheet.title,
                    "fila": row_index,
                    "motivo_revision": row_result["GS_MOTIVO_REVISION"],
                    "columna_poliza": column_map.get("policy"),
                    "columna_frecuencia": column_map.get("frequency"),
                    "columna_identificacion": column_map.get("identification"),
                }
            )
            for reason in row_result["GS_MOTIVO_REVISION"].split("; "):
                if reason:
                    review_counts[reason] += 1

        for offset, name in enumerate(AUXILIARY_COLUMNS):
            cell = worksheet.cell(row=row_index, column=auxiliary_start + offset, value=row_result[name])
            if name == "GS_FECHA_VENCIMIENTO_TECNICA" and row_result[name]:
                cell.number_format = "yyyy-mm-dd"

    return {
        "auxiliary_start_column": auxiliary_start,
        "auxiliary_columns": list(AUXILIARY_COLUMNS),
        "processed_rows": processed_rows,
        "review_rows": review_rows,
        "dm_count": dm_count,
        "frequency_counts": dict(sorted(frequency_counts.items())),
        "currency_counts": dict(sorted(currency_counts.items())),
        "policy_counts": dict(sorted(policy_counts.items())),
        "review_reason_counts": dict(sorted(review_counts.items())),
        "review_items": review_items,
        "warnings": _build_warnings(column_map),
        "recommendations": [
            "Validar manualmente los registros marcados como requiere_revision.",
            "Revisar las inferencias de moneda antes de usarlas como regla definitiva.",
            "Mantener el workbook original como fuente oficial hasta aprobacion humana.",
        ],
    }


def _build_row_auxiliary_values(worksheet: Worksheet, row_index: int, column_map: dict[str, int]) -> dict[str, Any]:
    policy_value = _cell_value(worksheet, row_index, column_map.get("policy"))
    frequency_value = _cell_value(worksheet, row_index, column_map.get("frequency"))
    identification_value = _cell_value(worksheet, row_index, column_map.get("identification"))
    due_date = consolidate_due_date(
        _cell_value(worksheet, row_index, column_map.get("due_day")),
        _cell_value(worksheet, row_index, column_map.get("due_month")),
        _cell_value(worksheet, row_index, column_map.get("due_year")),
    )

    frequency = classify_frequency(frequency_value)
    policy_type = classify_policy_number(policy_value)
    currency = infer_currency(policy_value)
    identification_type = classify_identification_format(identification_value)
    reasons = []

    if policy_type == POLICY_EMPTY:
        reasons.append("poliza_vacia_o_no_detectada")
    if frequency in {FREQUENCY_EMPTY, FREQUENCY_OTHER}:
        reasons.append("frecuencia_no_reconocida")
    if currency == CURRENCY_PENDING:
        reasons.append("moneda_pendiente")
    if {"due_day", "due_month", "due_year"}.issubset(column_map) and due_date is None:
        reasons.append("fecha_vencimiento_no_consolidada")
    if column_map.get("identification") and identification_type in {"vacio", "otro"}:
        reasons.append("identificacion_requiere_revision")

    requires_review = "si" if reasons else "no"
    is_dm = "si" if frequency == FREQUENCY_DM else "no"

    return {
        "GS_FRECUENCIA_OBSERVADA": frequency,
        "GS_ES_DM": is_dm,
        "GS_GENERA_AVISO_PRELIMINAR": "no" if is_dm == "si" else "preliminar",
        "GS_PATRON_POLIZA": policy_type,
        "GS_MONEDA_PRELIMINAR": currency,
        "GS_TIPO_IDENTIFICACION_PROBABLE": identification_type,
        "GS_FECHA_VENCIMIENTO_TECNICA": due_date,
        "GS_REQUIERE_REVISION": requires_review,
        "GS_MOTIVO_REVISION": "; ".join(reasons),
    }


def _apply_visual_formatting(worksheet: Worksheet, header_row: int, auxiliary_start: int) -> None:
    header_fill = PatternFill("solid", fgColor="D9EAF7")
    auxiliary_fill = PatternFill("solid", fgColor="E2F0D9")
    header_font = Font(bold=True)

    max_column = worksheet.max_column or 1
    for column_index in range(1, max_column + 1):
        cell = worksheet.cell(row=header_row, column=column_index)
        cell.font = header_font
        cell.fill = auxiliary_fill if column_index >= auxiliary_start else header_fill
        width = max(12, min(35, len(safe_text(cell.value)) + 4))
        worksheet.column_dimensions[get_column_letter(column_index)].width = width

    worksheet.freeze_panes = worksheet.cell(row=header_row + 1, column=1).coordinate
    worksheet.auto_filter.ref = worksheet.dimensions


def _write_control_sheet(
    workbook: Any,
    source: Path,
    output_workbook: Path,
    main_sheet: str,
    summary: dict[str, Any],
) -> None:
    if CONTROL_SHEET_NAME in workbook.sheetnames:
        del workbook[CONTROL_SHEET_NAME]
    sheet = workbook.create_sheet(CONTROL_SHEET_NAME)
    rows = [
        ("concepto", "valor"),
        ("generado_en", datetime.now().isoformat(timespec="seconds")),
        ("archivo_entrada", source.name),
        ("archivo_salida", output_workbook.name),
        ("hoja_principal", main_sheet),
        ("filas_procesadas", summary["processed_rows"]),
        ("registros_requieren_revision", summary["review_rows"]),
        ("dm_detectados", summary["dm_count"]),
        ("nota", "Copia local modernizada; no reemplaza el workbook original."),
    ]
    for row in rows:
        sheet.append(row)
    sheet.freeze_panes = "A2"
    sheet.column_dimensions["A"].width = 32
    sheet.column_dimensions["B"].width = 80
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="D9EAF7")


def _build_report(
    source: Path,
    output_workbook: Path,
    main_sheet: str,
    rows: int,
    columns: int,
    summary: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "generated_at": generated_at.isoformat(timespec="seconds"),
        "input_file": source.name,
        "output_file": str(output_workbook),
        "main_sheet": main_sheet,
        "dimensions": {"rows": rows, "columns": columns},
        "auxiliary_columns": summary["auxiliary_columns"],
        "processed_rows": summary["processed_rows"],
        "review_rows": summary["review_rows"],
        "dm_count": summary["dm_count"],
        "frequency_counts": summary["frequency_counts"],
        "currency_counts": summary["currency_counts"],
        "policy_counts": summary["policy_counts"],
        "review_reason_counts": summary["review_reason_counts"],
        "warnings": summary["warnings"],
        "recommendations": summary["recommendations"],
        "privacy": {
            "contains_row_samples": False,
            "contains_sensitive_values": False,
            "notes": [
                "El reporte contiene estadisticas y rutas locales, no valores reales de filas.",
                "La copia modernizada local puede contener datos reales y esta bajo data/output/.",
            ],
        },
    }


def _write_review_csv(path: Path, review_items: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "hoja",
                "fila",
                "motivo_revision",
                "columna_poliza",
                "columna_frecuencia",
                "columna_identificacion",
            ],
        )
        writer.writeheader()
        for item in review_items:
            writer.writerow(item)


def _render_markdown_report(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Reporte de Modernizacion Workbook",
            "",
            "Reporte local de control. No incluye muestras de filas ni valores sensibles.",
            "",
            f"- Generado: `{report['generated_at']}`",
            f"- Archivo de entrada: `{report['input_file']}`",
            f"- Archivo de salida: `{report['output_file']}`",
            f"- Hoja principal: `{report['main_sheet']}`",
            f"- Filas: `{report['dimensions']['rows']}`",
            f"- Columnas: `{report['dimensions']['columns']}`",
            f"- Filas procesadas: `{report['processed_rows']}`",
            f"- Registros que requieren revision: `{report['review_rows']}`",
            f"- Registros D.M.: `{report['dm_count']}`",
            "",
            "## Columnas Auxiliares",
            "",
            _format_bullets(report["auxiliary_columns"]),
            "",
            "## Frecuencias",
            "",
            _format_counter(report["frequency_counts"]),
            "",
            "## Monedas Inferidas",
            "",
            _format_counter(report["currency_counts"]),
            "",
            "## Tipos de Poliza Probables",
            "",
            _format_counter(report["policy_counts"]),
            "",
            "## Motivos de Revision",
            "",
            _format_counter(report["review_reason_counts"]),
            "",
            "## Advertencias",
            "",
            _format_bullets(report["warnings"]),
            "",
            "## Recomendaciones",
            "",
            _format_bullets(report["recommendations"]),
            "",
        ]
    )


def _format_counter(counter: dict[str, int]) -> str:
    if not counter:
        return "- Sin datos registrados."
    return "\n".join(f"- `{key}`: `{value}`" for key, value in counter.items())


def _format_bullets(items: list[str]) -> str:
    if not items:
        return "- Sin registros."
    return "\n".join(f"- {item}" for item in items)


def _build_warnings(column_map: dict[str, int]) -> list[str]:
    warnings = ["La hoja principal fue seleccionada automaticamente y debe validarse manualmente."]
    if "policy" not in column_map:
        warnings.append("No se detecto columna de poliza con confianza suficiente.")
    if "frequency" not in column_map:
        warnings.append("No se detecto columna de vigencia/frecuencia con confianza suficiente.")
    if not {"due_day", "due_month", "due_year"}.issubset(column_map):
        warnings.append("No se detectaron completas las columnas separadas de dia, mes y ano.")
    return warnings


def _row_has_data(worksheet: Worksheet, row_index: int, max_original_column: int) -> bool:
    return any(not _is_empty(worksheet.cell(row=row_index, column=column).value) for column in range(1, max_original_column + 1))


def _cell_value(worksheet: Worksheet, row_index: int, column_index: int | None) -> Any:
    if not column_index:
        return None
    return worksheet.cell(row=row_index, column=column_index).value


def _is_empty(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")
