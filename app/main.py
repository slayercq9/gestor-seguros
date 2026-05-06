"""Punto de entrada de la aplicación.

Por defecto este módulo inicia la GUI de escritorio. El modo `--check` queda
disponible para diagnósticos técnicos y pruebas rápidas automatizadas.
"""

from __future__ import annotations

import argparse

from app.bootstrap import bootstrap_application


def main(argv: list[str] | None = None) -> int:
    """Inicia la GUI o ejecuta un chequeo técnico no invasivo."""
    parser = argparse.ArgumentParser(description="Gestor de Seguros")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ejecuta un chequeo técnico sin abrir la interfaz gráfica.",
    )
    args = parser.parse_args(argv)

    if args.check:
        result = bootstrap_application()
        print(result.status_message)
        return 0

    from app.ui.main_window import run_gui

    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())
