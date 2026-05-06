"""Utilidades de assets para la interfaz de escritorio."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon


APP_ICON_FILENAME = "app_icon.svg"


def assets_dir() -> Path:
    """Devuelve la carpeta de assets en desarrollo o dentro de un paquete PyInstaller."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / "assets"
    return Path(__file__).resolve().parents[2] / "assets"


def app_icon_path() -> Path:
    """Devuelve la ruta esperada del ícono de la aplicación."""
    return assets_dir() / APP_ICON_FILENAME


def load_app_icon() -> QIcon:
    """Carga el ícono de la aplicación si el asset está disponible."""
    icon_path = app_icon_path()
    if not icon_path.exists():
        return QIcon()
    return QIcon(str(icon_path))
