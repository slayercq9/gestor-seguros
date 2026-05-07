import logging
from pathlib import Path

import pytest

from app.config import load_default_config
from app.core import ConfigurationError, PathResolutionError, configure_logging, get_project_paths
from app.utils import REDACTED_TEXT, redact_if_sensitive


def test_default_config_resolves_project_paths_without_creating_artifacts():
    config = load_default_config()

    assert config.app_name == "gestor-seguros"
    assert config.version == "1.10.1"
    assert config.project_root.name == "gestor-seguros"
    assert config.data_input_dir.name == "input"
    assert config.data_output_dir.name == "output"
    assert config.data_backups_dir.name == "backups"
    assert config.data_samples_dir.name == "samples"


def test_project_paths_report_expected_local_directories_without_creating_them():
    paths = get_project_paths()

    expected_names = {"input", "output", "backups", "samples"}
    assert {path.name for path in paths.required_directories()} == expected_names
    assert all(path.parent.name == "data" for path in paths.required_directories())
    assert isinstance(paths.missing_required_directories(), tuple)


def test_invalid_project_root_fails_cleanly():
    missing_root = Path("ruta-local-inexistente-para-prueba")

    with pytest.raises(PathResolutionError):
        get_project_paths(missing_root)


def test_logging_uses_console_handler_only():
    logger = configure_logging("DEBUG")

    assert logger.name == "gestor_seguros"
    assert logger.level == logging.DEBUG
    assert logger.handlers
    assert not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)


def test_invalid_logging_level_raises_configuration_error():
    with pytest.raises(ConfigurationError):
        configure_logging("NOPE")


def test_redact_if_sensitive_hides_sensitive_labels():
    assert redact_if_sensitive("numero_poliza_original", "01-ABC-123") == REDACTED_TEXT
    assert redact_if_sensitive("estado", "pendiente") == "pendiente"
