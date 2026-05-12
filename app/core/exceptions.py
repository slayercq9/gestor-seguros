"""Excepciones centralizadas del proyecto."""


class GestorSegurosError(Exception):
    """Excepción base para errores controlados del proyecto."""


class ConfigurationError(GestorSegurosError):
    """Se usa cuando la configuración de la aplicación es inválida."""


class PathResolutionError(GestorSegurosError):
    """Se usa cuando no se pueden resolver rutas requeridas del proyecto."""


class WorkbookModernizationError(GestorSegurosError):
    """Se usa cuando la modernización del libro de Excel no puede completarse con seguridad."""


class WorkbookLoadError(GestorSegurosError):
    """Se usa cuando el lector controlado no puede cargar un libro de Excel."""


class WorkbookSaveError(GestorSegurosError):
    """Se usa cuando no se puede guardar una copia del Control Cartera."""
