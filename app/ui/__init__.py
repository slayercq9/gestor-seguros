"""User interface package for gestor-seguros."""

from app.ui.main_window import MainWindow, run_gui
from app.ui.table_model import RecordsTableModel

__all__ = ["MainWindow", "RecordsTableModel", "run_gui"]
