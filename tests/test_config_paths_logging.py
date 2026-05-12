import logging
import shutil
from pathlib import Path
import sys

import pytest

from app.config import load_default_config
from app.core import ConfigurationError, PathResolutionError, configure_logging, get_project_paths, resolve_project_root
from app.utils import REDACTED_TEXT, redact_if_sensitive


def test_default_config_resolves_project_paths_without_creating_artifacts():
    config = load_default_config()

    assert config.app_name == "gestor-seguros"
    assert config.version == "1.11.3"
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


def test_project_root_resolves_in_development_mode():
    root = resolve_project_root()

    assert root.name == "gestor-seguros"
    assert (root / "README.md").is_file()
    assert (root / "docs" / "proyecto").is_dir()


def test_project_paths_use_executable_parent_when_packaged(monkeypatch):
    app_dir = Path(".pytest-app-empaquetada").resolve()
    if app_dir.exists():
        shutil.rmtree(app_dir)
    app_dir.mkdir()
    executable = app_dir / "GestorSeguros.exe"

    try:
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.setattr(sys, "executable", str(executable))

        paths = get_project_paths()

        assert paths.project_root == app_dir
        assert paths.data_input_dir.is_dir()
        assert paths.data_output_dir.is_dir()
        assert paths.data_backups_dir.is_dir()
        assert not paths.data_samples_dir.exists()
    finally:
        if app_dir.exists():
            shutil.rmtree(app_dir)


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
