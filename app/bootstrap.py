"""Arranque técnico de la aplicación.

Este módulo evita leer libros de Excel, abrir la GUI, crear bases de datos
o ejecutar flujos de negocio. Solo conecta la base técnica.
"""

from dataclasses import dataclass

from app.config import AppConfig, load_default_config
from app.core.logging import configure_logging
from app.services import build_application_status


@dataclass(frozen=True)
class BootstrapResult:
    """Resultado breve y seguro devuelto por el arranque técnico."""

    app_name: str
    version: str
    status_message: str


def bootstrap_application(config: AppConfig | None = None) -> BootstrapResult:
    """Inicializa configuración y logging para el proceso actual."""
    active_config = config or load_default_config()
    logger = configure_logging(active_config.log_level)
    status = build_application_status(active_config)

    logger.info("%s %s: arranque técnico listo", status.app_name, status.version)
    return BootstrapResult(
        app_name=status.app_name,
        version=status.version,
        status_message=f"{status.app_name} {status.version}: base técnica inicializada.",
    )
