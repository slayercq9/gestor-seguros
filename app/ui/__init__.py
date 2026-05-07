"""Paquete de interfaz de usuario para gestor-seguros."""

from app.ui.main_window import MainWindow, run_gui
from app.ui.audit_table_model import AuditTableModel
from app.ui.detail_dialog import RecordDetailDialog
from app.ui.detail_model import RecordDetailModel
from app.ui.edit_dialog import RecordEditDialog
from app.ui.filter_proxy_model import RecordsFilterProxyModel
from app.ui.table_model import RecordsTableModel

__all__ = [
    "MainWindow",
    "AuditTableModel",
    "RecordDetailDialog",
    "RecordDetailModel",
    "RecordEditDialog",
    "RecordsFilterProxyModel",
    "RecordsTableModel",
    "run_gui",
]
