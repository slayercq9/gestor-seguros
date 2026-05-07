"""Temas visuales para la interfaz PySide6.

Los temas son pequeños y locales a la capa de interfaz. No afectan la carga
de datos, los registros, los archivos Excel ni las reglas de negocio.
"""

from __future__ import annotations


LIGHT_THEME = "light"
DARK_THEME = "dark"
THEME_SETTING_KEY = "ui/theme"


def normalize_theme(value: object) -> str:
    """Devuelve un nombre de tema soportado y usa el tema claro como respaldo."""
    if str(value).lower() == DARK_THEME:
        return DARK_THEME
    return LIGHT_THEME


def theme_label(theme: str) -> str:
    """Devuelve la etiqueta en español para un tema."""
    return "Tema oscuro" if normalize_theme(theme) == DARK_THEME else "Tema claro"


def next_theme(theme: str) -> str:
    """Devuelve el tema visual alterno."""
    return DARK_THEME if normalize_theme(theme) == LIGHT_THEME else LIGHT_THEME


def build_stylesheet(theme: str) -> str:
    """Construye la hoja de estilos Qt para el tema solicitado."""
    return _dark_stylesheet() if normalize_theme(theme) == DARK_THEME else _light_stylesheet()


def _light_stylesheet() -> str:
    return """
        QMainWindow {
            background: #F6F7F9;
            color: #111827;
        }
        QWidget {
            color: #111827;
            background: #F6F7F9;
        }
        QScrollArea#summaryScrollArea, QWidget#mainContent, QWidget#summaryContent, QWidget#recordsTab {
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
        QLabel#recordsHint {
            padding: 2px 4px;
        }
        QLabel#recordsReadonlyNote {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
            color: #4B5563;
        }
        QWidget#searchBar {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
        }
        QLabel#searchLabel, QLabel#searchColumnLabel {
            background: transparent;
            color: #374151;
            font-weight: 600;
        }
        QLabel#searchResultsLabel {
            background: transparent;
            color: #6B7280;
            font-weight: 500;
        }
        QWidget#recordsCountsPanel {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
        }
        QLabel#recordsRowsLabel, QLabel#recordsColumnsLabel {
            background: transparent;
            color: #374151;
            font-weight: 600;
        }
        QLabel#pendingChangesLabel {
            background: transparent;
            color: #6B7280;
            font-weight: 600;
        }
        QLabel#pendingChangesLabel[hasPendingChanges="true"] {
            color: #B45309;
        }
        QLabel#editRecordNotice {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
            color: #4B5563;
            padding: 8px 10px;
        }
        QLabel#editRecordFieldLabel {
            background: transparent;
            color: #374151;
            font-weight: 600;
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
            font-weight: 700;
        }
        QGroupBox QLabel#summaryFieldLabel {
            background: transparent;
            color: #4B5563;
            font-weight: 600;
            padding: 6px 0;
        }
        QGroupBox QLabel[summaryValue="true"] {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
            color: #111827;
            font-weight: 500;
        }
        QLabel#recordDetailEmpty {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
            color: #4B5563;
            padding: 8px 10px;
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
        QPushButton#themeToggleButton {
            padding: 2px;
            border-radius: 6px;
            border: 1px solid #9CA3AF;
            background: #FFFFFF;
            color: #111827;
            font-size: 17px;
            font-weight: 600;
        }
        QPushButton#themeToggleButton:hover {
            background: #E5E7EB;
        }
        QPushButton#clearSearchButton {
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid #CBD5E1;
            background: #F8FAFC;
            color: #1F2937;
            font-weight: 600;
        }
        QPushButton#clearSearchButton:hover {
            background: #E5E7EB;
        }
        QLineEdit, QPlainTextEdit, QTableView, QComboBox {
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
        QComboBox {
            min-height: 34px;
        }
        QLineEdit#recordsSearchText, QComboBox#recordsSearchColumn {
            min-height: 30px;
            padding: 5px 8px;
        }
        QPlainTextEdit {
            font-family: Consolas, "Courier New", monospace;
            font-size: 12px;
        }
        QPlainTextEdit#summary_columnas {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
            color: #111827;
            padding: 10px;
        }
        QTableView#recordDetailDialogTable {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 6px;
        }
        QTableView {
            gridline-color: #E5E7EB;
            alternate-background-color: #F9FAFB;
        }
        QHeaderView::section {
            background: #E5E7EB;
            color: #111827;
            border: 1px solid #D1D5DB;
            padding: 6px;
            font-weight: 600;
        }
        QStatusBar {
            color: #374151;
            background: #F6F7F9;
        }
    """


def _dark_stylesheet() -> str:
    return """
        QMainWindow {
            background: #111827;
            color: #F9FAFB;
        }
        QWidget {
            color: #F9FAFB;
            background: #111827;
        }
        QScrollArea#summaryScrollArea, QWidget#mainContent, QWidget#summaryContent, QWidget#recordsTab {
            background: #111827;
        }
        QLabel {
            color: #F9FAFB;
        }
        QLabel#appTitle {
            font-size: 24px;
            font-weight: 700;
            color: #F9FAFB;
        }
        QLabel#versionLabel {
            color: #CBD5E1;
            font-weight: 600;
        }
        QLabel#helperText, QLabel#recordsHint, QLabel#recordsReadonlyNote {
            color: #D1D5DB;
        }
        QLabel#recordsHint {
            padding: 2px 4px;
        }
        QLabel#recordsReadonlyNote {
            background: #1F2937;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #D1D5DB;
        }
        QWidget#searchBar {
            background: #1F2937;
            border: 1px solid #374151;
            border-radius: 6px;
        }
        QLabel#searchLabel, QLabel#searchColumnLabel {
            background: transparent;
            color: #D1D5DB;
            font-weight: 600;
        }
        QLabel#searchResultsLabel {
            background: transparent;
            color: #CBD5E1;
            font-weight: 500;
        }
        QWidget#recordsCountsPanel {
            background: #1F2937;
            border: 1px solid #374151;
            border-radius: 6px;
        }
        QLabel#recordsRowsLabel, QLabel#recordsColumnsLabel {
            background: transparent;
            color: #D1D5DB;
            font-weight: 600;
        }
        QLabel#pendingChangesLabel {
            background: transparent;
            color: #CBD5E1;
            font-weight: 600;
        }
        QLabel#pendingChangesLabel[hasPendingChanges="true"] {
            color: #FBBF24;
        }
        QLabel#editRecordNotice {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #CBD5E1;
            padding: 8px 10px;
        }
        QLabel#editRecordFieldLabel {
            background: transparent;
            color: #D1D5DB;
            font-weight: 600;
        }
        QGroupBox {
            border: 1px solid #374151;
            border-radius: 6px;
            margin-top: 10px;
            padding: 12px;
            background: #1F2937;
            color: #F9FAFB;
            font-weight: 600;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
            color: #F9FAFB;
            background: #1F2937;
            font-weight: 700;
        }
        QGroupBox QLabel#summaryFieldLabel {
            background: transparent;
            color: #CBD5E1;
            font-weight: 600;
            padding: 6px 0;
        }
        QGroupBox QLabel[summaryValue="true"] {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #F9FAFB;
            font-weight: 500;
        }
        QLabel#recordDetailEmpty {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #CBD5E1;
            padding: 8px 10px;
        }
        QTabWidget::pane {
            border: 1px solid #374151;
            border-radius: 6px;
            background: #1F2937;
        }
        QTabBar::tab {
            background: #374151;
            color: #F9FAFB;
            padding: 8px 14px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background: #1F2937;
            font-weight: 600;
        }
        QPushButton {
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid #38BDF8;
            background: #0E7490;
            color: #FFFFFF;
            font-weight: 600;
        }
        QPushButton:hover {
            background: #0891B2;
        }
        QPushButton#themeToggleButton {
            padding: 2px;
            border-radius: 6px;
            border: 1px solid #64748B;
            background: #1F2937;
            color: #F9FAFB;
            font-size: 17px;
            font-weight: 600;
        }
        QPushButton#themeToggleButton:hover {
            background: #374151;
        }
        QPushButton#clearSearchButton {
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid #475569;
            background: #1E293B;
            color: #F9FAFB;
            font-weight: 600;
        }
        QPushButton#clearSearchButton:hover {
            background: #334155;
        }
        QLineEdit, QPlainTextEdit, QTableView, QComboBox {
            border: 1px solid #4B5563;
            border-radius: 6px;
            padding: 8px;
            background: #0F172A;
            color: #F9FAFB;
            selection-background-color: #155E75;
            selection-color: #FFFFFF;
        }
        QLineEdit {
            min-height: 34px;
        }
        QComboBox {
            min-height: 34px;
        }
        QLineEdit#recordsSearchText, QComboBox#recordsSearchColumn {
            min-height: 30px;
            padding: 5px 8px;
        }
        QPlainTextEdit {
            font-family: Consolas, "Courier New", monospace;
            font-size: 12px;
        }
        QPlainTextEdit#summary_columnas {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 6px;
            color: #F9FAFB;
            padding: 10px;
        }
        QTableView#recordDetailDialogTable {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 6px;
        }
        QTableView {
            gridline-color: #334155;
            alternate-background-color: #172033;
        }
        QHeaderView::section {
            background: #374151;
            color: #F9FAFB;
            border: 1px solid #4B5563;
            padding: 6px;
            font-weight: 600;
        }
        QStatusBar {
            color: #D1D5DB;
            background: #111827;
        }
    """
