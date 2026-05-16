"""Vista embebida de solo lectura para vencimientos calculados."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
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


class ExpirationView(QWidget):
    """Presenta vencimientos base dentro de la ventana principal."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("expirationTab")
        self._model = ExpirationTableModel()
        self._summary_labels: dict[str, QLabel] = {}
        self._build_ui()
        self.refresh_records(())

    @property
    def expiration_model(self) -> ExpirationTableModel:
        """Modelo de solo lectura usado por la tabla de vencimientos."""
        return self._model

    def refresh_records(self, records: tuple[WorkbookRowRecord, ...]) -> None:
        """Recalcula vencimientos desde registros cargados en memoria."""
        rows = build_expiration_rows(records, alert_days=30)
        summary = summarize_expiration_rows(rows)
        self._model.set_rows(rows)
        self._summary_labels["total"].setText(str(summary.total))
        self._summary_labels["vigentes"].setText(str(summary.active))
        self._summary_labels["proximas"].setText(str(summary.expiring_soon))
        self._summary_labels["vencidas"].setText(str(summary.expired))
        self._summary_labels["invalidas"].setText(str(summary.invalid_date))
        self._summary_labels["no_aplica"].setText(str(summary.notice_not_applicable))
        has_rows = bool(rows)
        self.empty_label.setVisible(not has_rows)
        self.expiration_table.setVisible(has_rows)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 10)
        layout.setSpacing(12)

        title = QLabel("Vencimientos base")
        title.setObjectName("expirationTitle")
        layout.addWidget(title)

        summary_group = QGroupBox("Resumen de vencimientos")
        summary_layout = QGridLayout(summary_group)
        summary_layout.setContentsMargins(12, 16, 12, 12)
        summary_layout.setHorizontalSpacing(18)
        summary_layout.setVerticalSpacing(8)
        for index, (key, label) in enumerate(
            (
                ("total", "Total evaluadas"),
                ("vigentes", "Vigentes"),
                ("proximas", "Próximas a vencer"),
                ("vencidas", "Vencidas"),
                ("invalidas", "Sin fecha válida"),
                ("no_aplica", "No aplica aviso"),
            )
        ):
            label_widget = QLabel(f"{label}:")
            label_widget.setObjectName("expirationSummaryLabel")
            value_widget = QLabel("0")
            value_widget.setObjectName(f"expirationSummary_{key}")
            value_widget.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row = index // 3
            column = (index % 3) * 2
            summary_layout.addWidget(label_widget, row, column)
            summary_layout.addWidget(value_widget, row, column + 1)
            self._summary_labels[key] = value_widget
        layout.addWidget(summary_group)

        self.empty_label = QLabel("Cargue un Control Cartera para evaluar vencimientos.")
        self.empty_label.setObjectName("expirationEmptyLabel")
        self.empty_label.setWordWrap(True)
        self.empty_label.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self.empty_label)

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
