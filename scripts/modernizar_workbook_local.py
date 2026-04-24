"""Comando local para generar una copia modernizada del workbook operativo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.exceptions import GestorSegurosError
from app.services.workbook_modernizer import modernize_workbook


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera una copia local modernizada del workbook operativo."
    )
    parser.add_argument("input_path", help="Ruta del workbook original.")
    parser.add_argument("output_dir", help="Carpeta local donde se guardaran la copia y reportes.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = modernize_workbook(Path(args.input_path), Path(args.output_dir))
    except GestorSegurosError as exc:
        print(f"Error de modernizacion: {exc}")
        return 1

    print("Workbook modernizado generado.")
    print(f"- {result.output_workbook}")
    print(f"- {result.markdown_report}")
    print(f"- {result.json_report}")
    print(f"- {result.review_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
