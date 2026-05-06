"""Servicio de estado técnico seguro para la base de la aplicación."""

from dataclasses import dataclass

from app.config import AppConfig


@dataclass(frozen=True)
class ApplicationStatus:
    """Estado no sensible expuesto por el arranque técnico."""

    app_name: str
    version: str
    gui_enabled: bool
    workbook_io_enabled: bool
    persistence_enabled: bool


def build_application_status(config: AppConfig) -> ApplicationStatus:
    """Devuelve capacidades técnicas actuales sin comportamiento de negocio."""
    return ApplicationStatus(
        app_name=config.app_name,
        version=config.version,
        gui_enabled=False,
        workbook_io_enabled=False,
        persistence_enabled=False,
    )
