"""Application bootstrap for the technical skeleton.

This module intentionally avoids reading workbooks, opening a GUI, creating
databases, or running business workflows. It only wires the technical base.
"""

from dataclasses import dataclass

from app.config import AppConfig, load_default_config
from app.core.logging import configure_logging
from app.services import build_application_status


@dataclass(frozen=True)
class BootstrapResult:
    """Small, safe result returned by the technical bootstrap."""

    app_name: str
    version: str
    status_message: str


def bootstrap_application(config: AppConfig | None = None) -> BootstrapResult:
    """Initialize configuration and logging for the current process."""
    active_config = config or load_default_config()
    logger = configure_logging(active_config.log_level)
    status = build_application_status(active_config)

    logger.info("%s %s technical bootstrap ready", status.app_name, status.version)
    return BootstrapResult(
        app_name=status.app_name,
        version=status.version,
        status_message=f"{status.app_name} {status.version}: base tecnica inicializada.",
    )
