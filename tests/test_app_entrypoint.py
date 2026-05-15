import subprocess
import sys

from app.bootstrap import bootstrap_application
from app.main import main


def test_main_returns_success_without_business_workflows():
    assert main(["--check"]) == 0


def test_main_check_does_not_initialize_bootstrap(monkeypatch, capsys):
    import app.main as app_main

    called = {"value": False}

    def fail_bootstrap():
        called["value"] = True
        raise AssertionError("bootstrap_application no debe ejecutarse en --check")

    monkeypatch.setattr(app_main, "bootstrap_application", fail_bootstrap, raising=False)

    assert app_main.main(["--check"]) == 0
    assert called["value"] is False
    assert capsys.readouterr().out.strip() == "gestor-seguros 1.13.1"


def test_main_without_arguments_starts_gui(monkeypatch):
    import app.ui.main_window as main_window

    called = {"value": False}

    def fake_run_gui():
        called["value"] = True
        return 0

    monkeypatch.setattr(main_window, "run_gui", fake_run_gui)

    assert main([]) == 0
    assert called["value"] is True


def test_bootstrap_reports_safe_technical_status():
    result = bootstrap_application()

    assert result.app_name == "gestor-seguros"
    assert result.version == "1.13.1"
    assert "base técnica inicializada" in result.status_message
    assert "CONTROLCARTERA" not in result.status_message


def test_module_entrypoint_runs_without_accessing_real_workbook():
    completed = subprocess.run(
        [sys.executable, "-m", "app", "--check"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "gestor-seguros 1.13.1"
    assert "CONTROLCARTERA" not in completed.stdout
    assert "CONTROLCARTERA" not in completed.stderr
