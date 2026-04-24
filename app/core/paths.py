"""Project path resolution helpers."""

from dataclasses import dataclass
from pathlib import Path

from app.core.exceptions import PathResolutionError


@dataclass(frozen=True)
class ProjectPaths:
    """Known local paths used by the technical base."""

    project_root: Path
    data_input_dir: Path
    data_output_dir: Path
    data_backups_dir: Path
    data_samples_dir: Path

    def required_directories(self) -> tuple[Path, ...]:
        """Return directories expected to exist in the repository layout."""
        return (
            self.data_input_dir,
            self.data_output_dir,
            self.data_backups_dir,
            self.data_samples_dir,
        )

    def missing_required_directories(self) -> tuple[Path, ...]:
        """Return missing local directories without creating them."""
        return tuple(path for path in self.required_directories() if not path.is_dir())


def resolve_project_root(start: Path | None = None) -> Path:
    """Resolve the repository root by walking upward from a starting path."""
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "README.md").is_file() and (candidate / "docs" / "proyecto").is_dir():
            return candidate

    raise PathResolutionError("No se pudo resolver la raiz del proyecto.")


def get_project_paths(project_root: Path | None = None) -> ProjectPaths:
    """Build the known project paths without touching filesystem contents."""
    root = resolve_project_root(project_root) if project_root is None else project_root.resolve()
    if not root.is_dir():
        raise PathResolutionError(f"La raiz del proyecto no existe: {root}")

    data_dir = root / "data"
    return ProjectPaths(
        project_root=root,
        data_input_dir=data_dir / "input",
        data_output_dir=data_dir / "output",
        data_backups_dir=data_dir / "backups",
        data_samples_dir=data_dir / "samples",
    )
