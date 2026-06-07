#!/usr/bin/env python3
"""Validate the local deterministic portfolio toolbench."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_MARKER = "Human Review Required"
NEEDS_REVIEW = "Needs review"

PRIMARY_CHECKS = [
    (
        "Project 1 regenerate Requirements-to-Verification outputs",
        [PYTHON, "tools/requirements_to_verification.py", "--input", "Synthetic Requirements Sample.csv", "--output", "projects/requirements-to-verification/generated_outputs"],
        REPO_ROOT,
    ),
    (
        "Project 1 unit tests",
        [PYTHON, "-m", "unittest", "discover", "-s", "tests"],
        REPO_ROOT / "projects" / "requirements-to-verification",
    ),
    (
        "Project 2 regenerate WCCA proof assets",
        [PYTHON, "-m", "wcca_prep.cli"],
        REPO_ROOT / "projects" / "wcca-prep-tool",
    ),
    (
        "Project 2 WCCA unit tests",
        [PYTHON, "-m", "unittest", "discover", "-s", "tests"],
        REPO_ROOT / "projects" / "wcca-prep-tool",
    ),
    (
        "Project 4 demo generator and validator",
        [PYTHON, "demo_project4.py"],
        REPO_ROOT / "projects" / "design-review-readiness-assistant",
    ),
    (
        "Project 5 regenerate feasibility and sensitivity outputs",
        [PYTHON, "feasibility_engine.py"],
        REPO_ROOT / "projects" / "lighting-feasibility-mini-simulator",
    ),
    (
        "Project 5 unit tests",
        [PYTHON, "-m", "unittest", "discover", "-s", "tests"],
        REPO_ROOT / "projects" / "lighting-feasibility-mini-simulator",
    ),
]

SECONDARY_CHECKS = [
    (
        "Curve Studio regenerate deterministic export package",
        [PYTHON, "run_demo.py"],
        REPO_ROOT / "projects" / "wcca-prep-tool" / "datasheet-plot-digitizer",
    ),
    (
        "Curve Studio deterministic tests",
        [PYTHON, "-m", "unittest", "discover", "-s", "tests"],
        REPO_ROOT / "projects" / "wcca-prep-tool" / "datasheet-plot-digitizer",
    ),
]

REQUIRED_TEXT_ARTIFACTS = [
    "UNVEIL_READINESS.md",
    "LOCAL_TOOLBENCH.md",
    "Screenshot Index.md",
    "LED Datasheet-to-Model Extractor README.md",
    "projects/codex-tool-development-case-study.md",
    "projects/codex-tool-development-case-study/README.md",
    "projects/codex-tool-development-case-study/codex_workflow_case_study.md",
    "projects/codex-tool-development-case-study/validation_checklist.md",
    "projects/codex-tool-development-case-study/examples/safe_task_prompt.md",
    "projects/codex-tool-development-case-study/examples/scope_control_example.md",
    "projects/codex-tool-development-case-study/examples/validation_log_example.md",
    "projects/codex-tool-development-case-study/examples/human_review_boundary.md",
    "projects/codex-tool-development-case-study/captures/codex_task_prompt.md",
    "projects/codex-tool-development-case-study/captures/scoped_file_tree.md",
    "projects/codex-tool-development-case-study/captures/validation_log.md",
    "projects/codex-tool-development-case-study/captures/human_review_boundary.md",
    "projects/requirements-to-verification/generated_outputs/trace_matrix.md",
    "projects/requirements-to-verification/generated_outputs/ambiguity_report.md",
    "projects/requirements-to-verification/generated_outputs/assumptions_register.md",
    "projects/requirements-to-verification/generated_outputs/review_checklist.md",
    "projects/requirements-to-verification/generated_outputs/run_summary.md",
    "projects/requirements-to-verification/generated_outputs/trace_matrix.csv",
    "projects/requirements-to-verification/generated_outputs/ambiguity_report.csv",
    "projects/requirements-to-verification/generated_outputs/assumptions_register.csv",
    "projects/requirements-to-verification/generated_outputs/review_checklist.csv",
    "projects/wcca-prep-tool/outputs/synthetic_wcca_report.md",
    "projects/wcca-prep-tool/outputs/missing_data_warnings.md",
    "projects/wcca-prep-tool/outputs/synthetic_wcca_summary.csv",
    "projects/wcca-prep-tool/captures/cli_run_mock.md",
    "projects/wcca-prep-tool/captures/generated_summary_table_mock.md",
    "projects/wcca-prep-tool/captures/plot_gallery_preview_mock.md",
    "projects/wcca-prep-tool/captures/report_preview_mock.md",
    "projects/wcca-prep-tool/captures/test_run_output_mock.md",
    "projects/design-review-readiness-assistant/outputs/design_review_packet.md",
    "projects/design-review-readiness-assistant/outputs/risk_register.csv",
    "projects/design-review-readiness-assistant/outputs/assumptions_list.md",
    "projects/design-review-readiness-assistant/outputs/validation_test_gaps.md",
    "projects/design-review-readiness-assistant/outputs/human_review_required.md",
    "projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.md",
    "projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.csv",
    "projects/design-review-readiness-assistant/outputs/diagnostic_response_table.md",
    "projects/design-review-readiness-assistant/outputs/diagnostic_response_table.csv",
    "projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.md",
    "projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.csv",
    "projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/sensitivity_summary.md",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/sensitivity_summary.csv",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/ambient_temperature_sweep.csv",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/led_current_sweep.csv",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/thermal_resistance_sweep.csv",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/optical_efficiency_sweep.csv",
]

REQUIRED_BINARY_ARTIFACTS = [
    "projects/wcca-prep-tool/outputs/plots/margin_by_case.png",
    "projects/wcca-prep-tool/outputs/plots/worst_case_result_by_condition.png",
    "projects/wcca-prep-tool/outputs/plots/pass_fail_distribution.png",
    "projects/wcca-prep-tool/outputs/plots/thermal_temperature_sensitivity.png",
    "projects/wcca-prep-tool/outputs/plots/voltage_sensitivity.png",
    "projects/design-review-readiness-assistant/screenshots/dashboard_overview.png",
    "projects/design-review-readiness-assistant/screenshots/review_packet_preview.png",
    "projects/design-review-readiness-assistant/screenshots/risk_register_export.png",
    "projects/design-review-readiness-assistant/screenshots/mode_to_test_matrix.png",
    "projects/design-review-readiness-assistant/screenshots/diagnostic_response_table.png",
    "projects/lighting-feasibility-mini-simulator/outputs/plots/thermal_margin_by_case.png",
    "projects/lighting-feasibility-mini-simulator/outputs/plots/current_margin_by_case.png",
    "projects/lighting-feasibility-mini-simulator/outputs/plots/feasibility_status_count.png",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/ambient_temperature_sweep.png",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/led_current_sweep.png",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/thermal_resistance_sweep.png",
    "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/optical_efficiency_sweep.png",
]

FORBIDDEN_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bAI[- ]?approved\b",
        r"\bapproved by AI\b",
        r"\bAI approves\b",
        r"\bAI approval\b",
        r"\bAI signoff\b",
        r"\bno human review required\b",
        r"\bhuman review not required\b",
        r"\bready for production\b",
        r"\brelease approved\b",
        r"\bdesign approved\b",
    ]
]


@dataclass
class CheckResult:
    name: str
    returncode: int
    duration_s: float
    blocking: bool
    output_tail: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def main() -> int:
    print("Local CLI Toolbench Validation")
    print("=" * 32)
    print("Primary workflows are release-blocking. Curve Studio is secondary.")

    results: list[CheckResult] = []
    for name, command, cwd in PRIMARY_CHECKS:
        results.append(run_command(name, command, cwd, blocking=True))

    artifact_result = validate_artifacts()
    results.append(artifact_result)

    for name, command, cwd in SECONDARY_CHECKS:
        results.append(run_command(name, command, cwd, blocking=False))

    print_summary(results)
    primary_failures = [result for result in results if result.blocking and not result.passed]
    return 1 if primary_failures else 0


def run_command(name: str, command: list[str], cwd: Path, blocking: bool) -> CheckResult:
    start = time.monotonic()
    print(f"\n[RUN] {name}")
    print(f"cwd: {cwd.relative_to(REPO_ROOT)}")
    print("cmd: " + " ".join(quote_arg(part) for part in command))
    env = os.environ.copy()
    env.setdefault("PYTHONPYCACHEPREFIX", "/private/tmp/ai_portfolio_pycache")
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        env=env,
    )
    duration_s = time.monotonic() - start
    output = "\n".join(part for part in [completed.stdout, completed.stderr] if part)
    tail = tail_lines(output, limit=12)
    status = "PASS" if completed.returncode == 0 else "FAIL"
    print(f"[{status}] {name} ({duration_s:.1f}s)")
    if tail:
        print(tail)
    return CheckResult(name, completed.returncode, duration_s, blocking, tail)


def validate_artifacts() -> CheckResult:
    start = time.monotonic()
    print("\n[RUN] Artifact safety metadata")
    errors: list[str] = []

    for relative_path in REQUIRED_TEXT_ARTIFACTS:
        path = REPO_ROOT / relative_path
        if not path.exists():
            errors.append(f"Missing {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        require_text(relative_path, text, SYNTHETIC_LABEL, errors)
        require_text(relative_path, text, HUMAN_REVIEW_MARKER, errors)
        require_text(relative_path, text, NEEDS_REVIEW, errors)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{relative_path}: wording may imply AI approval or final signoff")

    for relative_path in REQUIRED_BINARY_ARTIFACTS:
        path = REPO_ROOT / relative_path
        if not path.exists():
            errors.append(f"Missing {relative_path}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"{relative_path}: file is empty")

    duration_s = time.monotonic() - start
    if errors:
        output = "\n".join(f"- {error}" for error in errors)
        print(f"[FAIL] Artifact safety metadata ({duration_s:.1f}s)")
        print(output)
        return CheckResult("Artifact safety metadata", 1, duration_s, True, output)

    output = (
        f"Checked {len(REQUIRED_TEXT_ARTIFACTS)} text artifacts and "
        f"{len(REQUIRED_BINARY_ARTIFACTS)} binary artifacts."
    )
    print(f"[PASS] Artifact safety metadata ({duration_s:.1f}s)")
    print(output)
    return CheckResult("Artifact safety metadata", 0, duration_s, True, output)


def require_text(relative_path: str, text: str, marker: str, errors: list[str]) -> None:
    if marker not in text:
        errors.append(f"{relative_path}: missing {marker!r}")


def print_summary(results: Iterable[CheckResult]) -> None:
    results = list(results)
    print("\nSummary")
    print("-" * 32)
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        scope = "primary" if result.blocking else "secondary"
        print(f"{status:4}  {scope:9}  {result.name} ({result.duration_s:.1f}s)")


def quote_arg(value: str) -> str:
    if re.search(r"\s", value):
        return f'"{value}"'
    return value


def tail_lines(value: str, limit: int) -> str:
    lines = [line.rstrip() for line in value.splitlines() if line.strip()]
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(["...", *lines[-limit:]])


if __name__ == "__main__":
    raise SystemExit(main())
