#!/usr/bin/env python3
"""Validate Project 4 generated outputs for schema and review-safe wording."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
README_PATH = PROJECT_ROOT / "README.md"

BANNER = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_MARKER = "Human Review Required"

REQUIRED_RISK_COLUMNS = [
    "Risk ID",
    "Area",
    "Risk Statement",
    "Cause",
    "Potential Impact",
    "Likelihood",
    "Severity",
    "Detection",
    "Proposed Mitigation",
    "Owner",
    "Status",
    "Human Review Required",
]

REVIEWER_COLUMNS = [
    "Reviewer",
    "Disposition",
    "Engineering Decision",
    "Evidence / Rationale",
    "Date Reviewed",
]

REQUIRED_README_SECTIONS = [
    "Problem",
    "Engineering context",
    "Workflow",
    "Inputs",
    "Outputs",
    "Human review controls",
    "Codex contribution",
    "Jose contribution",
    "How to run",
    "Next improvements",
]

REQUIRED_OUTPUT_FILES = [
    OUTPUT_DIR / "design_review_packet.md",
    OUTPUT_DIR / "risk_register.csv",
    OUTPUT_DIR / "assumptions_list.md",
    OUTPUT_DIR / "validation_test_gaps.md",
    OUTPUT_DIR / "human_review_required.md",
    OUTPUT_DIR / "mode_to_test_matrix.csv",
    OUTPUT_DIR / "mode_to_test_matrix.md",
    OUTPUT_DIR / "diagnostic_response_table.csv",
    OUTPUT_DIR / "diagnostic_response_table.md",
]

MODE_MATRIX_COLUMNS = [
    "Mode ID",
    "Mode Name",
    "Input Condition",
    "Expected Output",
    "Verification Method",
    "Required Evidence",
    "Related Risk ID",
    "Status",
    "Human Review Required",
]

DIAGNOSTIC_COLUMNS = [
    "Diagnostic ID",
    "Fault Condition",
    "Detection Method",
    "Expected System Response",
    "Driver / Control Impact",
    "Verification Method",
    "Related Risk ID",
    "Status",
    "Human Review Required",
]

ALLOWED_STATUSES = {
    "Needs review",
    "Open",
    "Mitigation proposed",
    "Closed after review",
}

APPROVAL_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bAI[- ]?approved\b",
        r"\bapproved by AI\b",
        r"\bAI approves\b",
        r"\bAI approval\b",
        r"\bAI signoff\b",
        r"\bfinal engineering signoff\b",
        r"\bdesign approved\b",
        r"\brelease approved\b",
        r"\bready for production\b",
        r"\bno human review required\b",
        r"\bhuman review not required\b",
    ]
]

MARKDOWN_OUTPUTS = [
    OUTPUT_DIR / "design_review_packet.md",
    OUTPUT_DIR / "assumptions_list.md",
    OUTPUT_DIR / "validation_test_gaps.md",
    OUTPUT_DIR / "human_review_required.md",
    OUTPUT_DIR / "mode_to_test_matrix.md",
    OUTPUT_DIR / "diagnostic_response_table.md",
]

SCREENSHOT_OUTPUTS = [
    SCREENSHOT_DIR / "dashboard_overview.png",
    SCREENSHOT_DIR / "review_packet_preview.png",
    SCREENSHOT_DIR / "risk_register_export.png",
    SCREENSHOT_DIR / "mode_to_test_matrix.png",
    SCREENSHOT_DIR / "diagnostic_response_table.png",
]


def normalize_section_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return re.sub(r"\s+", " ", normalized)


def validate_readme_sections(errors: list[str]) -> None:
    if not README_PATH.exists():
        errors.append("Missing README.md")
        return
    text = README_PATH.read_text(encoding="utf-8")
    headings = {
        normalize_section_name(match.group(1))
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    }
    for section in REQUIRED_README_SECTIONS:
        if normalize_section_name(section) not in headings:
            errors.append(f"README.md missing required section: {section}")
    if BANNER not in text:
        errors.append("README.md missing synthetic-data label")
    if HUMAN_REVIEW_MARKER not in text:
        errors.append("README.md missing human-review marker")


def validate_required_output_files(errors: list[str]) -> None:
    for path in REQUIRED_OUTPUT_FILES:
        if not path.exists():
            errors.append(f"Missing {path.relative_to(PROJECT_ROOT)}")


def validate_risk_register(errors: list[str]) -> None:
    path = OUTPUT_DIR / "risk_register.csv"
    if not path.exists():
        errors.append(f"Missing {path.relative_to(PROJECT_ROOT)}")
        return

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        headers = reader.fieldnames or []

    missing_columns = [column for column in REQUIRED_RISK_COLUMNS if column not in headers]
    missing_reviewer_columns = [column for column in REVIEWER_COLUMNS if column not in headers]
    for column in missing_columns:
        errors.append(f"risk_register.csv missing required column: {column}")
    for column in missing_reviewer_columns:
        errors.append(f"risk_register.csv missing reviewer column: {column}")

    if not rows:
        errors.append("risk_register.csv has no data rows")
        return

    for index, row in enumerate(rows, start=2):
        risk_id = row.get("Risk ID") or f"row {index}"
        status = (row.get("Status") or "").strip()
        if status not in ALLOWED_STATUSES:
            errors.append(f"{risk_id}: unsafe or unexpected Status value: {status!r}")

        human_review = (row.get("Human Review Required") or "").strip()
        if HUMAN_REVIEW_MARKER not in human_review:
            errors.append(f"{risk_id}: Human Review Required field is missing required marker")

        if not all((row.get(column) or "").strip() for column in REVIEWER_COLUMNS):
            errors.append(f"{risk_id}: reviewer disposition placeholders must be populated")

        searchable = " ".join((value or "") for value in row.values())
        for pattern in APPROVAL_PATTERNS:
            if pattern.search(searchable):
                errors.append(f"{risk_id}: wording may imply AI approval or final signoff")


def validate_review_table_csv(
    errors: list[str],
    path: Path,
    required_columns: list[str],
    id_column: str,
) -> None:
    if not path.exists():
        errors.append(f"Missing {path.relative_to(PROJECT_ROOT)}")
        return

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        headers = reader.fieldnames or []

    missing_columns = [column for column in required_columns if column not in headers]
    for column in missing_columns:
        errors.append(f"{path.name} missing required column: {column}")

    if not rows:
        errors.append(f"{path.name} has no data rows")
        return

    for index, row in enumerate(rows, start=2):
        row_id = row.get(id_column) or f"row {index}"
        status = (row.get("Status") or "").strip()
        if status not in ALLOWED_STATUSES:
            errors.append(f"{path.name} {row_id}: unsafe or unexpected Status value: {status!r}")

        human_review = (row.get("Human Review Required") or "").strip()
        if HUMAN_REVIEW_MARKER not in human_review:
            errors.append(f"{path.name} {row_id}: Human Review Required field is missing required marker")

        searchable = " ".join((value or "") for value in row.values())
        for pattern in APPROVAL_PATTERNS:
            if pattern.search(searchable):
                errors.append(f"{path.name} {row_id}: wording may imply AI approval or final signoff")


def validate_markdown_outputs(errors: list[str]) -> None:
    for path in MARKDOWN_OUTPUTS:
        if not path.exists():
            errors.append(f"Missing {path.relative_to(PROJECT_ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if BANNER not in text:
            errors.append(f"{path.name}: missing synthetic-data label")
        if HUMAN_REVIEW_MARKER not in text:
            errors.append(f"{path.name}: missing human-review marker")
        for column in REVIEWER_COLUMNS:
            if column not in text:
                errors.append(f"{path.name}: missing reviewer field {column!r}")
        for pattern in APPROVAL_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.name}: wording may imply AI approval or final signoff")


def validate_screenshots(errors: list[str]) -> None:
    for path in SCREENSHOT_OUTPUTS:
        if not path.exists():
            errors.append(f"Missing {path.relative_to(PROJECT_ROOT)}")
            continue
        if path.stat().st_size < 5000:
            errors.append(f"{path.name}: screenshot file is unexpectedly small")


def main() -> int:
    errors: list[str] = []
    validate_readme_sections(errors)
    validate_required_output_files(errors)
    validate_risk_register(errors)
    validate_review_table_csv(
        errors,
        OUTPUT_DIR / "mode_to_test_matrix.csv",
        MODE_MATRIX_COLUMNS,
        "Mode ID",
    )
    validate_review_table_csv(
        errors,
        OUTPUT_DIR / "diagnostic_response_table.csv",
        DIAGNOSTIC_COLUMNS,
        "Diagnostic ID",
    )
    validate_markdown_outputs(errors)
    validate_screenshots(errors)

    if errors:
        print("Project 4 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Project 4 validation passed.")
    print("README sections, output files, CSV schemas, statuses, human-review fields, reviewer fields, and screenshots are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
