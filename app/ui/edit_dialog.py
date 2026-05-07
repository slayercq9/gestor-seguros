"""Diálogo modal para editar registros en memoria, sin guardar en Excel."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.domain.workbook_records import WorkbookRowRecord
from app.ui.table_model import value_to_display_text
from app.ui.theme import build_stylesheet


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
        self._inputs: dict[str, QLineEdit] = {}
        self._build_ui(record)
        self.setStyleSheet(build_stylesheet(theme))

    def edited_values(self) -> dict[str, str]:
        """Devuelve los valores escritos por el usuario, indexados por encabezado."""
        return {header: field.text() for header, field in self._inputs.items()}

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
            field = QLineEdit()
            field.setObjectName("editRecordField")
            field.setText(value_to_display_text(record.values_by_column.get(header)))
            field.setClearButtonEnabled(True)
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
        if self._confirm_changes and not self._confirm_apply_changes():
            return
        self.accept()

    def _confirm_apply_changes(self) -> bool:
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Question)
        message.setWindowTitle("Confirmar cambios")
        message.setText("Los cambios se aplicarán solo en memoria. No se modificará el archivo Excel en esta fase.")
        apply_button = message.addButton("Aplicar", QMessageBox.ButtonRole.AcceptRole)
        message.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        message.exec()
        return message.clickedButton() is apply_button
