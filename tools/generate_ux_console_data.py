#!/usr/bin/env python3
"""Generate the static UX console data bundle from portfolio artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "ux-console" / "data" / "portfolio_workflows.js"
SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts only. "
    "A qualified engineer owns final review and approval."
)
NEEDS_REVIEW = "Needs review"


def read_csv(relative_path: str) -> list[dict[str, str]]:
    path = REPO_ROOT / relative_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_text(relative_path: str) -> str:
    path = REPO_ROOT / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def list_existing_files(relative_dir: str, suffixes: tuple[str, ...]) -> list[str]:
    directory = REPO_ROOT / relative_dir
    if not directory.exists():
        return []
    return sorted(
        str(path.relative_to(REPO_ROOT))
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in suffixes
    )


def artifact(label: str, path: str, kind: str, status: str = NEEDS_REVIEW) -> dict[str, str]:
    exists = (REPO_ROOT / path).exists()
    return {
        "label": label,
        "path": path,
        "kind": kind,
        "status": status if exists else "Missing",
    }


def metric(label: str, value: int | str, tone: str = "neutral") -> dict[str, int | str]:
    return {"label": label, "value": value, "tone": tone}


def state_count(rows: list[dict[str, str]], *fields: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for field in fields:
            value = row.get(field, "").strip()
            if value:
                counts[value] += 1
                break
    return counts


def make_review_item(
    *,
    item_id: str,
    item_type: str,
    source: str,
    summary: str,
    state: str = NEEDS_REVIEW,
    severity: str = "Medium",
    action: str,
) -> dict[str, str]:
    return {
        "id": item_id,
        "type": item_type,
        "source": source,
        "summary": summary,
        "state": state,
        "severity": severity,
        "recommended_action": action,
    }


def base_project(
    *,
    project_id: str,
    title: str,
    short_title: str,
    route: str,
    workflow_summary: str,
    source_paths: list[str],
    proof_screens: list[str],
    metrics: list[dict[str, int | str]],
    review_items: list[dict[str, str]],
    artifacts: list[dict[str, str]],
    screen_tabs: list[str],
    status_counts: dict[str, int],
    project_boundary: str,
) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "title": title,
        "short_title": short_title,
        "route": route,
        "synthetic_label": SYNTHETIC_LABEL,
        "human_review_note": HUMAN_REVIEW_NOTE,
        "publication_classification": NEEDS_REVIEW,
        "workflow_summary": workflow_summary,
        "project_boundary": project_boundary,
        "source_paths": source_paths,
        "proof_screens": proof_screens,
        "metrics": metrics,
        "review_items": review_items,
        "artifacts": artifacts,
        "screen_tabs": screen_tabs,
        "status_counts": status_counts,
        "safe_to_publish_checks": [
            {"label": "Synthetic/demo label visible", "state": "Present"},
            {"label": "Human-review note visible", "state": "Present"},
            {"label": "Restricted identifier screen", "state": NEEDS_REVIEW},
            {"label": "AI-approval wording check", "state": NEEDS_REVIEW},
            {"label": "Qualified publication review", "state": NEEDS_REVIEW},
        ],
    }


def requirements_to_verification() -> dict[str, Any]:
    trace = read_csv("projects/requirements-to-verification/generated_outputs/trace_matrix.csv")
    ambiguity = read_csv("projects/requirements-to-verification/generated_outputs/ambiguity_report.csv")
    assumptions = read_csv("projects/requirements-to-verification/generated_outputs/assumptions_register.csv")
    checklist = read_csv("projects/requirements-to-verification/generated_outputs/review_checklist.csv")

    open_ambiguity = [row for row in ambiguity if row.get("Human_Review_Status") == NEEDS_REVIEW]
    open_assumptions = [row for row in assumptions if row.get("Status") == NEEDS_REVIEW]
    mapping_gaps = [
        row
        for row in trace
        if "TBD" in row.get("Acceptance_Criteria", "")
        or "needs review" in row.get("Risk_Ambiguity_Flag", "").lower()
    ]
    checklist_open = [row for row in checklist if row.get("Status") == NEEDS_REVIEW]

    review_items: list[dict[str, str]] = []
    for row in open_ambiguity[:5]:
        review_items.append(
            make_review_item(
                item_id=f"{row.get('Requirement_ID', 'REQ')}-{row.get('Issue_Type', 'Issue')}",
                item_type="Ambiguity",
                source=row.get("Requirement_ID", "Unknown requirement"),
                summary=f"{row.get('Issue_Type', 'Review issue')}: {row.get('Explanation', '')}",
                severity=row.get("Severity", "Medium"),
                action=row.get("Recommended_Reviewer_Action", "Record reviewer disposition."),
            )
        )
    for row in open_assumptions[:4]:
        review_items.append(
            make_review_item(
                item_id=row.get("Assumption_ID", "Assumption"),
                item_type="Assumption",
                source=row.get("Linked_Requirement_ID", "Unknown requirement"),
                summary=row.get("Assumption_Statement", "Assumption needs review."),
                severity="Medium",
                action="Accept for demo, revise, reject, escalate, or block export.",
            )
        )

    return base_project(
        project_id="requirements-to-verification",
        title="Requirements-to-Verification Tool",
        short_title="Req to Verification",
        route="#requirements-to-verification",
        workflow_summary=(
            "Turns synthetic requirement rows into trace matrices, ambiguity findings, "
            "assumptions, and review checklists."
        ),
        source_paths=["Synthetic Requirements Sample.csv"],
        proof_screens=[
            "Reviewer dashboard",
            "Ambiguity triage",
            "Requirement detail",
            "Trace matrix review",
            "Export package summary",
        ],
        metrics=[
            metric("Requirements processed", len(trace)),
            metric("Open ambiguity findings", len(open_ambiguity), "warning"),
            metric("Unresolved assumptions", len(open_assumptions), "warning"),
            metric("Verification mapping gaps", len(mapping_gaps), "warning"),
            metric("Checklist items needing review", len(checklist_open), "warning"),
            metric("Export-ready rows", 0),
        ],
        review_items=review_items,
        artifacts=[
            artifact("Trace matrix", "projects/requirements-to-verification/generated_outputs/trace_matrix.csv", "CSV"),
            artifact("Ambiguity report", "projects/requirements-to-verification/generated_outputs/ambiguity_report.csv", "CSV"),
            artifact("Assumptions register", "projects/requirements-to-verification/generated_outputs/assumptions_register.csv", "CSV"),
            artifact("Review checklist", "projects/requirements-to-verification/generated_outputs/review_checklist.csv", "CSV"),
            artifact("Run summary", "projects/requirements-to-verification/generated_outputs/run_summary.md", "Markdown"),
        ],
        screen_tabs=["Dashboard", "Review Queue", "Artifacts", "Publish Gate"],
        status_counts=dict(state_count(ambiguity, "Human_Review_Status") + state_count(assumptions, "Status")),
        project_boundary="Generated mappings are decision-support only; reviewer dispositions remain separate from source outputs.",
    )


def wcca_prep() -> dict[str, Any]:
    rows = read_csv("projects/wcca-prep-tool/outputs/synthetic_wcca_summary.csv")
    warning_text = read_text("projects/wcca-prep-tool/outputs/missing_data_warnings.md")
    plots = list_existing_files("projects/wcca-prep-tool/outputs/plots", (".png",))
    review_rows = [
        row
        for row in rows
        if row.get("Pass_Fail_Status") != "Pass" or row.get("Review_Status") == "Review required"
    ]
    missing_warning_count = warning_text.count("Review required") + warning_text.count("Missing")

    review_items = [
        make_review_item(
            item_id=f"{row.get('Case_ID', 'Case')}-{row.get('Condition_ID', 'Condition')}",
            item_type="WCCA result",
            source=row.get("Case_ID", "Unknown case"),
            summary=row.get("Review_Reason", "Calculated row needs review."),
            state=row.get("Review_Status", NEEDS_REVIEW),
            severity="Medium" if row.get("Pass_Fail_Status") == "Review" else "Low",
            action="Verify formulas, assumptions, thresholds, and missing-data warnings.",
        )
        for row in review_rows[:8]
    ]

    return base_project(
        project_id="wcca-prep",
        title="AI-Assisted WCCA Prep Tool",
        short_title="WCCA Prep",
        route="#wcca-prep",
        workflow_summary=(
            "Prepares synthetic WCCA inputs, calculation rows, warning reports, plots, "
            "and equation-review evidence."
        ),
        source_paths=[
            "projects/wcca-prep-tool/data/synthetic_wcca_cases.csv",
            "projects/wcca-prep-tool/data/operating_conditions.csv",
        ],
        proof_screens=[
            "Parameter audit table",
            "Missing-data warnings",
            "WCCA result table",
            "Plot gallery",
            "Equation review checklist",
        ],
        metrics=[
            metric("Calculation rows", len(rows)),
            metric("Rows requiring review", len(review_rows), "warning"),
            metric("Missing-data warning markers", missing_warning_count, "warning"),
            metric("Plot artifacts", len(plots)),
            metric("Export-ready rows", 0),
        ],
        review_items=review_items,
        artifacts=[
            artifact("WCCA summary", "projects/wcca-prep-tool/outputs/synthetic_wcca_summary.csv", "CSV"),
            artifact("WCCA report", "projects/wcca-prep-tool/outputs/synthetic_wcca_report.md", "Markdown"),
            artifact("Missing-data warnings", "projects/wcca-prep-tool/outputs/missing_data_warnings.md", "Markdown"),
            artifact("Equation review checklist", "projects/wcca-prep-tool/docs/equation_review_checklist.md", "Markdown"),
            *[artifact(Path(path).stem.replace("_", " ").title(), path, "PNG") for path in plots],
        ],
        screen_tabs=["Dashboard", "Review Queue", "Artifacts", "Publish Gate"],
        status_counts=dict(state_count(rows, "Review_Status", "Pass_Fail_Status")),
        project_boundary="This workflow prepares WCCA review artifacts; it is not a final WCCA approval tool.",
    )


def design_review_readiness() -> dict[str, Any]:
    risks = read_csv("projects/design-review-readiness-assistant/outputs/risk_register.csv")
    mode_rows = read_csv("projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.csv")
    diagnostic_rows = read_csv("projects/design-review-readiness-assistant/outputs/diagnostic_response_table.csv")
    screenshots = list_existing_files("projects/design-review-readiness-assistant/screenshots", (".png",))
    open_risks = [row for row in risks if row.get("Status") != "Closed"]

    review_items = [
        make_review_item(
            item_id=row.get("Risk ID", "Risk"),
            item_type="Risk",
            source=row.get("Area", "Review area"),
            summary=row.get("Risk Statement", "Risk needs review."),
            state=row.get("Status", NEEDS_REVIEW),
            severity=row.get("Severity", "Medium"),
            action=row.get("Proposed Mitigation", "Record reviewer disposition."),
        )
        for row in open_risks[:8]
    ]

    return base_project(
        project_id="design-review-readiness",
        title="Design Review Readiness Assistant",
        short_title="Design Review",
        route="#design-review-readiness",
        workflow_summary=(
            "Converts synthetic review notes into risks, assumptions, validation gaps, "
            "mode matrices, diagnostic tables, and review packets."
        ),
        source_paths=["projects/design-review-readiness-assistant/inputs/synthetic_lighting_review_notes.md"],
        proof_screens=[
            "Readiness dashboard",
            "Risk register",
            "Validation gaps",
            "Mode-to-test matrix",
            "Diagnostic response table",
            "Review packet preview",
        ],
        metrics=[
            metric("Risk rows", len(risks)),
            metric("Open review risks", len(open_risks), "warning"),
            metric("Mode-to-test rows", len(mode_rows)),
            metric("Diagnostic rows", len(diagnostic_rows)),
            metric("Screenshot artifacts", len(screenshots)),
            metric("Export-ready rows", 0),
        ],
        review_items=review_items,
        artifacts=[
            artifact("Design review packet", "projects/design-review-readiness-assistant/outputs/design_review_packet.md", "Markdown"),
            artifact("Risk register", "projects/design-review-readiness-assistant/outputs/risk_register.csv", "CSV"),
            artifact("Validation gaps", "projects/design-review-readiness-assistant/outputs/validation_test_gaps.md", "Markdown"),
            artifact("Mode-to-test matrix", "projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.csv", "CSV"),
            artifact("Diagnostic response table", "projects/design-review-readiness-assistant/outputs/diagnostic_response_table.csv", "CSV"),
            *[artifact(Path(path).stem.replace("_", " ").title(), path, "PNG") for path in screenshots],
        ],
        screen_tabs=["Dashboard", "Review Queue", "Artifacts", "Publish Gate"],
        status_counts=dict(state_count(risks, "Status")),
        project_boundary="Readiness means organized preparation context; it does not approve design release or validation strategy.",
    )


def lighting_feasibility() -> dict[str, Any]:
    rows = read_csv("projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.csv")
    sensitivity_rows = read_csv("projects/lighting-feasibility-mini-simulator/outputs/sensitivity/sensitivity_summary.csv")
    plots = list_existing_files("projects/lighting-feasibility-mini-simulator/outputs/plots", (".png",))
    sensitivity_plots = list_existing_files("projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots", (".png",))
    flagged = [row for row in rows if row.get("Status") in {"Marginal", "Fail"}]

    review_items = [
        make_review_item(
            item_id=row.get("Case_ID", "Case"),
            item_type="Feasibility case",
            source=row.get("Load_Name", "Synthetic load"),
            summary=row.get("Reason", "Case needs review."),
            state=row.get("Status", NEEDS_REVIEW),
            severity="High" if row.get("Status") == "Fail" else "Medium",
            action=row.get("Recommended_Next_Step", "Run deeper engineering review."),
        )
        for row in flagged[:8]
    ]

    return base_project(
        project_id="lighting-feasibility",
        title="Lighting Feasibility Mini-Simulator",
        short_title="Feasibility",
        route="#lighting-feasibility",
        workflow_summary=(
            "Runs first-pass deterministic screening for synthetic lighting loads, "
            "margins, status reasons, and sensitivity sweeps."
        ),
        source_paths=["projects/lighting-feasibility-mini-simulator/data/synthetic_lighting_cases.csv"],
        proof_screens=[
            "Case input table",
            "Feasibility status summary",
            "Margin plots",
            "Sensitivity sweep explorer",
            "Risk flag summary",
            "Export summary",
        ],
        metrics=[
            metric("Feasibility cases", len(rows)),
            metric("Marginal or fail cases", len(flagged), "warning"),
            metric("Sensitivity rows", len(sensitivity_rows)),
            metric("Plot artifacts", len(plots) + len(sensitivity_plots)),
            metric("Export-ready rows", 0),
        ],
        review_items=review_items,
        artifacts=[
            artifact("Feasibility summary", "projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.csv", "CSV"),
            artifact("Feasibility report", "projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.md", "Markdown"),
            artifact("Sensitivity summary", "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/sensitivity_summary.csv", "CSV"),
            artifact("Portfolio capture summary", "projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md", "Markdown"),
            *[artifact(Path(path).stem.replace("_", " ").title(), path, "PNG") for path in plots],
            *[artifact(Path(path).stem.replace("_", " ").title(), path, "PNG") for path in sensitivity_plots],
        ],
        screen_tabs=["Dashboard", "Review Queue", "Artifacts", "Publish Gate"],
        status_counts=dict(state_count(rows, "Status")),
        project_boundary="Pass means first-pass screening only; every formula, threshold, and assumption remains review-owned.",
    )


def build_portfolio_workflows() -> dict[str, Any]:
    projects = [
        requirements_to_verification(),
        wcca_prep(),
        design_review_readiness(),
        lighting_feasibility(),
    ]
    open_review_count = sum(len(project["review_items"]) for project in projects)
    artifact_count = sum(len(project["artifacts"]) for project in projects)
    return {
        "generated_from": "tools/generate_ux_console_data.py",
        "synthetic_label": SYNTHETIC_LABEL,
        "human_review_note": HUMAN_REVIEW_NOTE,
        "publication_classification": NEEDS_REVIEW,
        "review_log_policy": "Reviewer decisions are stored separately from generated deterministic outputs.",
        "projects": projects,
        "portfolio_metrics": [
            metric("Projects in console", len(projects)),
            metric("Review items surfaced", open_review_count, "warning"),
            metric("Artifacts indexed", artifact_count),
            metric("Safe-to-publish status", NEEDS_REVIEW, "warning"),
        ],
    }


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    projects = payload.get("projects", [])
    if len(projects) != 4:
        errors.append("Expected four project payloads.")
    for project in projects:
        title = project.get("title", "Unknown project")
        if project.get("synthetic_label") != SYNTHETIC_LABEL:
            errors.append(f"{title}: missing synthetic label.")
        if "Human Review Required" not in project.get("human_review_note", ""):
            errors.append(f"{title}: missing human-review note.")
        if project.get("publication_classification") != NEEDS_REVIEW:
            errors.append(f"{title}: publication classification must remain Needs review.")
        if not project.get("review_items"):
            errors.append(f"{title}: expected at least one surfaced review item.")
        if not project.get("artifacts"):
            errors.append(f"{title}: expected indexed artifacts.")
        if not project.get("route", "").startswith("#"):
            errors.append(f"{title}: route must be a hash route for static hosting.")
    return errors


def write_bundle(payload: dict[str, Any], output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(payload, indent=2, ensure_ascii=False)
    output_path.write_text(
        "window.PORTFOLIO_WORKFLOWS = " + json_text + ";\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--check", action="store_true", help="Validate without writing.")
    args = parser.parse_args()

    payload = build_portfolio_workflows()
    errors = validate_payload(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if not args.check:
        write_bundle(payload, args.output)
        print(f"Wrote {args.output.relative_to(REPO_ROOT)}")
    else:
        print("UX console data validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
