"""Diálogo modal para editar registros en memoria, sin guardar en Excel."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.domain.column_standards import DETAIL, DUE_DAY, DUE_MONTH, TERM, get_column_control, resolve_column_key
from app.domain.field_validators import DAY_VALUES, MONTH_VALUES, VIGENCIA_VALUES, validate_edited_fields
from app.domain.workbook_records import WorkbookRowRecord
from app.ui.table_model import value_to_display_text
from app.ui.theme import build_stylesheet


class NoWheelComboBox(QComboBox):
    """ComboBox que evita cambios accidentales con la rueda del mouse."""

    def wheelEvent(self, event: object) -> None:
        event.ignore()


class RecordEditDialog(QDialog):
    """Permite editar campos visibles de un registro solo en memoria."""

    def __init__(
        self,
        record: WorkbookRowRecord,
        headers: tuple[str, ...],
        theme: str,
        parent: QWidget | None = None,
        confirm_changes: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Editar registro")
        self.setMinimumSize(700, 520)
        self._headers = headers
        self._confirm_changes = confirm_changes
        self._inputs: dict[str, QWidget] = {}
        self._build_ui(record)
        self.setStyleSheet(build_stylesheet(theme))

    def edited_values(self) -> dict[str, str]:
        """Devuelve los valores escritos por el usuario, indexados por encabezado."""
        return {header: _field_text(field) for header, field in self._inputs.items()}

    def _build_ui(self, record: WorkbookRowRecord) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        notice = QLabel("Los cambios se aplicarán solo en memoria. No se modificará el archivo Excel.")
        notice.setObjectName("editRecordNotice")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("editRecordScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("editRecordContent")
        form = QFormLayout(content)
        form.setContentsMargins(4, 4, 10, 4)
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(10)
        for header in self._headers:
            label = QLabel(f"{header}:")
            label.setObjectName("editRecordFieldLabel")
            field = _build_field_for_column(header, value_to_display_text(record.values_by_column.get(header), header))
            form.addRow(label, field)
            self._inputs[header] = field

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area, stretch=1)

        buttons = QDialogButtonBox()
        buttons.setObjectName("editRecordButtons")
        apply_button = buttons.addButton("Aplicar cambios", QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_button = buttons.addButton("Cancelar", QDialogButtonBox.ButtonRole.RejectRole)
        apply_button.clicked.connect(self._confirm_and_accept)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(buttons, alignment=Qt.AlignmentFlag.AlignRight)

    def _confirm_and_accept(self) -> None:
        validation = validate_edited_fields(self.edited_values())
        if validation.has_errors:
            if self._confirm_changes:
                self._show_validation_errors(validation.errors)
            return
        if validation.has_warnings and self._confirm_changes and not self._confirm_validation_warnings(validation.warnings):
            return
        if self._confirm_changes and not self._confirm_apply_changes():
            return
        self.accept()

    def _show_validation_errors(self, errors: object) -> None:
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Critical)
        message.setWindowTitle("No se pueden aplicar los cambios")
        message.setText("Corrija los siguientes errores antes de aplicar cambios.")
        message.setInformativeText(_format_validation_issues(errors))
        message.addButton("Revisar", QMessageBox.ButtonRole.AcceptRole)
        message.exec()

    def _confirm_validation_warnings(self, warnings: object) -> bool:
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Warning)
        message.setWindowTitle("Advertencias de validación")
        message.setText("Se detectaron advertencias en los campos editados.")
        message.setInformativeText(_format_validation_issues(warnings))
        apply_button = message.addButton("Aplicar de todos modos", QMessageBox.ButtonRole.AcceptRole)
        message.addButton("Revisar", QMessageBox.ButtonRole.RejectRole)
        message.exec()
        return message.clickedButton() is apply_button

    def _confirm_apply_changes(self) -> bool:
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Question)
        message.setWindowTitle("Confirmar cambios")
        message.setText("Los cambios se aplicarán solo en memoria. No se modificará el archivo Excel en esta fase.")
        apply_button = message.addButton("Aplicar", QMessageBox.ButtonRole.AcceptRole)
        message.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        message.exec()
        return message.clickedButton() is apply_button


def _build_field_for_column(header: str, value: str) -> QWidget:
    key = resolve_column_key(header)
    control = get_column_control(header)
    if key == TERM:
        return _build_combo_field(value, VIGENCIA_VALUES, "editRecordComboField", editable=False, no_wheel=True)
    if key == DUE_DAY:
        return _build_combo_field(value, ("", *DAY_VALUES), "editRecordComboField", editable=False, no_wheel=True)
    if key == DUE_MONTH:
        return _build_combo_field(value, ("", *MONTH_VALUES), "editRecordComboField", editable=False, no_wheel=True)
    if key == DETAIL or control == "multiline":
        field = QPlainTextEdit()
        field.setObjectName("editRecordTextArea")
        field.setPlainText(value)
        field.setMinimumHeight(96)
        return field

    field = QLineEdit()
    field.setObjectName("editRecordField")
    field.setText(value)
    field.setClearButtonEnabled(True)
    return field


def _build_combo_field(
    value: str,
    options: tuple[str, ...],
    object_name: str,
    *,
    editable: bool = True,
    no_wheel: bool = False,
) -> QComboBox:
    field = NoWheelComboBox() if no_wheel else QComboBox()
    field.setObjectName(object_name)
    field.setEditable(editable)
    field.addItems(list(options))
    if value and field.findText(value) == -1:
        field.insertItem(0, value)
    field.setCurrentText(value)
    return field


def _field_text(field: QWidget) -> str:
    if isinstance(field, QLineEdit):
        return field.text()
    if isinstance(field, QComboBox):
        return field.currentText()
    if isinstance(field, QPlainTextEdit):
        return field.toPlainText()
    return ""


def _format_validation_issues(issues: object) -> str:
    lines = []
    for issue in issues:
        prefix = "Error" if getattr(issue, "is_error", False) else "Advertencia"
        lines.append(f"- {prefix}: {issue.field_name}: {issue.message}")
    return "\n".join(lines)
