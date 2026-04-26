"""Initial PySide6 main window for workbook loading.

The window only shows a safe technical summary. It does not display workbook
rows, edit data, save files, or create reports.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app import __version__
from app.core.exceptions import GestorSegurosError
from app.domain.workbook_records import WorkbookLoadResult
from app.services.workbook_loader import load_modernized_workbook


LoaderCallable = Callable[[str | Path], WorkbookLoadResult]


class MainWindow(QMainWindow):
    """Main application window for the first visual workbook load."""

    def __init__(self, loader: LoaderCallable = load_modernized_workbook) -> None:
        super().__init__()
        self._loader = loader
        self._summary_labels: dict[str, QLabel] = {}
        self.setWindowTitle("Gestor de Seguros")
        self.setMinimumSize(820, 620)
        self._build_ui()
        self._connect_signals()
        self._set_initial_state()

    def _build_ui(self) -> None:
        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 12)
        root.setSpacing(14)

        title = QLabel("Gestor de Seguros")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(title)

        version = QLabel(f"Versión {__version__}")
        version.setObjectName("versionLabel")
        root.addWidget(version)

        helper = QLabel("Seleccione un workbook modernizado .xlsx para cargar un resumen seguro.")
        helper.setWordWrap(True)
        root.addWidget(helper)

        selector_group = QGroupBox("Workbook modernizado")
        selector_layout = QHBoxLayout(selector_group)
        self.path_edit = QLineEdit()
        self.path_edit.setObjectName("workbookPath")
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("Ningún workbook seleccionado")
        self.select_button = QPushButton("Seleccionar workbook")
        self.select_button.setObjectName("selectWorkbookButton")
        self.load_button = QPushButton("Cargar workbook")
        self.load_button.setObjectName("loadWorkbookButton")
        selector_layout.addWidget(self.path_edit, stretch=1)
        selector_layout.addWidget(self.select_button)
        selector_layout.addWidget(self.load_button)
        root.addWidget(selector_group)

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
            ("columnas", "Columnas detectadas"),
            ("gs_presentes", "Columnas GS presentes"),
            ("gs_faltantes", "Columnas GS faltantes"),
            ("estructura", "Estructura completa"),
        ):
            value = QLabel("-")
            value.setObjectName(f"summary_{key}")
            value.setWordWrap(True)
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            summary_layout.addRow(f"{label}:", value)
            self._summary_labels[key] = value
        root.addWidget(summary_group)

        warnings_group = QGroupBox("Advertencias")
        warnings_layout = QVBoxLayout(warnings_group)
        self.warnings_text = QTextEdit()
        self.warnings_text.setObjectName("warningsText")
        self.warnings_text.setReadOnly(True)
        self.warnings_text.setMinimumHeight(100)
        self.warnings_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        warnings_layout.addWidget(self.warnings_text)
        root.addWidget(warnings_group, stretch=1)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar(self))
        self._apply_style()

    def _connect_signals(self) -> None:
        self.select_button.clicked.connect(self.select_workbook)
        self.load_button.clicked.connect(self.load_selected_workbook)

    def _set_initial_state(self) -> None:
        self.statusBar().showMessage("Estado inicial: seleccione un workbook modernizado.")
        self.warnings_text.setPlainText("Sin advertencias.")

    def select_workbook(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar workbook modernizado",
            "",
            "Excel (*.xlsx)",
        )
        if path:
            self.path_edit.setText(path)
            self.statusBar().showMessage("Workbook seleccionado. Listo para cargar.")

    def load_selected_workbook(self) -> None:
        path = self.path_edit.text().strip()
        if not path:
            self._show_error("Debe seleccionar un workbook modernizado antes de cargar.")
            return

        try:
            result = self._loader(path)
        except GestorSegurosError as exc:
            self._show_error(str(exc))
            return

        self._show_summary(result)

    def _show_summary(self, result: WorkbookLoadResult) -> None:
        summary = result.summary
        self._summary_labels["archivo"].setText(summary.source_name)
        self._summary_labels["hoja"].setText(summary.sheet_name)
        self._summary_labels["filas_detectadas"].setText(str(summary.data_rows_detected))
        self._summary_labels["filas_cargadas"].setText(str(summary.records_loaded))
        self._summary_labels["filas_omitidas"].setText(str(summary.rows_skipped))
        self._summary_labels["columnas"].setText(f"{summary.total_columns}: {_format_items(summary.detected_columns)}")
        self._summary_labels["gs_presentes"].setText(_format_items(summary.gs_columns_present))
        self._summary_labels["gs_faltantes"].setText(_format_items(summary.gs_columns_missing))
        self._summary_labels["estructura"].setText("Sí" if summary.structure_complete else "No")
        self.warnings_text.setPlainText("\n".join(summary.warnings) if summary.warnings else "Sin advertencias.")

        if summary.structure_complete:
            self.statusBar().showMessage("Workbook cargado correctamente.")
        else:
            self.statusBar().showMessage("Workbook cargado con estructura incompleta.")

    def _show_error(self, message: str) -> None:
        self.warnings_text.setPlainText(message)
        self.statusBar().showMessage("No se pudo cargar el workbook.")

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background: #F6F7F9;
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
            QGroupBox {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                margin-top: 10px;
                padding: 12px;
                background: #FFFFFF;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
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
            QLineEdit, QTextEdit {
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px;
                background: #FFFFFF;
            }
            QStatusBar {
                color: #374151;
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
