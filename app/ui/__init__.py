"""Paquete de interfaz de usuario para gestor-seguros."""

from app.ui.main_window import MainWindow, run_gui
from app.ui.filter_proxy_model import RecordsFilterProxyModel
from app.ui.table_model import RecordsTableModel

__all__ = ["MainWindow", "RecordsFilterProxyModel", "RecordsTableModel", "run_gui"]
