"""Application entry point.

By default this module starts the desktop GUI. A small `--check` mode remains
available for technical diagnostics and automated smoke tests.
"""

from __future__ import annotations

import argparse

from app.bootstrap import bootstrap_application


def main(argv: list[str] | None = None) -> int:
    """Start the GUI or run a non-invasive technical check."""
    parser = argparse.ArgumentParser(description="Gestor de Seguros")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ejecuta un chequeo tecnico sin abrir la interfaz grafica.",
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
