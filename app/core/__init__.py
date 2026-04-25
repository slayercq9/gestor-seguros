"""Core technical primitives for gestor-seguros."""

from app.core.exceptions import ConfigurationError, GestorSegurosError, PathResolutionError, WorkbookLoadError
from app.core.logging import LOGGER_NAME, configure_logging
from app.core.paths import ProjectPaths, get_project_paths, resolve_project_root

__all__ = [
    "ConfigurationError",
    "GestorSegurosError",
    "LOGGER_NAME",
    "PathResolutionError",
    "ProjectPaths",
    "WorkbookLoadError",
    "configure_logging",
    "get_project_paths",
    "resolve_project_root",
]
