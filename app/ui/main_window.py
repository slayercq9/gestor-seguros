"""Initial PySide6 main window for Control Cartera loading.

The window shows a safe technical summary and a read-only table. It does not
edit data, save Excel files, create reports, search, or filter records.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
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
from app.services.workbook_loader import get_default_control_cartera_path, load_control_cartera
from app.ui.table_model import RecordsTableModel
from app.ui.theme import DARK_THEME, LIGHT_THEME, THEME_SETTING_KEY, build_stylesheet, normalize_theme, theme_label


LoaderCallable = Callable[[str | Path], WorkbookLoadResult]
APP_DISPLAY_NAME = "Gestor de Seguros- Dagoberto Quirós Madriz"


class MainWindow(QMainWindow):
    """Main application window for visual Control Cartera loading."""

    def __init__(
        self,
        loader: LoaderCallable = load_control_cartera,
        default_path: str | Path | None = None,
        show_dialogs: bool = True,
        settings: QSettings | None = None,
    ) -> None:
        super().__init__()
        self._loader = loader
        self._default_path = Path(default_path) if default_path is not None else get_default_control_cartera_path()
        self._show_dialogs = show_dialogs
        self._settings = settings if settings is not None else QSettings("GestorSeguros", "GestorSeguros")
        self._current_theme = normalize_theme(self._settings.value(THEME_SETTING_KEY, LIGHT_THEME))
        self._summary_labels: dict[str, QLabel] = {}
        self._summary_texts: dict[str, QPlainTextEdit] = {}
        self._records_model = RecordsTableModel()
        self._last_user_message = ""
        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setMinimumSize(1060, 740)
        self._build_ui()
        self._connect_signals()
        self._set_initial_state()

    @property
    def last_user_message(self) -> str:
        """Last non-sensitive message shown or prepared for the user."""
        return self._last_user_message

    @property
    def current_theme(self) -> str:
        """Current visual theme name."""
        return self._current_theme

    def _build_ui(self) -> None:
        central = QWidget(self)
        central.setObjectName("mainContent")
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 12)
        root.setSpacing(14)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)

        title_block = QVBoxLayout()
        title = QLabel(APP_DISPLAY_NAME)
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_block.addWidget(title)

        version = QLabel(f"Versión {__version__}")
        version.setObjectName("versionLabel")
        title_block.addWidget(version)
        header_layout.addLayout(title_block, stretch=1)
        header_layout.addWidget(self._build_theme_control())
        root.addLayout(header_layout)

        helper = QLabel("Use el Control Cartera predeterminado o seleccione otro archivo .xlsx.")
        helper.setObjectName("helperText")
        helper.setWordWrap(True)
        root.addWidget(helper)

        root.addWidget(self._build_selector())

        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.tabs.addTab(self._build_records_tab(), "Registros")
        self.tabs.addTab(self._build_summary_tab(), "Resumen")
        root.addWidget(self.tabs, stretch=1)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar(self))
        self._apply_style()

    def _build_theme_control(self) -> QWidget:
        theme_box = QWidget()
        theme_layout = QHBoxLayout(theme_box)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(8)

        theme_label_widget = QLabel("Tema:")
        theme_label_widget.setObjectName("themeLabel")
        self.theme_selector = QComboBox()
        self.theme_selector.setObjectName("themeSelector")
        self.theme_selector.setToolTip("Cambia entre tema claro y tema oscuro.")
        self.theme_selector.addItem(theme_label(LIGHT_THEME), LIGHT_THEME)
        self.theme_selector.addItem(theme_label(DARK_THEME), DARK_THEME)
        self._sync_theme_selector()

        theme_layout.addWidget(theme_label_widget)
        theme_layout.addWidget(self.theme_selector)
        return theme_box

    def _build_selector(self) -> QGroupBox:
        selector_group = QGroupBox("Control Cartera")
        selector_layout = QHBoxLayout(selector_group)
        self.path_edit = QLineEdit()
        self.path_edit.setObjectName("workbookPath")
        self.path_edit.setReadOnly(False)
        self.path_edit.setPlaceholderText("Ruta del Control Cartera")
        self.path_edit.setToolTip("Ruta local del Control Cartera en formato .xlsx.")
        self.select_button = QPushButton("Seleccionar Control Cartera")
        self.select_button.setObjectName("selectWorkbookButton")
        self.default_button = QPushButton("Cargar predeterminado")
        self.default_button.setObjectName("loadDefaultControlButton")
        self.default_button.setToolTip("Carga data/input/CONTROLCARTERA_V2.xlsx sin modificarlo.")
        selector_layout.addWidget(self.path_edit, stretch=1)
        selector_layout.addWidget(self.select_button)
        selector_layout.addWidget(self.default_button)
        return selector_group

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
            ("filas_utiles", "Filas útiles detectadas"),
            ("filas_cargadas", "Filas cargadas"),
            ("filas_omitidas", "Filas omitidas o vacías"),
            ("columnas_visibles", "Columnas visibles"),
            ("modo", "Modo"),
            ("estado", "Estado de carga"),
        ):
            value = QLabel("-")
            value.setObjectName(f"summary_{key}")
            value.setWordWrap(True)
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            summary_layout.addRow(f"{label}:", value)
            self._summary_labels[key] = value

        value = QPlainTextEdit()
        value.setObjectName("summary_columnas")
        value.setReadOnly(True)
        value.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        value.setMinimumHeight(96)
        value.setMaximumHeight(180)
        value.setPlainText("-")
        value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        summary_layout.addRow("Columnas visibles:", value)
        self._summary_texts["columnas"] = value
        layout.addWidget(summary_group)

        layout.addStretch(1)

        scroll_area.setWidget(content)
        return scroll_area

    def _connect_signals(self) -> None:
        self.select_button.clicked.connect(self.select_workbook)
        self.default_button.clicked.connect(self.load_default_control_cartera)
        self.path_edit.returnPressed.connect(self.load_selected_workbook)
        self.theme_selector.currentIndexChanged.connect(self.change_theme)

    def _set_initial_state(self) -> None:
        self._set_selected_path(str(self._default_path), "Ruta predeterminada lista para cargar.")
        self._clear_records()

    def select_workbook(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Control Cartera",
            "",
            "Excel (*.xlsx)",
        )
        if not path:
            return

        self._set_selected_path(path, "Control Cartera seleccionado. Cargando...")
        self.load_selected_workbook()

    def load_default_control_cartera(self) -> None:
        """Load the default operational source from data/input."""
        self._set_selected_path(str(self._default_path), "Cargando Control Cartera predeterminado...")
        self.load_selected_workbook()

    def _set_selected_path(self, path: str, status_message: str) -> None:
        self.path_edit.setText(path)
        self.path_edit.setToolTip(path)
        self._last_user_message = status_message
        self.statusBar().showMessage(status_message)

    def load_selected_workbook(self) -> None:
        path = self.path_edit.text().strip()
        validation_error = self._validate_selected_path(path)
        if validation_error:
            self._show_error(validation_error)
            return

        try:
            result = self._loader(path)
        except GestorSegurosError:
            self._show_error("No fue posible cargar el Control Cartera. Revise la estructura del archivo.")
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
        self._summary_labels["filas_utiles"].setText(str(summary.useful_rows_detected))
        self._summary_labels["filas_cargadas"].setText(str(summary.records_loaded))
        self._summary_labels["filas_omitidas"].setText(str(summary.rows_skipped))
        self._summary_labels["columnas_visibles"].setText(str(len(summary.visible_columns)))
        self._summary_labels["modo"].setText("Solo lectura" if summary.read_only else "Editable")
        self._summary_labels["estado"].setText("Cargado correctamente")
        self._summary_texts["columnas"].setPlainText(_format_items(summary.visible_columns))
        self._last_user_message = "Control Cartera cargado correctamente."
        self.statusBar().showMessage("Control Cartera cargado correctamente.")

    def _show_records(self, result: WorkbookLoadResult) -> None:
        headers = result.summary.visible_columns
        self._records_model.set_records(result.records, headers)
        self.records_rows_label.setText(f"Filas cargadas: {self._records_model.rowCount()}")
        self.records_columns_label.setText(f"Columnas visibles: {self._records_model.columnCount()}")
        if self._records_model.rowCount() == 0:
            self.records_hint.setText("No hay registros cargados para mostrar.")
        else:
            self.records_hint.setText("Registros cargados")
        self.tabs.setCurrentIndex(0)

    def _clear_records(self) -> None:
        self._records_model.clear()
        self.records_rows_label.setText("Filas cargadas: 0")
        self.records_columns_label.setText("Columnas visibles: 0")
        self.records_hint.setText("Cargue un Control Cartera para visualizar los registros.")

    def _show_error(self, message: str) -> None:
        self._clear_records()
        self._summary_labels["estado"].setText("Error de carga")
        self._last_user_message = message
        self.statusBar().showMessage("No se pudo cargar el Control Cartera.")
        if self._show_dialogs:
            QMessageBox.warning(self, "Control Cartera", message)

    def change_theme(self) -> None:
        """Apply and persist the theme selected by the user."""
        self.apply_theme(self.theme_selector.currentData(), persist=True)

    def apply_theme(self, theme: str, persist: bool = False, update_status: bool = True) -> None:
        """Apply a supported visual theme without touching loaded records."""
        self._current_theme = normalize_theme(theme)
        self._sync_theme_selector()
        self.setStyleSheet(build_stylesheet(self._current_theme))
        if persist:
            self._settings.setValue(THEME_SETTING_KEY, self._current_theme)
            self._settings.sync()
        if update_status:
            message = f"{theme_label(self._current_theme)} aplicado."
            self._last_user_message = message
            self.statusBar().showMessage(message)

    def _sync_theme_selector(self) -> None:
        if not hasattr(self, "theme_selector"):
            return
        for index in range(self.theme_selector.count()):
            if self.theme_selector.itemData(index) == self._current_theme:
                previous = self.theme_selector.blockSignals(True)
                self.theme_selector.setCurrentIndex(index)
                self.theme_selector.blockSignals(previous)
                return

    def _apply_style(self) -> None:
        self.apply_theme(self._current_theme, persist=False, update_status=False)


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
