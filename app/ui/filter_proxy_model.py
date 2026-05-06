"""Modelo proxy para búsqueda local de registros cargados."""

from __future__ import annotations

import unicodedata
from typing import Any

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, Qt


ALL_COLUMNS_INDEX = -1


class RecordsFilterProxyModel(QSortFilterProxyModel):
    """Filtra registros visibles sin modificar el modelo original."""

    def __init__(self) -> None:
        super().__init__()
        self._query = ""
        self._normalized_query = ""
        self._source_column = ALL_COLUMNS_INDEX

    def set_search_text(self, text: str) -> None:
        """Actualiza el texto de búsqueda y refresca el filtro."""
        query = text.strip()
        self._query = query
        self._normalized_query = _normalize_search_text(query)
        self._refresh_rows_filter()

    def set_search_column(self, source_column: int) -> None:
        """Define la columna de origen donde se aplicará la búsqueda."""
        self._source_column = source_column
        self._refresh_rows_filter()

    def search_text(self) -> str:
        """Devuelve el texto de búsqueda activo."""
        return self._query

    def search_column(self) -> int:
        """Devuelve la columna de origen usada para filtrar."""
        return self._source_column

    def _refresh_rows_filter(self) -> None:
        self.beginFilterChange()
        self.endFilterChange(QSortFilterProxyModel.Direction.Rows)

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not self._normalized_query:
            return True

        source_model = self.sourceModel()
        if source_model is None:
            return False

        if self._source_column >= 0:
            return self._matches_cell(source_row, self._source_column, source_parent)

        return any(
            self._matches_cell(source_row, column, source_parent)
            for column in range(source_model.columnCount(source_parent))
        )

    def _matches_cell(self, source_row: int, source_column: int, source_parent: QModelIndex) -> bool:
        source_model = self.sourceModel()
        if source_model is None:
            return False

        index = source_model.index(source_row, source_column, source_parent)
        value = source_model.data(index, Qt.ItemDataRole.DisplayRole)
        return self._normalized_query in _normalize_search_text(value)


def _normalize_search_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char))
