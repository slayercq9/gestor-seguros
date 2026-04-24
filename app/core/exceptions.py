"""Centralized project exceptions."""


class GestorSegurosError(Exception):
    """Base exception for controlled project errors."""


class ConfigurationError(GestorSegurosError):
    """Raised when application configuration is invalid."""


class PathResolutionError(GestorSegurosError):
    """Raised when required project paths cannot be resolved."""
