"""Safe technical status service for the application skeleton."""

from dataclasses import dataclass

from app.config import AppConfig


@dataclass(frozen=True)
class ApplicationStatus:
    """Non-sensitive status exposed by the technical bootstrap."""

    app_name: str
    version: str
    gui_enabled: bool
    workbook_io_enabled: bool
    persistence_enabled: bool


def build_application_status(config: AppConfig) -> ApplicationStatus:
    """Return current technical capabilities without business behavior."""
    return ApplicationStatus(
        app_name=config.app_name,
        version=config.version,
        gui_enabled=False,
        workbook_io_enabled=False,
        persistence_enabled=False,
    )
