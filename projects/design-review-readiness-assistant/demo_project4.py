#!/usr/bin/env python3
"""Live demo runner for Project 4."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

GENERATED_OUTPUTS = [
    "design_review_packet.md",
    "risk_register.csv",
    "assumptions_list.md",
    "validation_test_gaps.md",
    "human_review_required.md",
    "mode_to_test_matrix.md",
    "diagnostic_response_table.md",
]


def run_script(label: str, script_path: Path) -> int:
    print(f"\n{label}", flush=True)
    print(f"Running: python3 {script_path.relative_to(PROJECT_ROOT)}", flush=True)
    result = subprocess.run([sys.executable, str(script_path)], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"\nDemo stopped: {script_path.name} failed with exit code {result.returncode}.")
    return result.returncode


def main() -> int:
    print("Project 4: Design Review Readiness Assistant", flush=True)
    print("=" * 51, flush=True)
    print(
        "Synthetic Codex-assisted automotive lighting workflow demo for preparing "
        "design-review packets, risk registers, validation gaps, mode-to-test "
        "matrices, and diagnostic response tables.",
        flush=True,
    )

    generate_result = run_script(
        "Step 1: Generate structured review artifacts",
        PROJECT_ROOT / "scripts" / "generate_design_review_packet.py",
    )
    if generate_result != 0:
        return generate_result

    validate_result = run_script(
        "Step 2: Validate schema and safety boundaries",
        PROJECT_ROOT / "scripts" / "validate_project4_outputs.py",
    )
    if validate_result != 0:
        return validate_result

    print("\nDemo completed successfully.", flush=True)
    print("Generated outputs:", flush=True)
    for filename in GENERATED_OUTPUTS:
        print(f"- outputs/{filename}", flush=True)

    print("\nAI prepares review artifacts. Qualified engineers own final decisions.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
