import subprocess
import sys

from app.bootstrap import bootstrap_application
from app.main import main


def test_main_returns_success_without_business_workflows():
    assert main() == 0


def test_bootstrap_reports_safe_technical_status():
    result = bootstrap_application()

    assert result.app_name == "gestor-seguros"
    assert result.version == "1.6.0"
    assert "base tecnica inicializada" in result.status_message
    assert "CONTROLCARTERA" not in result.status_message


def test_module_entrypoint_runs_without_accessing_real_workbook():
    completed = subprocess.run(
        [sys.executable, "-m", "app"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "gestor-seguros 1.6.0" in completed.stdout
    assert "CONTROLCARTERA" not in completed.stdout
    assert "CONTROLCARTERA" not in completed.stderr
