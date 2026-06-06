#!/usr/bin/env python3
"""Root-level wrapper for Project 1 Requirements-to-Verification."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1] / "projects" / "requirements-to-verification"
sys.path.insert(0, str(PROJECT_DIR))

from requirements_to_verification.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
