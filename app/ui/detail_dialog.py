"""Diálogo modal de solo lectura para revisar el detalle de un registro."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.detail_model import RecordDetailModel
from app.ui.theme import build_stylesheet


class RecordDetailDialog(QDialog):
    """Muestra campos con información del registro seleccionado sin permitir edición."""

    def __init__(
        self,
        record: WorkbookRowRecord,
        headers: tuple[str, ...],
        theme: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Detalle del registro")
        self.setMinimumSize(640, 420)
        self._model = RecordDetailModel()
        self._model.set_record(record, headers)
        self._build_ui()
        self.setStyleSheet(build_stylesheet(theme))

    @property
    def detail_model(self) -> RecordDetailModel:
        """Modelo de solo lectura usado por la tabla del detalle."""
        return self._model

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        self.empty_label = QLabel("No hay campos con información para este registro.")
        self.empty_label.setObjectName("recordDetailEmpty")
        self.empty_label.setWordWrap(True)
        self.empty_label.setVisible(self._model.rowCount() == 0)
        layout.addWidget(self.empty_label)

        self.detail_table = QTableView()
        self.detail_table.setObjectName("recordDetailDialogTable")
        self.detail_table.setModel(self._model)
        self.detail_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.detail_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.detail_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.detail_table.setAlternatingRowColors(True)
        self.detail_table.setVisible(self._model.rowCount() > 0)
        self.detail_table.verticalHeader().setDefaultSectionSize(24)
        self.detail_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.detail_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.detail_table, stretch=1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.setObjectName("recordDetailCloseButtons")
        buttons.button(QDialogButtonBox.StandardButton.Close).setText("Cerrar")
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, alignment=Qt.AlignmentFlag.AlignRight)
