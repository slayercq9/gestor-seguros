"""Local command for controlled loading of a modernized workbook.

The command prints only a technical summary. It does not print row values,
create output files, save the workbook, or run business workflows.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.exceptions import GestorSegurosError
from app.services.workbook_loader import load_modernized_workbook


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Carga segura de workbook modernizado.")
    parser.add_argument("workbook_path", help="Ruta exacta del workbook modernizado .xlsx.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = load_modernized_workbook(args.workbook_path)
    except GestorSegurosError as exc:
        print(f"Error de carga controlada: {exc}")
        return 1

    summary = result.summary
    print("Carga controlada completada.")
    print(f"- Archivo: {summary.source_name}")
    print(f"- Hoja cargada: {summary.sheet_name}")
    print(f"- Fila de encabezados: {summary.header_row}")
    print(f"- Filas utiles detectadas: {summary.useful_rows_detected}")
    print(f"- Filas cargadas: {summary.records_loaded}")
    print(f"- Filas omitidas o vacias: {summary.rows_skipped}")
    print(f"- Columnas visibles ({len(summary.visible_columns)}): {_format_items(summary.visible_columns)}")
    print(f"- Modo: {'solo lectura' if summary.read_only else 'editable'}")
    print(f"- Advertencias: {_format_items(summary.warnings)}")
    return 0


def _format_items(items: tuple[str, ...]) -> str:
    if not items:
        return "ninguna"
    return ", ".join(items)


if __name__ == "__main__":
    raise SystemExit(main())
