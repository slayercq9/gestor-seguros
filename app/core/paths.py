"""Utilidades para resolver rutas del proyecto."""

from dataclasses import dataclass
from pathlib import Path

from app.core.exceptions import PathResolutionError


@dataclass(frozen=True)
class ProjectPaths:
    """Rutas locales conocidas que usa la base técnica."""

    project_root: Path
    data_input_dir: Path
    data_output_dir: Path
    data_backups_dir: Path
    data_samples_dir: Path

    def required_directories(self) -> tuple[Path, ...]:
        """Devuelve las carpetas esperadas en la estructura del repositorio."""
        return (
            self.data_input_dir,
            self.data_output_dir,
            self.data_backups_dir,
            self.data_samples_dir,
        )

    def missing_required_directories(self) -> tuple[Path, ...]:
        """Devuelve carpetas locales faltantes sin crearlas."""
        return tuple(path for path in self.required_directories() if not path.is_dir())


def resolve_project_root(start: Path | None = None) -> Path:
    """Resuelve la raíz del repositorio recorriendo hacia arriba desde una ruta inicial."""
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "README.md").is_file() and (candidate / "docs" / "proyecto").is_dir():
            return candidate

    raise PathResolutionError("No se pudo resolver la raíz del proyecto.")


def get_project_paths(project_root: Path | None = None) -> ProjectPaths:
    """Construye las rutas conocidas del proyecto sin modificar el sistema de archivos."""
    root = resolve_project_root(project_root) if project_root is None else project_root.resolve()
    if not root.is_dir():
        raise PathResolutionError(f"La raíz del proyecto no existe: {root}")

    data_dir = root / "data"
    return ProjectPaths(
        project_root=root,
        data_input_dir=data_dir / "input",
        data_output_dir=data_dir / "output",
        data_backups_dir=data_dir / "backups",
        data_samples_dir=data_dir / "samples",
    )
