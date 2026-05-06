"""Configuración central de la aplicación."""

from dataclasses import dataclass
from pathlib import Path

from app import __app_name__, __version__
from app.core.exceptions import ConfigurationError
from app.core.paths import ProjectPaths, get_project_paths


@dataclass(frozen=True)
class AppConfig:
    """Configuración resuelta que usa el arranque de la aplicación."""

    app_name: str
    version: str
    project_root: Path
    data_input_dir: Path
    data_output_dir: Path
    data_backups_dir: Path
    data_samples_dir: Path
    log_level: str = "INFO"


def load_default_config(project_root: Path | None = None, log_level: str = "INFO") -> AppConfig:
    """Construye la configuración por defecto desde las rutas del repositorio.

    La función solo resuelve rutas; no crea carpetas, no lee archivos Excel
    ni carga archivos externos de configuración.
    """
    normalized_log_level = log_level.upper().strip()
    if not normalized_log_level:
        raise ConfigurationError("El nivel de logging no puede estar vacío.")

    paths: ProjectPaths = get_project_paths(project_root)
    return AppConfig(
        app_name=__app_name__,
        version=__version__,
        project_root=paths.project_root,
        data_input_dir=paths.data_input_dir,
        data_output_dir=paths.data_output_dir,
        data_backups_dir=paths.data_backups_dir,
        data_samples_dir=paths.data_samples_dir,
        log_level=normalized_log_level,
    )
