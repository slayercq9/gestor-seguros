"""Initial PySide6 main window for Control Cartera loading.

The window shows a safe technical summary and a read-only table. It does not
edit data, save Excel files, create reports, search, or filter records.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app import __version__
from app.core.exceptions import GestorSegurosError
from app.domain.workbook_records import WorkbookLoadResult
from app.services.workbook_loader import load_modernized_workbook
from app.ui.table_model import RecordsTableModel


LoaderCallable = Callable[[str | Path], WorkbookLoadResult]
APP_DISPLAY_NAME = "Gestor de Seguros- Dagoberto Quirós Madriz"


class MainWindow(QMainWindow):
    """Main application window for visual Control Cartera loading."""

    def __init__(self, loader: LoaderCallable = load_modernized_workbook) -> None:
        super().__init__()
        self._loader = loader
        self._summary_labels: dict[str, QLabel] = {}
        self._summary_texts: dict[str, QPlainTextEdit] = {}
        self._records_model = RecordsTableModel()
        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setMinimumSize(1060, 740)
        self._build_ui()
        self._connect_signals()
        self._set_initial_state()

    def _build_ui(self) -> None:
        central = QWidget(self)
        central.setObjectName("mainContent")
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 12)
        root.setSpacing(14)

        title = QLabel(APP_DISPLAY_NAME)
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(title)

        version = QLabel(f"Versión {__version__}")
        version.setObjectName("versionLabel")
        root.addWidget(version)

        helper = QLabel("Seleccione un Control Cartera modernizado .xlsx para cargar un resumen seguro.")
        helper.setObjectName("helperText")
        helper.setWordWrap(True)
        root.addWidget(helper)

        root.addWidget(self._build_selector())

        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.tabs.addTab(self._build_summary_tab(), "Resumen")
        self.tabs.addTab(self._build_records_tab(), "Registros")
        root.addWidget(self.tabs, stretch=1)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar(self))
        self._apply_style()

    def _build_selector(self) -> QGroupBox:
        selector_group = QGroupBox("Control Cartera modernizado")
        selector_layout = QHBoxLayout(selector_group)
        self.path_edit = QLineEdit()
        self.path_edit.setObjectName("workbookPath")
        self.path_edit.setReadOnly(False)
        self.path_edit.setPlaceholderText("Ningún Control Cartera seleccionado")
        self.path_edit.setToolTip("Ruta local del Control Cartera modernizado en formato .xlsx.")
        self.select_button = QPushButton("Seleccionar Control Cartera")
        self.select_button.setObjectName("selectWorkbookButton")
        self.load_button = QPushButton("Cargar Control Cartera")
        self.load_button.setObjectName("loadWorkbookButton")
        selector_layout.addWidget(self.path_edit, stretch=1)
        selector_layout.addWidget(self.select_button)
        selector_layout.addWidget(self.load_button)
        return selector_group

    def _build_summary_tab(self) -> QScrollArea:
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("summaryScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("summaryContent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(14)

        summary_group = QGroupBox("Resumen de carga")
        summary_layout = QFormLayout(summary_group)
        summary_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        summary_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        for key, label in (
            ("archivo", "Archivo seleccionado"),
            ("hoja", "Hoja cargada"),
            ("filas_detectadas", "Filas detectadas"),
            ("filas_cargadas", "Filas cargadas"),
            ("filas_omitidas", "Filas omitidas"),
            ("estructura", "Estructura completa"),
        ):
            value = QLabel("-")
            value.setObjectName(f"summary_{key}")
            value.setWordWrap(True)
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            summary_layout.addRow(f"{label}:", value)
            self._summary_labels[key] = value

        for key, label in (
            ("columnas", "Columnas detectadas"),
            ("gs_presentes", "Columnas GS presentes"),
            ("gs_faltantes", "Columnas GS faltantes"),
        ):
            value = QPlainTextEdit()
            value.setObjectName(f"summary_{key}")
            value.setReadOnly(True)
            value.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
            value.setMinimumHeight(72)
            value.setMaximumHeight(140)
            value.setPlainText("-")
            value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            summary_layout.addRow(f"{label}:", value)
            self._summary_texts[key] = value
        layout.addWidget(summary_group)

        warnings_group = QGroupBox("Advertencias")
        warnings_layout = QVBoxLayout(warnings_group)
        self.warnings_text = QPlainTextEdit()
        self.warnings_text.setObjectName("warningsText")
        self.warnings_text.setReadOnly(True)
        self.warnings_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.warnings_text.setMinimumHeight(120)
        self.warnings_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        warnings_layout.addWidget(self.warnings_text)
        layout.addWidget(warnings_group, stretch=1)

        scroll_area.setWidget(content)
        return scroll_area

    def _build_records_tab(self) -> QWidget:
        tab = QWidget()
        tab.setObjectName("recordsTab")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.records_hint = QLabel("Cargue un Control Cartera para visualizar los registros.")
        self.records_hint.setObjectName("recordsHint")
        self.records_hint.setWordWrap(True)
        layout.addWidget(self.records_hint)

        counts_layout = QHBoxLayout()
        self.records_rows_label = QLabel("Filas cargadas: 0")
        self.records_rows_label.setObjectName("recordsRowsLabel")
        self.records_columns_label = QLabel("Columnas visibles: 0")
        self.records_columns_label.setObjectName("recordsColumnsLabel")
        counts_layout.addWidget(self.records_rows_label)
        counts_layout.addWidget(self.records_columns_label)
        counts_layout.addStretch(1)
        layout.addLayout(counts_layout)

        self.records_table = QTableView()
        self.records_table.setObjectName("recordsTable")
        self.records_table.setModel(self._records_model)
        self.records_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.records_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.records_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.records_table.setAlternatingRowColors(True)
        self.records_table.setWordWrap(False)
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.records_table.horizontalHeader().setStretchLastSection(False)
        self.records_table.verticalHeader().setDefaultSectionSize(24)
        layout.addWidget(self.records_table, stretch=1)

        note = QLabel("La tabla es de solo lectura en esta versión.")
        note.setObjectName("recordsReadonlyNote")
        layout.addWidget(note)
        return tab

    def _connect_signals(self) -> None:
        self.select_button.clicked.connect(self.select_workbook)
        self.load_button.clicked.connect(self.load_selected_workbook)

    def _set_initial_state(self) -> None:
        self.statusBar().showMessage("Estado inicial: seleccione un Control Cartera modernizado.")
        self.warnings_text.setPlainText("Sin advertencias.")
        self._clear_records()

    def select_workbook(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Control Cartera modernizado",
            "",
            "Excel (*.xlsx)",
        )
        if path:
            self.path_edit.setText(path)
            self.path_edit.setToolTip(path)
            self.statusBar().showMessage("Control Cartera seleccionado. Listo para cargar.")

    def load_selected_workbook(self) -> None:
        path = self.path_edit.text().strip()
        validation_error = self._validate_selected_path(path)
        if validation_error:
            self._show_error(validation_error)
            return

        try:
            result = self._loader(path)
        except GestorSegurosError as exc:
            self._show_error(
                "No fue posible cargar el Control Cartera. Revise que el archivo sea el modernizado.\n\n"
                f"Detalle: {exc}"
            )
            return

        self._show_summary(result)
        self._show_records(result)

    def _validate_selected_path(self, path: str) -> str | None:
        if not path:
            return "Seleccione un archivo Control Cartera en formato Excel (.xlsx)."

        selected_path = Path(path)
        if selected_path.suffix.lower() != ".xlsx":
            return "Formato no admitido. Seleccione un archivo Excel con extensión .xlsx."
        if not selected_path.exists() or not selected_path.is_file():
            return "El archivo seleccionado no existe."
        return None

    def _show_summary(self, result: WorkbookLoadResult) -> None:
        summary = result.summary
        self._summary_labels["archivo"].setText(summary.source_name)
        self._summary_labels["hoja"].setText(summary.sheet_name)
        self._summary_labels["filas_detectadas"].setText(str(summary.data_rows_detected))
        self._summary_labels["filas_cargadas"].setText(str(summary.records_loaded))
        self._summary_labels["filas_omitidas"].setText(str(summary.rows_skipped))
        self._summary_texts["columnas"].setPlainText(f"{summary.total_columns}: {_format_items(summary.detected_columns)}")
        self._summary_texts["gs_presentes"].setPlainText(_format_items(summary.gs_columns_present))
        self._summary_texts["gs_faltantes"].setPlainText(_format_items(summary.gs_columns_missing))
        self._summary_labels["estructura"].setText("Sí" if summary.structure_complete else "No")
        self.warnings_text.setPlainText("\n".join(summary.warnings) if summary.warnings else "Sin advertencias.")

        if summary.structure_complete:
            self.statusBar().showMessage("Control Cartera cargado correctamente.")
        else:
            self.statusBar().showMessage("Control Cartera cargado con estructura incompleta.")

    def _show_records(self, result: WorkbookLoadResult) -> None:
        headers = result.summary.detected_columns
        self._records_model.set_records(result.records, headers)
        self.records_rows_label.setText(f"Filas cargadas: {self._records_model.rowCount()}")
        self.records_columns_label.setText(f"Columnas visibles: {self._records_model.columnCount()}")
        if self._records_model.rowCount() == 0:
            self.records_hint.setText("No hay registros cargados para mostrar.")
        else:
            self.records_hint.setText("Registros cargados")
        self.tabs.setCurrentIndex(1)

    def _clear_records(self) -> None:
        self._records_model.clear()
        self.records_rows_label.setText("Filas cargadas: 0")
        self.records_columns_label.setText("Columnas visibles: 0")
        self.records_hint.setText("Cargue un Control Cartera para visualizar los registros.")

    def _show_error(self, message: str) -> None:
        self._clear_records()
        self.warnings_text.setPlainText(message)
        self.statusBar().showMessage("No se pudo cargar el Control Cartera.")

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background: #F6F7F9;
                color: #111827;
            }
            QWidget {
                color: #111827;
                background: #F6F7F9;
            }
            QScrollArea#summaryScrollArea, QWidget#mainContent, QWidget#summaryContent {
                background: #F6F7F9;
            }
            QLabel {
                color: #111827;
            }
            QLabel#appTitle {
                font-size: 24px;
                font-weight: 700;
                color: #1F2937;
            }
            QLabel#versionLabel {
                color: #4B5563;
                font-weight: 600;
            }
            QLabel#helperText, QLabel#recordsHint, QLabel#recordsReadonlyNote {
                color: #374151;
            }
            QGroupBox {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                margin-top: 10px;
                padding: 12px;
                background: #FFFFFF;
                color: #111827;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
                color: #111827;
                background: #FFFFFF;
            }
            QTabWidget::pane {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                background: #FFFFFF;
            }
            QTabBar::tab {
                background: #E5E7EB;
                color: #111827;
                padding: 8px 14px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                font-weight: 600;
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #1F6FEB;
                background: #1F6FEB;
                color: #FFFFFF;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #1A5FCC;
            }
            QLineEdit, QPlainTextEdit, QTableView {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px;
                background: #FFFFFF;
                color: #111827;
                selection-background-color: #BFDBFE;
                selection-color: #111827;
            }
            QLineEdit {
                min-height: 34px;
            }
            QPlainTextEdit {
                font-family: Consolas, "Courier New", monospace;
                font-size: 12px;
            }
            QHeaderView::section {
                background: #E5E7EB;
                color: #111827;
                border: 1px solid #D1D5DB;
                padding: 4px;
                font-weight: 600;
            }
            QStatusBar {
                color: #374151;
                background: #F6F7F9;
            }
            """
        )


def _format_items(items: tuple[str, ...]) -> str:
    if not items:
        return "ninguna"
    return ", ".join(items)


def run_gui(argv: list[str] | None = None) -> int:
    """Run the PySide6 application."""
    app = QApplication.instance() or QApplication(argv if argv is not None else sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()
