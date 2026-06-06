"""Save and load helpers for `.ledcurve.json` project files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import LedCurveProject


PROJECT_FILE_EXTENSION = ".ledcurve.json"


def save_project(project: LedCurveProject, path: str | Path) -> Path:
    """Write a deterministic `.ledcurve.json` project file."""

    output_path = _validate_project_path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(project.to_dict(), indent=2, sort_keys=True) + "\n"
    output_path.write_text(content, encoding="utf-8")
    return output_path


def load_project(path: str | Path) -> LedCurveProject:
    """Load and validate a `.ledcurve.json` project file."""

    input_path = _validate_project_path(path)
    payload: dict[str, Any] = json.loads(input_path.read_text(encoding="utf-8"))
    return LedCurveProject.from_dict(payload)


def _validate_project_path(path: str | Path) -> Path:
    project_path = Path(path)
    if not project_path.name.endswith(PROJECT_FILE_EXTENSION):
        raise ValueError("Project files must use the .ledcurve.json extension.")
    return project_path
