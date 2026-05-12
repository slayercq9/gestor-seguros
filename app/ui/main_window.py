"""Ventana principal en PySide6 para cargar y revisar el Control Cartera.

La ventana muestra un resumen técnico seguro, una tabla de solo lectura y
búsqueda local sobre registros cargados. Los cambios se editan en memoria y
solo se exportan mediante `Guardar como`.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QSettings, QSignalBlocker, Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QFileDialog,
    QComboBox,
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
from app.core.paths import get_project_paths
from app.domain.audit_log import build_audit_entries
from app.domain.column_standards import (
    DETAIL,
    DUE_DAY,
    DUE_MONTH,
    DUE_YEAR,
    EMAIL,
    IDENTIFICATION,
    INSURED_AMOUNT,
    INSURED_NAME,
    ISSUE_DATE,
    PHONE,
    POLICY_NUMBER,
    POLICY_TYPE,
    PREMIUM,
    TERM,
    resolve_column_key,
)
from app.domain.workbook_records import WorkbookLoadResult
from app.services.workbook_loader import get_default_control_cartera_path, load_control_cartera
from app.services.workbook_saver import WorkbookCellUpdate, save_control_cartera_as
from app.ui.assets import load_app_icon
from app.ui.audit_table_model import AuditTableModel
from app.ui.detail_dialog import RecordDetailDialog
from app.ui.edit_dialog import RecordEditDialog
from app.ui.filter_proxy_model import ALL_COLUMNS_INDEX, RecordsFilterProxyModel
from app.ui.table_model import RecordsTableModel
from app.ui.theme import DARK_THEME, LIGHT_THEME, THEME_SETTING_KEY, build_stylesheet, next_theme, normalize_theme, theme_label


LoaderCallable = Callable[[str | Path], WorkbookLoadResult]
SaverCallable = Callable[..., Path]
APP_DISPLAY_NAME = "Gestor de Seguros- Dagoberto Quirós Madriz"
_COLUMN_WIDTH_RULES: dict[str, tuple[int, int]] = {
    "nº póliza": (140, 220),
    "n° póliza": (140, 220),
    "no. póliza": (140, 220),
    "nombre del asegurado": (220, 320),
    "cédula": (130, 220),
    "nº placa / finca": (130, 220),
    "n° placa / finca": (130, 220),
    "emisión": (110, 180),
    "vigencia": (100, 180),
    "día": (70, 110),
    "mes": (70, 110),
    "año": (80, 120),
    "monto asegurado": (130, 240),
    "prima": (100, 180),
    "teléfono": (140, 240),
    "correo": (200, 320),
    "tipo de póliza": (150, 260),
    "detalle": (200, 360),
}
_DEFAULT_COLUMN_WIDTH = (100, 240)
_COLUMN_WIDTH_SAMPLE_ROWS = 80
_COLUMN_WIDTH_RULES.update(
    {
        POLICY_NUMBER: (140, 220),
        INSURED_NAME: (220, 320),
        IDENTIFICATION: (130, 220),
        ISSUE_DATE: (110, 180),
        TERM: (100, 180),
        DUE_DAY: (70, 110),
        DUE_MONTH: (70, 110),
        DUE_YEAR: (80, 120),
        INSURED_AMOUNT: (130, 240),
        PREMIUM: (100, 180),
        PHONE: (140, 240),
        EMAIL: (200, 320),
        POLICY_TYPE: (150, 260),
        DETAIL: (200, 360),
    }
)


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación para la carga visual del Control Cartera."""

    def __init__(
        self,
        loader: LoaderCallable = load_control_cartera,
        saver: SaverCallable = save_control_cartera_as,
        default_path: str | Path | None = None,
        show_dialogs: bool = True,
        settings: QSettings | None = None,
    ) -> None:
        super().__init__()
        self._loader = loader
        self._saver = saver
        self._default_path = Path(default_path) if default_path is not None else get_default_control_cartera_path()
        self._show_dialogs = show_dialogs
        self._settings = settings if settings is not None else QSettings("GestorSeguros", "GestorSeguros")
        self._current_theme = normalize_theme(self._settings.value(THEME_SETTING_KEY, LIGHT_THEME))
        self._summary_labels: dict[str, QLabel] = {}
        self._summary_texts: dict[str, QPlainTextEdit] = {}
        self._records_model = RecordsTableModel()
        self._records_filter_model = RecordsFilterProxyModel()
        self._records_filter_model.setSourceModel(self._records_model)
        self._audit_model = AuditTableModel()
        self._last_user_message = ""
        self._current_source_path: Path | None = None
        self._current_result: WorkbookLoadResult | None = None
        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setWindowIcon(load_app_icon())
        self.setMinimumSize(1060, 740)
        self._build_ui()
        self._connect_signals()
        self._set_initial_state()

    @property
    def last_user_message(self) -> str:
        """Último mensaje no sensible mostrado o preparado para el usuario."""
        return self._last_user_message

    @property
    def current_theme(self) -> str:
        """Nombre del tema visual actual."""
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
        self.tabs.addTab(self._build_audit_tab(), "Bitácora")
        root.addWidget(self.tabs, stretch=1)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar(self))
        self._apply_style()

    def _build_theme_control(self) -> QWidget:
        theme_box = QWidget()
        theme_layout = QHBoxLayout(theme_box)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        self.theme_button = QPushButton()
        self.theme_button.setObjectName("themeToggleButton")
        self.theme_button.setToolTip("Cambiar tema")
        self.theme_button.setFixedSize(38, 34)
        self._sync_theme_control()
        theme_layout.addWidget(self.theme_button)
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
        self.save_as_button = QPushButton("Guardar como")
        self.save_as_button.setObjectName("saveAsButton")
        self.save_as_button.setToolTip("Guarda una copia .xlsx sin sobrescribir el archivo cargado.")
        selector_layout.addWidget(self.path_edit, stretch=1)
        selector_layout.addWidget(self.select_button)
        selector_layout.addWidget(self.default_button)
        selector_layout.addWidget(self.save_as_button)
        return selector_group

    def _build_search_controls(self) -> QWidget:
        search_group = QWidget()
        search_group.setObjectName("searchBar")
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(10, 8, 10, 8)
        search_layout.setSpacing(10)

        search_label = QLabel("Buscar")
        search_label.setObjectName("searchLabel")
        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("recordsSearchText")
        self.search_edit.setPlaceholderText("Buscar por cliente, identificación, póliza, placa, correo, teléfono...")
        self.search_edit.setClearButtonEnabled(True)

        column_label = QLabel("Buscar en")
        column_label.setObjectName("searchColumnLabel")
        self.search_column_combo = QComboBox()
        self.search_column_combo.setObjectName("recordsSearchColumn")
        self.search_column_combo.setMinimumWidth(190)

        self.clear_search_button = QPushButton("Limpiar")
        self.clear_search_button.setObjectName("clearSearchButton")
        self.clear_search_button.setMaximumWidth(84)

        self.search_results_label = QLabel("Mostrando 0 de 0 registros")
        self.search_results_label.setObjectName("searchResultsLabel")
        self.search_results_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.search_results_label.setMinimumWidth(190)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit, stretch=1)
        search_layout.addWidget(column_label)
        search_layout.addWidget(self.search_column_combo)
        search_layout.addWidget(self.clear_search_button)
        search_layout.addWidget(self.search_results_label)
        return search_group

    def _build_records_tab(self) -> QWidget:
        tab = QWidget()
        tab.setObjectName("recordsTab")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 10)
        layout.setSpacing(12)

        self.records_hint = QLabel("Cargue un Control Cartera para visualizar los registros.")
        self.records_hint.setObjectName("recordsHint")
        self.records_hint.setWordWrap(True)
        layout.addWidget(self.records_hint)
        layout.addWidget(self._build_search_controls())

        counts_panel = QWidget()
        counts_panel.setObjectName("recordsCountsPanel")
        counts_layout = QHBoxLayout(counts_panel)
        counts_layout.setContentsMargins(10, 6, 10, 6)
        counts_layout.setSpacing(16)
        self.records_rows_label = QLabel("Filas cargadas: 0")
        self.records_rows_label.setObjectName("recordsRowsLabel")
        self.records_columns_label = QLabel("Columnas visibles: 0")
        self.records_columns_label.setObjectName("recordsColumnsLabel")
        self.pending_changes_label = QLabel("Cambios pendientes: 0")
        self.pending_changes_label.setObjectName("pendingChangesLabel")
        counts_layout.addWidget(self.records_rows_label)
        counts_layout.addWidget(self.records_columns_label)
        counts_layout.addWidget(self.pending_changes_label)
        counts_layout.addStretch(1)
        layout.addWidget(counts_panel)

        self.records_table = QTableView()
        self.records_table.setObjectName("recordsTable")
        self.records_table.setModel(self._records_filter_model)
        self.records_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.records_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.records_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.records_table.setAlternatingRowColors(True)
        self.records_table.setWordWrap(False)
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.records_table.horizontalHeader().setStretchLastSection(False)
        self.records_table.horizontalHeader().setSectionsMovable(False)
        self.records_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.records_table.verticalHeader().setDefaultSectionSize(24)
        layout.addWidget(self.records_table, stretch=1)

        note = QLabel("La tabla es de solo lectura en esta versión.")
        note.setObjectName("recordsReadonlyNote")
        note.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(note)
        return tab

    def _build_audit_tab(self) -> QWidget:
        tab = QWidget()
        tab.setObjectName("auditTab")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 10)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()
        title = QLabel("Cambios pendientes en memoria")
        title.setObjectName("auditTitle")
        self.audit_count_label = QLabel("Cambios registrados: 0")
        self.audit_count_label.setObjectName("auditCountLabel")
        self.audit_count_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        header_layout.addWidget(self.audit_count_label)
        layout.addLayout(header_layout)

        self.audit_empty_label = QLabel("No hay cambios registrados en esta sesión.")
        self.audit_empty_label.setObjectName("auditEmptyLabel")
        self.audit_empty_label.setWordWrap(True)
        self.audit_empty_label.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self.audit_empty_label)

        self.audit_table = QTableView()
        self.audit_table.setObjectName("auditTable")
        self.audit_table.setModel(self._audit_model)
        self.audit_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.audit_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.audit_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.audit_table.setAlternatingRowColors(True)
        self.audit_table.setWordWrap(False)
        self.audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.audit_table.horizontalHeader().setStretchLastSection(False)
        self.audit_table.verticalHeader().setDefaultSectionSize(24)
        layout.addWidget(self.audit_table, stretch=1)
        return tab

    def _build_summary_tab(self) -> QScrollArea:
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("summaryScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("summaryContent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 12, 12, 10)
        layout.setSpacing(14)

        summary_group = QGroupBox("Resumen de carga")
        summary_layout = QFormLayout(summary_group)
        summary_layout.setContentsMargins(14, 18, 14, 14)
        summary_layout.setHorizontalSpacing(18)
        summary_layout.setVerticalSpacing(10)
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
            label_widget = QLabel(f"{label}:")
            label_widget.setObjectName("summaryFieldLabel")
            label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            value = QLabel("-")
            value.setProperty("summaryValue", True)
            value.setObjectName(f"summary_{key}")
            value.setWordWrap(True)
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            value.setContentsMargins(10, 6, 10, 6)
            summary_layout.addRow(label_widget, value)
            self._summary_labels[key] = value

        value = QPlainTextEdit()
        value.setObjectName("summary_columnas")
        value.setReadOnly(True)
        value.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        value.setMinimumHeight(96)
        value.setMaximumHeight(180)
        value.setPlainText("-")
        value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        label_widget = QLabel("Columnas visibles:")
        label_widget.setObjectName("summaryFieldLabel")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        summary_layout.addRow(label_widget, value)
        self._summary_texts["columnas"] = value
        layout.addWidget(summary_group)

        layout.addStretch(1)

        scroll_area.setWidget(content)
        return scroll_area

    def _connect_signals(self) -> None:
        self.select_button.clicked.connect(self.select_workbook)
        self.default_button.clicked.connect(self.load_default_control_cartera)
        self.save_as_button.clicked.connect(self.save_as_control_cartera)
        self.path_edit.returnPressed.connect(self.load_selected_workbook)
        self.theme_button.clicked.connect(self.change_theme)
        self.search_edit.textChanged.connect(self._apply_search_filter)
        self.search_column_combo.currentIndexChanged.connect(self._apply_search_filter)
        self.clear_search_button.clicked.connect(self.clear_search)
        self.records_table.doubleClicked.connect(self.open_record_detail)

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

        if not self._confirm_discard_pending_changes():
            return
        self._set_selected_path(path, "Control Cartera seleccionado. Cargando...")
        self.load_selected_workbook(confirm_pending=False)

    def load_default_control_cartera(self) -> None:
        """Carga la fuente operativa predeterminada desde data/input."""
        if not self._confirm_discard_pending_changes():
            return
        self._set_selected_path(str(self._default_path), "Cargando Control Cartera predeterminado...")
        self.load_selected_workbook(confirm_pending=False)

    def _set_selected_path(self, path: str, status_message: str) -> None:
        self.path_edit.setText(path)
        self.path_edit.setToolTip(path)
        self._last_user_message = status_message
        self.statusBar().showMessage(status_message)

    def load_selected_workbook(self, confirm_pending: bool = True) -> None:
        path = self.path_edit.text().strip()
        if confirm_pending and not self._confirm_discard_pending_changes():
            return
        validation_error = self._validate_selected_path(path)
        if validation_error:
            self._show_error(validation_error)
            return

        try:
            result = self._loader(path)
        except GestorSegurosError:
            self._show_error("No fue posible cargar el Control Cartera. Revise la estructura del archivo.")
            return

        self._current_source_path = Path(path).resolve()
        self._current_result = result
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
        self._records_model.set_records(result.records, headers, result.summary.column_indexes_by_name)
        self._populate_search_columns(headers)
        self.records_table.clearSelection()
        self.clear_search()
        self.records_rows_label.setText(f"Filas cargadas: {self._records_model.rowCount()}")
        self.records_columns_label.setText(f"Columnas visibles: {self._records_model.columnCount()}")
        self._update_pending_changes_indicator()
        self._clear_audit_log()
        if self._records_model.rowCount() == 0:
            self.records_hint.setText("No hay registros cargados para mostrar.")
        else:
            self.records_hint.setText("Registros cargados")
        self._adjust_records_table_columns()
        self.tabs.setCurrentIndex(0)

    def _clear_records(self) -> None:
        self._current_source_path = None
        self._current_result = None
        self._records_model.clear()
        self.records_table.clearSelection()
        self._populate_search_columns(())
        self.clear_search()
        self.records_rows_label.setText("Filas cargadas: 0")
        self.records_columns_label.setText("Columnas visibles: 0")
        self._update_pending_changes_indicator()
        self._clear_audit_log()
        self.records_hint.setText("Cargue un Control Cartera para visualizar los registros.")
        self._adjust_records_table_columns()

    def _populate_search_columns(self, headers: tuple[str, ...]) -> None:
        blocker = QSignalBlocker(self.search_column_combo)
        try:
            self.search_column_combo.clear()
            self.search_column_combo.addItem("Todas las columnas", ALL_COLUMNS_INDEX)
            for index, header in enumerate(headers):
                self.search_column_combo.addItem(header, index)
        finally:
            del blocker

    def clear_search(self) -> None:
        text_blocker = QSignalBlocker(self.search_edit)
        combo_blocker = QSignalBlocker(self.search_column_combo)
        try:
            self.search_edit.clear()
            self.search_column_combo.setCurrentIndex(0)
        finally:
            del text_blocker
            del combo_blocker
        self._apply_search_filter()

    def _apply_search_filter(self, *_args: object) -> None:
        self._records_filter_model.set_search_text(self.search_edit.text())
        self._records_filter_model.set_search_column(self._selected_search_column())
        self._update_search_counter()

    def _selected_search_column(self) -> int:
        selected = self.search_column_combo.currentData()
        return selected if isinstance(selected, int) else ALL_COLUMNS_INDEX

    def _update_search_counter(self) -> None:
        visible_rows = self._records_filter_model.rowCount()
        total_rows = self._records_model.rowCount()
        self.search_results_label.setText(f"Mostrando {visible_rows} de {total_rows} registros")

    def _show_error(self, message: str) -> None:
        self._clear_records()
        self._summary_labels["estado"].setText("Error de carga")
        self._last_user_message = message
        self.statusBar().showMessage("No se pudo cargar el Control Cartera.")
        if self._show_dialogs:
            QMessageBox.warning(self, "Control Cartera", message)

    def save_as_control_cartera(self) -> None:
        """Guarda una copia del Control Cartera con los cambios en memoria."""
        if self._current_source_path is None or self._current_result is None:
            self._show_save_error("Cargue un Control Cartera antes de guardar una copia.")
            return

        destination = self._select_save_destination()
        if destination is None:
            return
        if destination == self._current_source_path:
            self._show_save_error("Guardar como no puede sobrescribir el archivo cargado.")
            return
        if destination.exists() and not self._confirm_overwrite_destination(destination):
            return

        updates = tuple(
            WorkbookCellUpdate(row_number=row_number, column_name=column_name, column_index=column_index, value=value)
            for row_number, column_name, column_index, value in self._records_model.pending_cell_updates()
        )
        try:
            saved_path = self._saver(
                self._current_source_path,
                destination,
                updates,
                sheet_name=self._current_result.summary.sheet_name,
                header_row=self._current_result.summary.header_row,
            )
        except (GestorSegurosError, OSError, ValueError):
            self._show_save_error("No fue posible guardar la copia del Control Cartera.")
            return

        self._records_model.mark_saved()
        self._current_source_path = Path(saved_path).resolve()
        self.path_edit.setText(str(self._current_source_path))
        self.path_edit.setToolTip(str(self._current_source_path))
        self._summary_labels["archivo"].setText(self._current_source_path.name)
        self._update_pending_changes_indicator()
        message = f"Copia guardada correctamente: {saved_path.name}"
        self._last_user_message = message
        self.statusBar().showMessage(message)
        if self._show_dialogs:
            QMessageBox.information(self, "Guardar como", "Control Cartera guardado como copia correctamente.")

    def _select_save_destination(self) -> Path | None:
        default_path = get_project_paths().data_output_dir / _default_save_as_name()
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar como",
            str(default_path),
            "Excel (*.xlsx)",
        )
        if not path:
            return None
        destination = Path(path)
        if not destination.suffix:
            destination = destination.with_suffix(".xlsx")
        if destination.suffix.lower() != ".xlsx":
            self._show_save_error("Formato no admitido. Guarde la copia con extensiÃ³n .xlsx.")
            return None
        return destination.resolve()

    def _confirm_overwrite_destination(self, destination: Path) -> bool:
        if not self._show_dialogs:
            return True
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Warning)
        message.setWindowTitle("Confirmar sobrescritura")
        message.setText("Ya existe un archivo en la ruta seleccionada.")
        message.setInformativeText("Puede sobrescribir esa copia, pero nunca se sobrescribirÃ¡ el archivo cargado.")
        overwrite_button = message.addButton("Sobrescribir copia", QMessageBox.ButtonRole.AcceptRole)
        message.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        message.exec()
        return message.clickedButton() is overwrite_button

    def _show_save_error(self, message: str) -> None:
        self._last_user_message = message
        self.statusBar().showMessage("No se pudo guardar la copia del Control Cartera.")
        if self._show_dialogs:
            QMessageBox.warning(self, "Guardar como", message)

    def open_record_detail(self, index: object | None = None) -> RecordDetailDialog | None:
        """Abre el detalle del registro visible seleccionado por doble clic."""
        if index is None or not hasattr(index, "isValid") or not index.isValid():
            return None

        source_index = self._records_filter_model.mapToSource(index)
        record = self._records_model.record_at(source_index.row())
        if record is None:
            return None

        dialog = RecordDetailDialog(record, self._records_model.headers(), self._current_theme, self)
        dialog.set_edit_callback(lambda detail_dialog: self.edit_record_at_source_row(source_index.row(), detail_dialog))
        dialog.exec()
        return dialog

    def edit_record_at_source_row(self, source_row: int, detail_dialog: RecordDetailDialog | None = None) -> bool:
        """Abre la ediciÃ³n modal y aplica cambios Ãºnicamente en memoria."""
        record = self._records_model.record_at(source_row)
        if record is None:
            return False

        dialog = RecordEditDialog(
            record,
            self._records_model.headers(),
            self._current_theme,
            self,
            confirm_changes=self._show_dialogs,
        )
        if dialog.exec() != RecordEditDialog.DialogCode.Accepted:
            return False

        edited_values = dialog.edited_values()
        changes = self._records_model.preview_update_changes(source_row, edited_values)
        if not changes:
            return False

        if not self._records_model.update_record(source_row, edited_values):
            return False

        self._audit_model.add_entries(build_audit_entries(record.row_number, changes))
        self._apply_search_filter()
        self._adjust_records_table_columns()
        self._update_pending_changes_indicator()
        self._update_audit_indicator()
        self._last_user_message = "Cambios pendientes sin guardar."
        self.statusBar().showMessage("Cambios pendientes sin guardar.")
        updated_record = self._records_model.record_at(source_row)
        if detail_dialog is not None and updated_record is not None:
            detail_dialog.refresh_record(updated_record)
        return True

    def _adjust_records_table_columns(self) -> None:
        """Ajusta anchos visibles sin impedir el redimensionamiento manual."""
        model = self.records_table.model()
        if model is None or model.columnCount() == 0:
            return

        metrics = QFontMetrics(self.records_table.font())
        header_metrics = QFontMetrics(self.records_table.horizontalHeader().font())
        rows_to_sample = min(model.rowCount(), _COLUMN_WIDTH_SAMPLE_ROWS)
        for column in range(model.columnCount()):
            header = str(model.headerData(column, Qt.Orientation.Horizontal) or "")
            minimum, maximum = _column_width_bounds(header)
            width = header_metrics.horizontalAdvance(header) + 34
            for row in range(rows_to_sample):
                index = model.index(row, column)
                value = str(model.data(index, Qt.ItemDataRole.DisplayRole) or "")
                width = max(width, metrics.horizontalAdvance(value) + 32)
            self.records_table.setColumnWidth(column, max(minimum, min(width, maximum)))

    def _update_pending_changes_indicator(self) -> None:
        count = self._records_model.pending_changes_count()
        self.pending_changes_label.setText(f"Cambios pendientes: {count}")
        self.pending_changes_label.setProperty("hasPendingChanges", count > 0)
        self.pending_changes_label.style().unpolish(self.pending_changes_label)
        self.pending_changes_label.style().polish(self.pending_changes_label)

    def _clear_audit_log(self) -> None:
        self._audit_model.clear()
        self._update_audit_indicator()

    def _update_audit_indicator(self) -> None:
        count = self._audit_model.rowCount()
        self.audit_count_label.setText(f"Cambios registrados: {count}")
        self.audit_empty_label.setVisible(count == 0)

    def _confirm_discard_pending_changes(self) -> bool:
        if not self._records_model.has_pending_changes() or not self._show_dialogs:
            return True

        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Warning)
        message.setWindowTitle("Cambios pendientes sin guardar")
        message.setText(
            "Hay cambios aplicados solo en memoria. Si continúa, se descartarán porque todavía no existe guardado."
        )
        continue_button = message.addButton("Continuar sin guardar", QMessageBox.ButtonRole.AcceptRole)
        message.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        message.exec()
        return message.clickedButton() is continue_button

    def closeEvent(self, event: object) -> None:
        if self._confirm_discard_pending_changes():
            event.accept()
        else:
            event.ignore()

    def change_theme(self) -> None:
        """Cambia al tema visual alterno y persiste la selección."""
        self.apply_theme(next_theme(self._current_theme), persist=True)

    def apply_theme(self, theme: str, persist: bool = False, update_status: bool = True) -> None:
        """Aplica un tema visual soportado sin tocar los registros cargados."""
        self._current_theme = normalize_theme(theme)
        self._sync_theme_control()
        self.setStyleSheet(build_stylesheet(self._current_theme))
        if persist:
            self._settings.setValue(THEME_SETTING_KEY, self._current_theme)
            self._settings.sync()
        if update_status:
            message = f"{theme_label(self._current_theme)} aplicado."
            self._last_user_message = message
            self.statusBar().showMessage(message)

    def _sync_theme_control(self) -> None:
        if not hasattr(self, "theme_button"):
            return
        self.theme_button.setText("🌙" if self._current_theme == LIGHT_THEME else "☀")
        self.theme_button.setAccessibleName(f"Cambiar a {theme_label(next_theme(self._current_theme)).lower()}")

    def _apply_style(self) -> None:
        self.apply_theme(self._current_theme, persist=False, update_status=False)


def _format_items(items: tuple[str, ...]) -> str:
    if not items:
        return "ninguna"
    return ", ".join(items)


def _column_width_bounds(header: str) -> tuple[int, int]:
    """Devuelve límites visuales conservadores para una columna visible."""
    key = resolve_column_key(header)
    if key in _COLUMN_WIDTH_RULES:
        return _COLUMN_WIDTH_RULES[key]
    normalized = " ".join(header.strip().lower().split())
    return _COLUMN_WIDTH_RULES.get(normalized, _DEFAULT_COLUMN_WIDTH)


def _default_save_as_name() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"CONTROLCARTERA_V2_editado_{timestamp}.xlsx"


def run_gui(argv: list[str] | None = None) -> int:
    """Ejecuta la aplicación PySide6."""
    app = QApplication.instance() or QApplication(argv if argv is not None else sys.argv)
    app.setWindowIcon(load_app_icon())
    window = MainWindow()
    window.show()
    return app.exec()
