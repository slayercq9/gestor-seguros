"""Asset helpers for the desktop interface."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon


APP_ICON_FILENAME = "app_icon.svg"


def assets_dir() -> Path:
    """Return the assets directory in development or a PyInstaller bundle."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / "assets"
    return Path(__file__).resolve().parents[2] / "assets"


def app_icon_path() -> Path:
    """Return the expected application icon path."""
    return assets_dir() / APP_ICON_FILENAME


def load_app_icon() -> QIcon:
    """Load the application icon if the asset is available."""
    icon_path = app_icon_path()
    if not icon_path.exists():
        return QIcon()
    return QIcon(str(icon_path))
