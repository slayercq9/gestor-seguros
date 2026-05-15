"""Diálogo de solo lectura para revisar vencimientos calculados."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.expiration_table_model import (
    ExpirationTableModel,
    build_expiration_rows,
    summarize_expiration_rows,
)
from app.ui.theme import build_stylesheet


class ExpirationDialog(QDialog):
    """Muestra vencimientos base calculados sin modificar datos."""

    def __init__(
        self,
        records: tuple[WorkbookRowRecord, ...],
        theme: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Vencimientos")
        self.setMinimumSize(980, 540)
        self._rows = build_expiration_rows(records, alert_days=30)
        self._summary = summarize_expiration_rows(self._rows)
        self._model = ExpirationTableModel(self._rows)
        self._build_ui()
        self.setStyleSheet(build_stylesheet(theme))

    @property
    def expiration_model(self) -> ExpirationTableModel:
        """Modelo de solo lectura usado por la tabla de vencimientos."""
        return self._model

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        title = QLabel("Vencimientos base")
        title.setObjectName("expirationDialogTitle")
        layout.addWidget(title)

        summary_group = QGroupBox("Resumen de vencimientos")
        summary_layout = QGridLayout(summary_group)
        summary_layout.setContentsMargins(12, 16, 12, 12)
        summary_layout.setHorizontalSpacing(18)
        summary_layout.setVerticalSpacing(8)
        for index, (label, value) in enumerate(
            (
                ("Total evaluadas", self._summary.total),
                ("Vigentes", self._summary.active),
                ("Próximas a vencer", self._summary.expiring_soon),
                ("Vencidas", self._summary.expired),
                ("Sin fecha válida", self._summary.invalid_date),
                ("No aplica aviso", self._summary.notice_not_applicable),
            )
        ):
            label_widget = QLabel(f"{label}:")
            label_widget.setObjectName("expirationSummaryLabel")
            value_widget = QLabel(str(value))
            value_widget.setObjectName("expirationSummaryValue")
            value_widget.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row = index // 3
            column = (index % 3) * 2
            summary_layout.addWidget(label_widget, row, column)
            summary_layout.addWidget(value_widget, row, column + 1)
        layout.addWidget(summary_group)

        self.expiration_table = QTableView()
        self.expiration_table.setObjectName("expirationTable")
        self.expiration_table.setModel(self._model)
        self.expiration_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.expiration_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.expiration_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.expiration_table.setAlternatingRowColors(True)
        self.expiration_table.setWordWrap(False)
        self.expiration_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.expiration_table.horizontalHeader().setStretchLastSection(True)
        self.expiration_table.verticalHeader().setDefaultSectionSize(24)
        layout.addWidget(self.expiration_table, stretch=1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.setObjectName("expirationCloseButtons")
        buttons.button(QDialogButtonBox.StandardButton.Close).setText("Cerrar")
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, alignment=Qt.AlignmentFlag.AlignRight)
