"""Logging setup for the technical skeleton."""

import logging

from app.core.exceptions import ConfigurationError


LOGGER_NAME = "gestor_seguros"


def configure_logging(log_level: str = "INFO") -> logging.Logger:
    """Configure a console logger without persistent artifacts."""
    numeric_level = getattr(logging, log_level.upper().strip(), None)
    if not isinstance(numeric_level, int):
        raise ConfigurationError(f"Nivel de logging no valido: {log_level!r}")

    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()
    logger.setLevel(numeric_level)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(numeric_level)
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger
