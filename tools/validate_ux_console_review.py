#!/usr/bin/env python3
"""Validate UX console reviewer-disposition records."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW_LOG = REPO_ROOT / "ux-console" / "review" / "review_log.csv"
DEFAULT_CONSOLE_DATA = REPO_ROOT / "ux-console" / "data" / "portfolio_workflows.js"
REQUIRED_FIELDS = [
    "project_id",
    "object_id",
    "object_type",
    "prior_state",
    "new_state",
    "reviewer_role",
    "review_note",
    "blocker_reason",
    "publication_check",
    "run_marker",
]
REVIEWED_STATES = {"Reviewed demo", "Export ready", "Safe to publish"}
OPEN_STATES = {"Needs review", "Blocked"}
PUBLICATION_CHECKS = {
    "synthetic_label",
    "human_review",
    "restricted_detail",
    "ai_approval_wording",
    "qualified_publication",
}
GENERATED_ARTIFACT_FIELDS = {
    "workflow_summary",
    "project_boundary",
    "source_paths",
    "proof_screens",
    "metrics",
    "review_items",
    "artifacts",
    "safe_to_publish_checks",
}


def load_console_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").strip()
    prefix = "window.PORTFOLIO_WORKFLOWS = "
    if not text.startswith(prefix):
        raise ValueError(f"{path}: console data must start with {prefix!r}")
    json_text = text[len(prefix) :]
    if json_text.endswith(";"):
        json_text = json_text[:-1]
    return json.loads(json_text)


def read_review_log(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        return fieldnames, list(reader)


def parse_publication_check(value: str) -> set[str]:
    normalized = value.strip()
    if not normalized:
        return set()
    return {part.strip() for part in normalized.split("|") if part.strip()}


def validate_review_log(review_log: Path, console_data: Path) -> list[str]:
    errors: list[str] = []
    if not review_log.exists():
        return [f"{review_log}: review log is missing."]
    if not console_data.exists():
        return [f"{console_data}: console data bundle is missing."]
    if review_log.resolve() == console_data.resolve():
        return ["Review decisions must not be stored in the generated console data bundle."]
    try:
        payload = load_console_payload(console_data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    fieldnames, rows = read_review_log(review_log)
    missing_fields = [field for field in REQUIRED_FIELDS if field not in fieldnames]
    if missing_fields:
        errors.append(f"{review_log}: missing required fields: {', '.join(missing_fields)}")
    generated_fields = [field for field in fieldnames if field in GENERATED_ARTIFACT_FIELDS]
    if generated_fields:
        errors.append(
            f"{review_log}: generated artifact fields do not belong in the review log: "
            + ", ".join(generated_fields)
        )

    project_ids = {project["project_id"] for project in payload.get("projects", [])}
    open_states_present = False

    for index, row in enumerate(rows, start=2):
        project_id = row.get("project_id", "").strip()
        object_id = row.get("object_id", "").strip()
        new_state = row.get("new_state", "").strip()
        reviewer_role = row.get("reviewer_role", "").strip()
        review_note = row.get("review_note", "").strip()
        blocker_reason = row.get("blocker_reason", "").strip()
        publication_checks = parse_publication_check(row.get("publication_check", ""))

        if project_id and project_id not in project_ids:
            errors.append(f"row {index}: unknown project_id {project_id!r}.")
        if not object_id:
            errors.append(f"row {index}: object_id is required.")
        if new_state in REVIEWED_STATES and (not reviewer_role or not review_note):
            errors.append(
                f"row {index}: {new_state!r} requires non-empty reviewer_role and review_note."
            )
        if new_state == "Blocked" and not blocker_reason:
            errors.append("row {index}: 'Blocked' requires a blocker_reason.".format(index=index))
        if new_state in OPEN_STATES:
            open_states_present = True
        if new_state == "Safe to publish":
            missing_checks = PUBLICATION_CHECKS - publication_checks
            if missing_checks:
                errors.append(
                    f"row {index}: 'Safe to publish' is missing publication checks: "
                    + ", ".join(sorted(missing_checks))
                )

    if open_states_present and any(row.get("new_state", "").strip() == "Safe to publish" for row in rows):
        errors.append("'Safe to publish' is blocked while any row remains 'Needs review' or 'Blocked'.")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-log", type=Path, default=DEFAULT_REVIEW_LOG)
    parser.add_argument("--console-data", type=Path, default=DEFAULT_CONSOLE_DATA)
    args = parser.parse_args(argv)

    errors = validate_review_log(args.review_log, args.console_data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    relative_log = args.review_log.relative_to(REPO_ROOT) if args.review_log.is_relative_to(REPO_ROOT) else args.review_log
    print(f"UX console review validation passed: {relative_log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
