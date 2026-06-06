#!/usr/bin/env python3
"""Generate Project 4 synthetic design-review readiness artifacts."""

from __future__ import annotations

import csv
import html
import re
import shutil
import struct
import subprocess
import tempfile
import zlib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "inputs" / "synthetic_lighting_review_notes.md"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"

BANNER = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW = (
    "Human Review Required: AI-generated outputs are decision-support artifacts "
    "only. A qualified engineer owns final review and approval."
)
PUBLICATION = "Needs review"
ENGINEERING_REVIEW_STATUS = "Needs review"

REVIEWER_FIELDS = {
    "Reviewer": "TBD - qualified engineer",
    "Disposition": "Pending review",
    "Engineering Decision": "No engineering decision - preparation artifact only",
    "Evidence / Rationale": "Synthetic evidence pending",
    "Date Reviewed": "YYYY-MM-DD",
}

REVIEW_TOPICS = {
    "DRN-001": {
        "area": "Operating-mode traceability",
        "risk": "Operating-mode behavior may stay fragmented across low beam, high beam, and DRL notes.",
        "cause": "Mode behavior is described in separate synthetic notes instead of one traceable table.",
        "impact": "Reviewers may miss gaps between lighting modes, requirements, and planned validation evidence.",
        "likelihood": "Medium",
        "severity": "Medium",
        "detection": "Inspect the generated mode-to-test matrix.",
        "mitigation": "Create one synthetic operating-mode trace table before review.",
        "owner": "Systems engineering",
        "status": "Open",
    },
    "DRN-002": {
        "area": "Input-voltage behavior",
        "risk": "Start-up and low-voltage behavior may be underprepared for review.",
        "cause": "The synthetic notes identify a generic input-voltage range but do not define edge-case tests.",
        "impact": "Reviewers may not see how input-voltage conditions connect to proposed validation coverage.",
        "likelihood": "Medium",
        "severity": "Medium",
        "detection": "Review the voltage sweep outline and missing-test list.",
        "mitigation": "Draft synthetic start-up, nominal, low-voltage, and recovery test cases.",
        "owner": "Validation engineering",
        "status": "Needs review",
    },
    "DRN-003": {
        "area": "DRL reduced-current behavior",
        "risk": "DRL reduced-current behavior may remain qualitative without a reviewable synthetic target.",
        "cause": "The public demo intentionally avoids proprietary optical or current targets.",
        "impact": "Reviewers may not know what behavior the synthetic demo is checking.",
        "likelihood": "Medium",
        "severity": "Medium",
        "detection": "Review DRL requirement wording and candidate test fields.",
        "mitigation": "Define a public-safe synthetic reduction target or keep the item open.",
        "owner": "Lighting electronics",
        "status": "Mitigation proposed",
    },
    "DRN-004": {
        "area": "Thermal evidence",
        "risk": "Thermal review trigger may be discussed without supporting synthetic plot evidence.",
        "cause": "The notes reference a demo threshold but no generated plot exists in the input.",
        "impact": "The review packet may not show why thermal follow-up is needed.",
        "likelihood": "Medium",
        "severity": "Medium",
        "detection": "Check whether a synthetic thermal plot and assumptions are attached.",
        "mitigation": "Generate a synthetic thermal trend plot and label the threshold as demo-only.",
        "owner": "Thermal review",
        "status": "Mitigation proposed",
    },
    "DRN-005": {
        "area": "Diagnostic behavior",
        "risk": "Diagnostic response coverage may be incomplete for open-load and short-to-ground review topics.",
        "cause": "Fault injection method and expected response table are not written in the input notes.",
        "impact": "Reviewers may not have a clear diagnostic coverage outline.",
        "likelihood": "Medium",
        "severity": "Medium",
        "detection": "Inspect the diagnostic test outline for method and response fields.",
        "mitigation": "Add a synthetic diagnostic response table and fault injection checklist.",
        "owner": "Validation engineering",
        "status": "Open",
    },
    "DRN-006": {
        "area": "WCCA readiness",
        "risk": "WCCA readiness may be referenced without parameter maturity or tolerance-source status.",
        "cause": "The notes mention LED-driver WCCA preparation but do not summarize readiness.",
        "impact": "Reviewers may confuse referenced WCCA preparation with completed calculation review.",
        "likelihood": "Low",
        "severity": "Medium",
        "detection": "Review the WCCA readiness summary fields.",
        "mitigation": "Separate missing, draft, and reviewed WCCA preparation evidence.",
        "owner": "Electrical engineering",
        "status": "Needs review",
    },
    "DRN-007": {
        "area": "Evidence package",
        "risk": "The public workflow may lack visible proof if screenshots and synthetic evidence remain placeholders.",
        "cause": "Dashboard, packet preview, and export screenshots are not source inputs.",
        "impact": "The portfolio artifact may not demonstrate the workflow end to end.",
        "likelihood": "Medium",
        "severity": "High",
        "detection": "Check the screenshots folder and proof-gap list.",
        "mitigation": "Generate public-safe synthetic screenshots for the dashboard, packet preview, and risk export.",
        "owner": "Portfolio documentation",
        "status": "Mitigation proposed",
    },
    "DRN-008": {
        "area": "Human review boundary",
        "risk": "Readers may misinterpret a preparation packet as an engineering approval artifact.",
        "cause": "Readiness summaries can look authoritative if draft status is not prominent.",
        "impact": "AI-generated preparation output may be mistaken for final engineering judgment.",
        "likelihood": "Low",
        "severity": "High",
        "detection": "Inspect output labels, status fields, and reviewer placeholders.",
        "mitigation": "Repeat the human-review boundary and draft status in every generated artifact.",
        "owner": "Engineering governance",
        "status": "Needs review",
    },
}

ASSUMPTIONS = [
    {
        "Assumption ID": "SYN-DRR-A001",
        "Source Note": "DRN-002",
        "Assumption": "A generic nominal automotive input-voltage range is sufficient for this public demo.",
        "Impact If Wrong": "Test gaps may omit important start-up or low-voltage behavior.",
        "Needed Confirmation": "Define synthetic voltage cases and mark them as demo-only.",
        "Owner": "Electrical engineering",
        "Status": "Needs review",
    },
    {
        "Assumption ID": "SYN-DRR-A002",
        "Source Note": "DRN-003",
        "Assumption": "DRL reduced-current behavior can be represented with a synthetic target.",
        "Impact If Wrong": "Reviewers may not know what behavior the demo is checking.",
        "Needed Confirmation": "Select a public-safe target or keep the item open.",
        "Owner": "Lighting electronics",
        "Status": "Open",
    },
    {
        "Assumption ID": "SYN-DRR-A003",
        "Source Note": "DRN-004",
        "Assumption": "A synthetic thermal threshold can demonstrate thermal review workflow without implying a product limit.",
        "Impact If Wrong": "The threshold may be misread as a validated design limit.",
        "Needed Confirmation": "Add a label stating the threshold is demonstration-only.",
        "Owner": "Thermal review",
        "Status": "Needs review",
    },
    {
        "Assumption ID": "SYN-DRR-A004",
        "Source Note": "DRN-005",
        "Assumption": "Diagnostic response examples can use generic open-load and short-to-ground cases.",
        "Impact If Wrong": "Diagnostic coverage may look incomplete or unrealistic.",
        "Needed Confirmation": "Confirm expected response fields are public-safe and technically plausible.",
        "Owner": "Validation engineering",
        "Status": "Open",
    },
    {
        "Assumption ID": "SYN-DRR-A005",
        "Source Note": "DRN-006",
        "Assumption": "WCCA readiness can be summarized without showing source-specific tolerance data.",
        "Impact If Wrong": "The packet may imply calculations are complete when they are only referenced.",
        "Needed Confirmation": "Add explicit WCCA status and separate assumptions from reviewed evidence.",
        "Owner": "Electrical engineering",
        "Status": "Needs review",
    },
    {
        "Assumption ID": "SYN-DRR-A006",
        "Source Note": "DRN-007",
        "Assumption": "Screenshot placeholders are acceptable for initial structure only.",
        "Impact If Wrong": "The public artifact lacks visual proof of the workflow.",
        "Needed Confirmation": "Replace placeholders with synthetic screenshots before publication.",
        "Owner": "Portfolio documentation",
        "Status": "Mitigation proposed",
    },
]

VALIDATION_GAPS = [
    {
        "Gap ID": "SYN-DRR-G001",
        "Source Note": "DRN-001",
        "Missing Evidence": "Operating-mode trace table for low beam, high beam, and DRL.",
        "Why It Matters": "Reviewers need to see how each mode maps to planned evidence.",
        "Draft Verification Activity": "Inspect a generated mode-to-test matrix.",
        "Blocks Review Prep Completion": "Yes",
        "Status": "Open",
    },
    {
        "Gap ID": "SYN-DRR-G002",
        "Source Note": "DRN-002",
        "Missing Evidence": "Start-up and low-voltage synthetic test cases.",
        "Why It Matters": "Input-voltage behavior is incomplete without defined edge cases.",
        "Draft Verification Activity": "Draft a synthetic bench sweep outline.",
        "Blocks Review Prep Completion": "Yes",
        "Status": "Needs review",
    },
    {
        "Gap ID": "SYN-DRR-G003",
        "Source Note": "DRN-003",
        "Missing Evidence": "DRL reduced-current target and acceptance rationale.",
        "Why It Matters": "Qualitative wording is not enough for review preparation.",
        "Draft Verification Activity": "Define a public-safe synthetic target or keep as open item.",
        "Blocks Review Prep Completion": "Yes",
        "Status": "Open",
    },
    {
        "Gap ID": "SYN-DRR-G004",
        "Source Note": "DRN-004",
        "Missing Evidence": "Thermal trigger plot and assumption notes.",
        "Why It Matters": "Thermal review trigger needs visible supporting evidence.",
        "Draft Verification Activity": "Generate a synthetic thermal trend plot.",
        "Blocks Review Prep Completion": "Yes",
        "Status": "Mitigation proposed",
    },
    {
        "Gap ID": "SYN-DRR-G005",
        "Source Note": "DRN-005",
        "Missing Evidence": "Diagnostic fault injection method and expected response table.",
        "Why It Matters": "Diagnostic behavior needs a reviewable coverage outline.",
        "Draft Verification Activity": "Draft synthetic open-load and short-to-ground checks.",
        "Blocks Review Prep Completion": "Yes",
        "Status": "Open",
    },
    {
        "Gap ID": "SYN-DRR-G006",
        "Source Note": "DRN-006",
        "Missing Evidence": "WCCA readiness summary.",
        "Why It Matters": "Reviewers need to know whether calculations are complete, draft, or missing.",
        "Draft Verification Activity": "Add parameter maturity and tolerance-source status fields.",
        "Blocks Review Prep Completion": "Yes",
        "Status": "Needs review",
    },
    {
        "Gap ID": "SYN-DRR-G007",
        "Source Note": "DRN-007",
        "Missing Evidence": "Public-safe screenshots for the workflow.",
        "Why It Matters": "Portfolio proof is incomplete without visible output examples.",
        "Draft Verification Activity": "Generate synthetic dashboard, packet preview, and risk export screenshots.",
        "Blocks Review Prep Completion": "No",
        "Status": "Mitigation proposed",
    },
]

MODE_TO_TEST_MATRIX = [
    {
        "Mode ID": "SYN-MODE-001",
        "Mode Name": "Low Beam",
        "Input Condition": "Low beam command active with generic nominal input voltage.",
        "Expected Output": "Low beam output is commanded on; other lighting modes remain governed by their command state.",
        "Verification Method": "Synthetic bench functional test",
        "Required Evidence": "Mode-command log and synthetic output-state capture.",
        "Related Risk ID": "SYN-DRR-R001",
        "Status": "Needs review",
    },
    {
        "Mode ID": "SYN-MODE-002",
        "Mode Name": "High Beam",
        "Input Condition": "High beam command active with low beam state recorded for traceability.",
        "Expected Output": "High beam output is commanded on according to the synthetic command table.",
        "Verification Method": "Synthetic command truth-table test",
        "Required Evidence": "Command matrix row and output-state capture.",
        "Related Risk ID": "SYN-DRR-R001",
        "Status": "Needs review",
    },
    {
        "Mode ID": "SYN-MODE-003",
        "Mode Name": "DRL",
        "Input Condition": "Daytime running lamp command active and full-intensity command inactive.",
        "Expected Output": "DRL output uses a reduced-current demo target that remains pending engineer definition.",
        "Verification Method": "Analysis plus synthetic bench check",
        "Required Evidence": "Demo current target, command log, and current-measurement placeholder.",
        "Related Risk ID": "SYN-DRR-R003",
        "Status": "Open",
    },
    {
        "Mode ID": "SYN-MODE-004",
        "Mode Name": "Park Lamp",
        "Input Condition": "Park lamp command active with main forward-lighting commands inactive.",
        "Expected Output": "Park lamp output is commanded on at a synthetic demonstration level.",
        "Verification Method": "Synthetic functional inspection",
        "Required Evidence": "Command-state capture and output-state checklist.",
        "Related Risk ID": "SYN-DRR-R001",
        "Status": "Needs review",
    },
    {
        "Mode ID": "SYN-MODE-005",
        "Mode Name": "Turn Signal",
        "Input Condition": "Turn command active with a generic periodic command profile.",
        "Expected Output": "Turn output follows the synthetic on/off command profile.",
        "Verification Method": "Synthetic timing observation",
        "Required Evidence": "Timing trace placeholder and output-state capture.",
        "Related Risk ID": "SYN-DRR-R001",
        "Status": "Needs review",
    },
    {
        "Mode ID": "SYN-MODE-006",
        "Mode Name": "Welcome Animation",
        "Input Condition": "Synthetic welcome-event trigger active while vehicle state permits demo animation.",
        "Expected Output": "Sequence follows a public-safe synthetic animation step list.",
        "Verification Method": "Synthetic sequence inspection",
        "Required Evidence": "Step list, timing notes, and screen capture placeholder.",
        "Related Risk ID": "SYN-DRR-R007",
        "Status": "Mitigation proposed",
    },
    {
        "Mode ID": "SYN-MODE-007",
        "Mode Name": "Fault / Safe State",
        "Input Condition": "Synthetic diagnostic fault active for the selected channel.",
        "Expected Output": "Affected output enters the configured demo safe state while the review packet records the open diagnostic disposition.",
        "Verification Method": "Synthetic fault injection checklist",
        "Required Evidence": "Fault injection row, response log, and reviewer disposition.",
        "Related Risk ID": "SYN-DRR-R005",
        "Status": "Open",
    },
]

DIAGNOSTIC_RESPONSE_TABLE = [
    {
        "Diagnostic ID": "SYN-DIAG-001",
        "Fault Condition": "Open LED load",
        "Detection Method": "Synthetic current below expected demo range.",
        "Expected System Response": "Record diagnostic flag and command affected channel to the demo response state.",
        "Driver / Control Impact": "Affected lighting output may be unavailable in the synthetic fault case.",
        "Verification Method": "Synthetic open-load fault injection",
        "Related Risk ID": "SYN-DRR-R005",
        "Status": "Open",
    },
    {
        "Diagnostic ID": "SYN-DIAG-002",
        "Fault Condition": "Short to ground",
        "Detection Method": "Synthetic current or voltage signature outside demo range.",
        "Expected System Response": "Limit or disable affected channel in the demonstration response table.",
        "Driver / Control Impact": "Affected output is controlled to the synthetic safe response.",
        "Verification Method": "Synthetic short-to-ground injection",
        "Related Risk ID": "SYN-DRR-R005",
        "Status": "Open",
    },
    {
        "Diagnostic ID": "SYN-DIAG-003",
        "Fault Condition": "Short to battery",
        "Detection Method": "Synthetic output voltage remains high when command is inactive.",
        "Expected System Response": "Flag diagnostic and document the review-needed response path.",
        "Driver / Control Impact": "Unexpected output behavior remains a review item.",
        "Verification Method": "Synthetic short-to-battery injection",
        "Related Risk ID": "SYN-DRR-R005",
        "Status": "Needs review",
    },
    {
        "Diagnostic ID": "SYN-DIAG-004",
        "Fault Condition": "Overtemperature",
        "Detection Method": "Synthetic temperature estimate exceeds demo threshold.",
        "Expected System Response": "Flag thermal review condition and apply demo derating or shutdown response.",
        "Driver / Control Impact": "Output may be reduced or disabled in the synthetic thermal case.",
        "Verification Method": "Synthetic thermal trend review",
        "Related Risk ID": "SYN-DRR-R004",
        "Status": "Mitigation proposed",
    },
    {
        "Diagnostic ID": "SYN-DIAG-005",
        "Fault Condition": "Undervoltage",
        "Detection Method": "Synthetic supply input falls below demo operating threshold.",
        "Expected System Response": "Record condition and evaluate command response in the draft voltage sweep.",
        "Driver / Control Impact": "Output behavior remains pending synthetic test-case definition.",
        "Verification Method": "Synthetic input-voltage sweep",
        "Related Risk ID": "SYN-DRR-R002",
        "Status": "Needs review",
    },
    {
        "Diagnostic ID": "SYN-DIAG-006",
        "Fault Condition": "Overvoltage",
        "Detection Method": "Synthetic supply input rises above demo operating threshold.",
        "Expected System Response": "Record condition and evaluate response using a demo-only voltage case.",
        "Driver / Control Impact": "Output response remains pending engineer review.",
        "Verification Method": "Synthetic input-voltage sweep",
        "Related Risk ID": "SYN-DRR-R002",
        "Status": "Needs review",
    },
    {
        "Diagnostic ID": "SYN-DIAG-007",
        "Fault Condition": "Communication timeout",
        "Detection Method": "Synthetic command message not updated within demo timeout window.",
        "Expected System Response": "Enter a review-defined fallback command state in the preparation table.",
        "Driver / Control Impact": "Output state is controlled by the demo fallback behavior.",
        "Verification Method": "Synthetic timeout simulation",
        "Related Risk ID": "SYN-DRR-R005",
        "Status": "Open",
    },
    {
        "Diagnostic ID": "SYN-DIAG-008",
        "Fault Condition": "Current regulation out of range",
        "Detection Method": "Synthetic measured current deviates from the demo current target.",
        "Expected System Response": "Flag regulation review item and document response in the diagnostic table.",
        "Driver / Control Impact": "Brightness or output availability may be affected in the synthetic case.",
        "Verification Method": "Synthetic current regulation check",
        "Related Risk ID": "SYN-DRR-R003",
        "Status": "Mitigation proposed",
    },
]


def parse_note_table(path: Path) -> list[dict[str, str]]:
    required_columns = [
        "Note ID",
        "Category",
        "Synthetic Review Note",
        "Draft Extraction Target",
    ]
    if path.suffix.lower() in {".md", ".markdown"}:
        notes = parse_markdown_note_table(path, required_columns)
        if not notes:
            raise ValueError(f"No DRN rows found in {path}")
        return notes

    notes: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_columns = [column for column in required_columns if column not in (reader.fieldnames or [])]
        if missing_columns:
            raise ValueError(f"{path.name} missing required columns: {', '.join(missing_columns)}")
        for row in reader:
            note_id = (row.get("Note ID") or "").strip()
            if not re.match(r"^DRN-\d{3}$", note_id):
                raise ValueError(f"Unexpected Note ID in {path.name}: {note_id!r}")
            notes.append({column: (row.get(column) or "").strip() for column in required_columns})
    if not notes:
        raise ValueError(f"No DRN rows found in {path}")
    return notes


def parse_markdown_note_table(path: Path, required_columns: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing synthetic review notes: {path}")

    rows: list[dict[str, str]] = []
    headers = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells:
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if cells == required_columns:
            headers = cells
            continue
        if headers != required_columns or len(cells) != len(headers):
            continue

        row = dict(zip(headers, cells))
        note_id = (row.get("Note ID") or "").strip()
        if not re.match(r"^DRN-\d{3}$", note_id):
            continue
        rows.append({column: (row.get(column) or "").strip() for column in required_columns})

    missing_columns = [] if headers == required_columns else required_columns
    if missing_columns:
        raise ValueError(f"{path.name} missing required Markdown table columns: {', '.join(missing_columns)}")
    return rows


def markdown_table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "") for header in headers) + " |")
    return "\n".join(lines)


def review_record_table() -> str:
    return markdown_table(list(REVIEWER_FIELDS), [REVIEWER_FIELDS])


def topic_rows(notes: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for note in notes:
        topic = REVIEW_TOPICS.get(note["Note ID"])
        if not topic:
            continue
        rows.append(
            {
                "Source Note": note["Note ID"],
                "Input Category": note["Category"],
                "Review Area": topic["area"],
                "Draft Status": topic["status"],
                "Extraction Target": note["Draft Extraction Target"],
            }
        )
    return rows


def risk_rows(notes: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, note in enumerate(notes, start=1):
        topic = REVIEW_TOPICS.get(note["Note ID"])
        if not topic:
            continue
        rows.append(
            {
                "Risk ID": f"SYN-DRR-R{index:03d}",
                "Source Note ID": note["Note ID"],
                "Area": topic["area"],
                "Risk Statement": topic["risk"],
                "Cause": topic["cause"],
                "Potential Impact": topic["impact"],
                "Likelihood": topic["likelihood"],
                "Severity": topic["severity"],
                "Detection": topic["detection"],
                "Proposed Mitigation": topic["mitigation"],
                "Owner": topic["owner"],
                "Status": topic["status"],
                "Human Review Required": HUMAN_REVIEW,
                **REVIEWER_FIELDS,
                "Publication Classification": PUBLICATION,
                "Synthetic Data Label": BANNER,
            }
        )
    return rows


def with_reviewer_fields(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{**row, **REVIEWER_FIELDS} for row in rows]


def write_risk_register(rows: list[dict[str, str]]) -> None:
    headers = [
        "Risk ID",
        "Source Note ID",
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
        "Reviewer",
        "Disposition",
        "Engineering Decision",
        "Evidence / Rationale",
        "Date Reviewed",
        "Publication Classification",
        "Synthetic Data Label",
    ]
    with (OUTPUT_DIR / "risk_register.csv").open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def rows_with_human_review(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            **row,
            "Human Review Required": HUMAN_REVIEW,
            "Publication Classification": PUBLICATION,
            "Synthetic Data Label": BANNER,
        }
        for row in rows
    ]


def write_csv_output(filename: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def write_mode_to_test_matrix() -> None:
    headers = [
        "Mode ID",
        "Mode Name",
        "Input Condition",
        "Expected Output",
        "Verification Method",
        "Required Evidence",
        "Related Risk ID",
        "Status",
        "Human Review Required",
        "Publication Classification",
        "Synthetic Data Label",
    ]
    rows = rows_with_human_review(MODE_TO_TEST_MATRIX)
    write_csv_output("mode_to_test_matrix.csv", headers, rows)

    content = f"""# Synthetic Mode-To-Test Matrix

{BANNER}

> {HUMAN_REVIEW}

Publication classification: {PUBLICATION}

## Preparation-Only Boundary

This matrix is a draft design-review preparation artifact. It makes synthetic lighting-mode behavior, verification needs, required evidence, and related risks easier to inspect before human review. It does not approve mode behavior, verification coverage, validation results, or design readiness.

## Problem

Lighting-mode behavior can be difficult to review when mode inputs, expected outputs, and required evidence are scattered across notes.

## Engineering Context

The matrix uses generated automotive-lighting mode examples only: low beam, high beam, DRL, park lamp, turn signal, welcome animation, and fault safe-state behavior.

## Workflow

1. Parse synthetic review notes.
2. Map review topics into draft mode-to-test rows.
3. Link each mode to a candidate risk.
4. Keep all rows at review-safe status until a qualified engineer reviews them.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- `outputs/mode_to_test_matrix.csv`
- `outputs/mode_to_test_matrix.md`

## Screenshots Or Screenshot Placeholders

- `screenshots/mode_to_test_matrix.png`: generated synthetic matrix mockup.

## Sanitized Sample Data

All rows use generated `SYN-MODE-*` IDs and synthetic lighting-mode behavior.

## Mode-To-Test Matrix

{markdown_table(headers, rows)}

## Reviewer Disposition Fields

{review_record_table()}

## Human Review Controls

- A qualified engineer must review each expected output, verification method, evidence request, and risk link.
- Draft mode rows are preparation prompts, not approved requirements or accepted validation coverage.
- Any final mode behavior or test procedure must be reviewed separately under controlled engineering processes.

## Codex Contribution

Codex generates the draft matrix and links mode rows to synthetic risks.

## Jose Contribution

Jose defines which mode behaviors and evidence requests are meaningful for engineering review and owns final judgment.

## AI Fundamentals Demonstrated

- Structured extraction
- Traceability mapping
- Review-safe output generation

## Engineering Skills Demonstrated

- Mode behavior review
- Verification planning
- Traceability

## Risks And Mitigations

- Risk: Mode rows may look like accepted requirements. Mitigation: keep status as `{PUBLICATION}`, `Open`, or `Mitigation proposed` and require engineer review.

## Next Improvements

- Add reviewer disposition capture.
- Add linkage from each mode row to validation gap closure status.

## Safe-to-Publish Status

{PUBLICATION}. This matrix uses synthetic data only. Engineering review and final validation remain outside this artifact.

## Proof Gaps

- Reviewer disposition is not complete.
- No final validation evidence is attached.
"""
    (OUTPUT_DIR / "mode_to_test_matrix.md").write_text(content, encoding="utf-8")


def write_diagnostic_response_table() -> None:
    headers = [
        "Diagnostic ID",
        "Fault Condition",
        "Detection Method",
        "Expected System Response",
        "Driver / Control Impact",
        "Verification Method",
        "Related Risk ID",
        "Status",
        "Human Review Required",
        "Publication Classification",
        "Synthetic Data Label",
    ]
    rows = rows_with_human_review(DIAGNOSTIC_RESPONSE_TABLE)
    write_csv_output("diagnostic_response_table.csv", headers, rows)

    content = f"""# Synthetic Diagnostic Response Table

{BANNER}

> {HUMAN_REVIEW}

Publication classification: {PUBLICATION}

## Preparation-Only Boundary

This table is a draft design-review preparation artifact. It organizes synthetic diagnostic cases, detection methods, expected responses, control impacts, and verification prompts for human review. It does not approve diagnostic strategy, final fault handling, validation coverage, release readiness, or engineering signoff.

## Problem

Diagnostic expectations can be hard to review when fault conditions, detection methods, expected responses, and verification evidence are not visible in one table.

## Engineering Context

The table uses generated automotive-lighting diagnostic examples only: open LED load, short to ground, short to battery, overtemperature, undervoltage, overvoltage, communication timeout, and current regulation out of range.

## Workflow

1. Parse synthetic review notes.
2. Generate draft diagnostic-response rows.
3. Link each diagnostic case to a candidate risk.
4. Keep every response as a preparation prompt until qualified engineer review.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- `outputs/diagnostic_response_table.csv`
- `outputs/diagnostic_response_table.md`

## Screenshots Or Screenshot Placeholders

- `screenshots/diagnostic_response_table.png`: generated synthetic diagnostic table mockup.

## Sanitized Sample Data

All rows use generated `SYN-DIAG-*` IDs and synthetic diagnostic behavior.

## Diagnostic Response Table

{markdown_table(headers, rows)}

## Reviewer Disposition Fields

{review_record_table()}

## Human Review Controls

- A qualified engineer must review each fault condition, detection method, expected response, control impact, and verification method.
- Draft diagnostic rows do not approve diagnostic strategy or final fault handling.
- Any final diagnostic strategy, validation procedure, or release decision must be reviewed separately under controlled engineering processes.

## Codex Contribution

Codex generates the draft diagnostic table and keeps diagnostic language preparation-only.

## Jose Contribution

Jose determines whether the diagnostic cases and response prompts are technically meaningful and owns final judgment.

## AI Fundamentals Demonstrated

- Diagnostic-case structuring
- Risk linkage
- Review-safe technical summarization

## Engineering Skills Demonstrated

- Diagnostic review preparation
- Validation planning
- Risk traceability

## Risks And Mitigations

- Risk: Draft diagnostic responses may look like accepted strategy. Mitigation: mark each row review-required and state that diagnostic decisions are outside this artifact.

## Next Improvements

- Add reviewer disposition capture.
- Add a synthetic fault-injection checklist.

## Safe-to-Publish Status

{PUBLICATION}. This diagnostic table uses synthetic data only. Engineering review and final validation remain outside this artifact.

## Proof Gaps

- Reviewer disposition is not complete.
- No final diagnostic validation evidence is attached.
"""
    (OUTPUT_DIR / "diagnostic_response_table.md").write_text(content, encoding="utf-8")


def write_design_review_packet(notes: list[dict[str, str]], risks: list[dict[str, str]]) -> None:
    readiness_rows = [
        {"Metric": "Synthetic notes parsed", "Draft Value": str(len(notes)), "Review Meaning": "Input coverage only"},
        {"Metric": "Draft risk rows", "Draft Value": str(len(risks)), "Review Meaning": "Candidate risks, not closure"},
        {"Metric": "Draft assumptions", "Draft Value": str(len(ASSUMPTIONS)), "Review Meaning": "Needs engineer confirmation"},
        {"Metric": "Validation/test gaps", "Draft Value": str(len(VALIDATION_GAPS)), "Review Meaning": "Planning prompts only"},
        {"Metric": "Mode-to-test rows", "Draft Value": str(len(MODE_TO_TEST_MATRIX)), "Review Meaning": "Mode behavior inspection aid"},
        {"Metric": "Diagnostic rows", "Draft Value": str(len(DIAGNOSTIC_RESPONSE_TABLE)), "Review Meaning": "Diagnostic strategy preparation aid"},
        {"Metric": "Publication classification", "Draft Value": PUBLICATION, "Review Meaning": "Public portfolio safety only"},
        {"Metric": "Engineering review state", "Draft Value": ENGINEERING_REVIEW_STATUS, "Review Meaning": "Qualified engineer disposition required"},
    ]
    sample_input_rows = notes[:4]
    sample_output_rows = [
        {"Output Type": "Open questions", "Generated Count": "6", "Review Use": "Focus unresolved design-review prompts"},
        {"Output Type": "Missing information", "Generated Count": str(len(VALIDATION_GAPS)), "Review Use": "Expose evidence and data gaps"},
        {"Output Type": "Risk items", "Generated Count": str(len(risks)), "Review Use": "Create a draft risk register"},
        {"Output Type": "Verification needs", "Generated Count": str(len(MODE_TO_TEST_MATRIX) + len(DIAGNOSTIC_RESPONSE_TABLE)), "Review Use": "Prepare test and diagnostic coverage prompts"},
        {"Output Type": "Follow-up actions", "Generated Count": "7", "Review Use": "Turn review preparation into owner-visible next steps"},
    ]
    open_question_rows = [
        {"Question ID": "SYN-DRR-Q001", "Open Question": "Which lighting modes need traceability in the review packet?", "Source": "DRN-001", "Owner": "Systems engineering"},
        {"Question ID": "SYN-DRR-Q002", "Open Question": "Which synthetic voltage cases should represent start-up and low-voltage behavior?", "Source": "DRN-002", "Owner": "Validation engineering"},
        {"Question ID": "SYN-DRR-Q003", "Open Question": "Should DRL reduced-current behavior use a public-safe numeric target or remain open?", "Source": "DRN-003", "Owner": "Lighting electronics"},
        {"Question ID": "SYN-DRR-Q004", "Open Question": "What demo-only thermal evidence is needed before review?", "Source": "DRN-004", "Owner": "Thermal review"},
        {"Question ID": "SYN-DRR-Q005", "Open Question": "Which diagnostic faults require synthetic response rows before review?", "Source": "DRN-005", "Owner": "Validation engineering"},
        {"Question ID": "SYN-DRR-Q006", "Open Question": "How should WCCA readiness be summarized without exposing source-specific tolerance data?", "Source": "DRN-006", "Owner": "Electrical engineering"},
    ]
    missing_information_rows = [
        {"Missing Item": gap["Missing Evidence"], "Why Needed": gap["Why It Matters"], "Source": gap["Source Note"], "Status": gap["Status"]}
        for gap in VALIDATION_GAPS
    ]
    required_evidence_rows = [
        {"Evidence ID": "SYN-DRR-E001", "Required Evidence": "Synthetic operating-mode trace table", "Supports": "Mode traceability", "Status": "Open"},
        {"Evidence ID": "SYN-DRR-E002", "Required Evidence": "Synthetic voltage sweep outline", "Supports": "Input-voltage behavior", "Status": "Needs review"},
        {"Evidence ID": "SYN-DRR-E003", "Required Evidence": "Demo-only DRL reduction target or open-item disposition", "Supports": "DRL behavior review", "Status": "Open"},
        {"Evidence ID": "SYN-DRR-E004", "Required Evidence": "Synthetic thermal trend plot and assumption note", "Supports": "Thermal review trigger", "Status": "Mitigation proposed"},
        {"Evidence ID": "SYN-DRR-E005", "Required Evidence": "Synthetic diagnostic fault injection table", "Supports": "Diagnostic coverage", "Status": "Open"},
        {"Evidence ID": "SYN-DRR-E006", "Required Evidence": "WCCA readiness summary with parameter maturity fields", "Supports": "Calculation-readiness review", "Status": "Needs review"},
    ]
    verification_need_rows = [
        {"Need ID": row["Mode ID"], "Verification Need": row["Verification Method"], "Evidence": row["Required Evidence"], "Status": row["Status"]}
        for row in MODE_TO_TEST_MATRIX
    ] + [
        {"Need ID": row["Diagnostic ID"], "Verification Need": row["Verification Method"], "Evidence": row["Expected System Response"], "Status": row["Status"]}
        for row in DIAGNOSTIC_RESPONSE_TABLE
    ]
    follow_up_rows = [
        {"Action ID": "SYN-DRR-F001", "Follow-Up Action": "Confirm operating-mode scope and reviewer owner.", "Source": "DRN-001", "Status": "Open"},
        {"Action ID": "SYN-DRR-F002", "Follow-Up Action": "Draft synthetic start-up and low-voltage cases.", "Source": "DRN-002", "Status": "Needs review"},
        {"Action ID": "SYN-DRR-F003", "Follow-Up Action": "Disposition DRL target wording for public demo use.", "Source": "DRN-003", "Status": "Open"},
        {"Action ID": "SYN-DRR-F004", "Follow-Up Action": "Attach synthetic thermal trend evidence.", "Source": "DRN-004", "Status": "Mitigation proposed"},
        {"Action ID": "SYN-DRR-F005", "Follow-Up Action": "Draft diagnostic fault injection checklist.", "Source": "DRN-005", "Status": "Open"},
        {"Action ID": "SYN-DRR-F006", "Follow-Up Action": "Separate WCCA assumptions from reviewed evidence.", "Source": "DRN-006", "Status": "Needs review"},
        {"Action ID": "SYN-DRR-F007", "Follow-Up Action": "Confirm screenshots are synthetic and public-safe.", "Source": "DRN-007/DRN-008", "Status": "Mitigation proposed"},
    ]
    agenda_rows = [
        {"#": "1", "Agenda Item": "Confirm operating-mode traceability table scope.", "Source": "DRN-001"},
        {"#": "2", "Agenda Item": "Review synthetic input-voltage and start-up test cases.", "Source": "DRN-002"},
        {"#": "3", "Agenda Item": "Disposition DRL reduced-current target as open or demo-defined.", "Source": "DRN-003"},
        {"#": "4", "Agenda Item": "Review thermal trigger evidence and assumptions.", "Source": "DRN-004"},
        {"#": "5", "Agenda Item": "Define diagnostic fault injection coverage.", "Source": "DRN-005"},
        {"#": "6", "Agenda Item": "Confirm WCCA readiness summary language.", "Source": "DRN-006"},
        {"#": "7", "Agenda Item": "Review screenshots and publication proof gaps.", "Source": "DRN-007/DRN-008"},
    ]
    risk_summary_headers = [
        "Risk ID",
        "Source Note ID",
        "Area",
        "Severity",
        "Likelihood",
        "Status",
        "Reviewer",
        "Disposition",
        "Engineering Decision",
        "Evidence / Rationale",
        "Date Reviewed",
    ]
    content = f"""# Synthetic Design Review Readiness Report

{BANNER}

> {HUMAN_REVIEW}

Publication classification: {PUBLICATION}

## Preparation-Only Boundary

This packet is a draft design-review preparation artifact. It organizes risks, assumptions, open questions, and evidence gaps from synthetic notes. It does not approve design readiness, close risks, validate requirements, accept test results, or authorize release. AI prepares structured review artifacts; qualified engineers own final judgment.

## Problem

The synthetic lighting review notes contain open risks, assumptions, and evidence gaps that need to be visible before a design review.

## Engineering Context

The example covers generic automotive lighting electronics review preparation for operating modes, input-voltage behavior, DRL current reduction, thermal review triggers, diagnostic behavior, WCCA readiness, and validation evidence planning.

## Workflow

1. Read `inputs/synthetic_lighting_review_notes.md`.
2. Parse the synthetic review-note table.
3. Map each review topic into draft open questions, missing information, assumptions, risk items, required evidence, verification needs, agenda items, and follow-up actions.
4. Export Markdown and CSV artifacts with reviewer disposition placeholders.
5. Run schema checks before treating the package as portfolio-ready.
6. Route all content to a qualified engineer for review before any engineering use.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`
- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- `outputs/synthetic_design_review_readiness_report.md`
- `outputs/design_review_packet.md`
- `outputs/risk_register.csv`
- `outputs/assumptions_list.md`
- `outputs/validation_test_gaps.md`
- `outputs/human_review_required.md`
- `outputs/mode_to_test_matrix.csv`
- `outputs/mode_to_test_matrix.md`
- `outputs/diagnostic_response_table.csv`
- `outputs/diagnostic_response_table.md`
- `screenshots/dashboard_overview.png`
- `screenshots/review_packet_preview.png`
- `screenshots/risk_register_export.png`
- `screenshots/mode_to_test_matrix.png`
- `screenshots/diagnostic_response_table.png`

## Screenshots Or Screenshot Placeholders

- `screenshots/dashboard_overview.png`: generated synthetic readiness dashboard mockup.
- `screenshots/review_packet_preview.png`: generated packet preview mockup.
- `screenshots/risk_register_export.png`: generated risk register export mockup.
- `screenshots/mode_to_test_matrix.png`: generated mode matrix mockup.
- `screenshots/diagnostic_response_table.png`: generated diagnostic table mockup.

## Sanitized Sample Data

The packet uses synthetic note IDs `DRN-001` through `DRN-008` and generated output IDs `SYN-DRR-*`. It contains no real program names, customer names, part numbers, schematic content, BOM data, harness details, cost data, internal validation results, internal requirements, ticket IDs, or local file paths.

## Synthetic Sample Input

{markdown_table(["Note ID", "Category", "Synthetic Review Note", "Draft Extraction Target"], sample_input_rows)}

## Synthetic Sample Output

{markdown_table(["Output Type", "Generated Count", "Review Use"], sample_output_rows)}

## Parsed Review Topics

{markdown_table(["Source Note", "Input Category", "Review Area", "Draft Status", "Extraction Target"], topic_rows(notes))}

## Open Questions

{markdown_table(["Question ID", "Open Question", "Source", "Owner"], open_question_rows)}

## Missing Information

{markdown_table(["Missing Item", "Why Needed", "Source", "Status"], missing_information_rows)}

## Required Evidence

{markdown_table(["Evidence ID", "Required Evidence", "Supports", "Status"], required_evidence_rows)}

## Verification Needs

{markdown_table(["Need ID", "Verification Need", "Evidence", "Status"], verification_need_rows)}

## Draft Readiness Preparation Summary

{markdown_table(["Metric", "Draft Value", "Review Meaning"], readiness_rows)}

## Reviewer Disposition Fields

{review_record_table()}

## Draft Review Agenda

{markdown_table(["#", "Agenda Item", "Source"], agenda_rows)}

## Follow-Up Actions

{markdown_table(["Action ID", "Follow-Up Action", "Source", "Status"], follow_up_rows)}

## Draft Risk Summary

{markdown_table(risk_summary_headers, risks)}

## Draft Assumptions

{markdown_table(["Assumption ID", "Source Note", "Assumption", "Status", "Reviewer", "Disposition", "Engineering Decision", "Evidence / Rationale", "Date Reviewed"], with_reviewer_fields(ASSUMPTIONS))}

## Draft Validation And Test Gaps

{markdown_table(["Gap ID", "Source Note", "Missing Evidence", "Draft Verification Activity", "Status", "Reviewer", "Disposition", "Engineering Decision", "Evidence / Rationale", "Date Reviewed"], with_reviewer_fields(VALIDATION_GAPS))}

## Synthetic Mode-To-Test Matrix Preview

{markdown_table(["Mode ID", "Mode Name", "Input Condition", "Expected Output", "Verification Method", "Required Evidence", "Related Risk ID", "Status", "Human Review Required"], rows_with_human_review(MODE_TO_TEST_MATRIX))}

## Synthetic Diagnostic Response Preview

{markdown_table(["Diagnostic ID", "Fault Condition", "Detection Method", "Expected System Response", "Driver / Control Impact", "Verification Method", "Related Risk ID", "Status", "Human Review Required"], rows_with_human_review(DIAGNOSTIC_RESPONSE_TABLE))}

## Human Review Controls

- AI-generated extraction results are draft decision-support outputs only.
- A qualified engineer must review every risk, assumption, severity, likelihood, gap, mitigation, and agenda item.
- Readiness language must not be treated as design approval.
- Publication is blocked if proprietary or customer-specific details appear.
- Screenshot placeholders must be replaced only with synthetic, public-safe images.

## Codex Contribution

Codex provides the generator, schema checks, output templates, CSV export, screenshot mockups, and repeatable validation workflow.

## Jose Contribution

Jose defines the engineering review criteria, validates whether the extracted items are technically meaningful, sets final risk severity, confirms assumptions, and owns all engineering conclusions.

## AI Fundamentals Demonstrated

- Structured extraction
- Classification under safety constraints
- Risk and assumption tracking
- Gap detection
- Human-in-the-loop review workflow design
- Output validation

## Engineering Skills Demonstrated

- Design-review planning
- Validation readiness assessment
- Risk management
- Assumption management
- Cross-functional review communication
- Engineering governance

## Risks And Mitigations

- Risk: Draft readiness status may be mistaken for approval. Mitigation: mark every section as preparation-only and require engineer review.
- Risk: Extracted severity may be technically wrong. Mitigation: keep severity labels draft until reviewed.
- Risk: Missing evidence may be overlooked. Mitigation: maintain an explicit proof-gap section and validation gap list.
- Risk: Public artifact may accidentally include sensitive information. Mitigation: use only synthetic note IDs and generic subsystem language.

## Next Improvements

- Add a small local UI for reviewer dispositions.
- Add automated tests for Markdown section completeness.
- Add a synthetic fault-injection checklist.
- Add reviewer signoff only after human review is complete.

## Safe-to-Publish Status

{PUBLICATION}. Content is synthetic and public-safe by design. Engineering review, risk closure, and validation approval remain incomplete and require qualified human review.

## Proof Gaps

- Reviewer disposition fields are placeholders.
- No independent reviewer signoff is complete.
- Final validation evidence is not attached.
- Final diagnostic validation evidence is not attached.
"""
    (OUTPUT_DIR / "synthetic_design_review_readiness_report.md").write_text(content, encoding="utf-8")
    (OUTPUT_DIR / "design_review_packet.md").write_text(content, encoding="utf-8")


def write_assumptions_list() -> None:
    rows = with_reviewer_fields(ASSUMPTIONS)
    content = f"""# Draft Assumptions List

{BANNER}

> {HUMAN_REVIEW}

Publication classification: {PUBLICATION}

## Preparation-Only Boundary

These assumptions are draft preparation items extracted from synthetic notes. They are not verified facts and do not approve any engineering decision.

## Problem

Assumptions can be mixed with facts during design-review preparation, which makes open items harder to disposition.

## Engineering Context

The assumptions below use generic automotive lighting topics: input voltage, DRL behavior, thermal review, diagnostics, WCCA readiness, and screenshot evidence.

## Workflow

1. Parse synthetic review notes.
2. Identify statements that need engineering confirmation.
3. Export assumption rows with reviewer disposition placeholders.
4. Keep all rows at draft status until a qualified engineer reviews them.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- Draft assumption register for review preparation.

## Screenshots Or Screenshot Placeholders

- `screenshots/dashboard_overview.png`: generated synthetic dashboard mockup.

## Sanitized Sample Data

All rows use generated IDs and synthetic lighting-review wording.

## Assumptions

{markdown_table(["Assumption ID", "Source Note", "Assumption", "Impact If Wrong", "Needed Confirmation", "Owner", "Status", "Reviewer", "Disposition", "Engineering Decision", "Evidence / Rationale", "Date Reviewed"], rows)}

## Human Review Controls

- Treat each row as a draft extraction.
- Confirm whether the item is a valid engineering assumption or should be rewritten as a risk, requirement, or open question.
- Do not use any assumption as a design input until a qualified engineer reviews it.

## Codex Contribution

Codex generates the draft assumption register and preserves review placeholders.

## Jose Contribution

Jose confirms which assumptions are meaningful and owns final engineering interpretation.

## AI Fundamentals Demonstrated

- Assumption extraction
- Structured output generation
- Human-review workflow design

## Engineering Skills Demonstrated

- Assumption management
- Design-review preparation
- Engineering communication

## Risks And Mitigations

- Risk: Assumptions can be mistaken for facts. Mitigation: keep each row marked as draft and pending review.

## Next Improvements

- Add reviewer disposition filters.
- Add an assumptions-to-risk cross-reference.

## Safe To Publish Status

{PUBLICATION}. The assumptions are synthetic, but final publication review remains incomplete.

## Proof Gaps

- No independent reviewer disposition has been completed.
- No automated cross-check confirms every assumption maps to a risk or gap.
"""
    (OUTPUT_DIR / "assumptions_list.md").write_text(content, encoding="utf-8")


def write_validation_gaps() -> None:
    rows = with_reviewer_fields(VALIDATION_GAPS)
    content = f"""# Draft Validation And Test Gaps

{BANNER}

> {HUMAN_REVIEW}

Publication classification: {PUBLICATION}

## Preparation-Only Boundary

This list identifies missing synthetic evidence for review preparation. It does not define a final validation plan or approve test coverage.

## Problem

Validation gaps can remain hidden until design review if missing evidence is not separated from assumptions and agenda items.

## Engineering Context

The gaps cover generic automotive lighting review preparation for operating modes, input voltage, DRL behavior, thermal evidence, diagnostics, WCCA readiness, and portfolio proof.

## Workflow

1. Parse synthetic review notes.
2. Identify missing evidence and draft verification activities.
3. Export gap rows with reviewer disposition placeholders.
4. Keep activities as planning prompts until a qualified engineer reviews them.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- Draft validation/test gap register for review preparation.

## Screenshots Or Screenshot Placeholders

- `screenshots/review_packet_preview.png`: generated synthetic packet preview mockup.

## Sanitized Sample Data

All rows are synthetic and use generated `SYN-DRR-G*` IDs.

## Validation And Test Gaps

{markdown_table(["Gap ID", "Source Note", "Missing Evidence", "Why It Matters", "Draft Verification Activity", "Blocks Review Prep Completion", "Status", "Reviewer", "Disposition", "Engineering Decision", "Evidence / Rationale", "Date Reviewed"], rows)}

## Human Review Controls

- A qualified engineer must review whether each gap is real, complete, and correctly prioritized.
- Draft verification activities are prompts for planning, not approved test procedures.
- Any final validation plan must be generated and reviewed separately under controlled engineering processes.

## Codex Contribution

Codex generates the draft gap register and keeps validation language preparation-only.

## Jose Contribution

Jose determines whether each gap is technically meaningful and what evidence is needed before review.

## AI Fundamentals Demonstrated

- Gap detection
- Structured planning output
- Review-safe wording

## Engineering Skills Demonstrated

- Validation planning
- Review preparation
- Evidence tracking

## Risks And Mitigations

- Risk: Draft activities may be mistaken for final test procedures. Mitigation: mark activities as planning prompts and require engineer review.

## Next Improvements

- Add automated linkage between gaps and risks.
- Add reviewer disposition capture for each gap.
- Add a synthetic fault-injection checklist.

## Safe To Publish Status

{PUBLICATION}. This gap list is synthetic, but final publication review remains incomplete.

## Proof Gaps

- No independent reviewer disposition has been completed.
- Final validation evidence is not attached.
- Final diagnostic validation evidence is not attached.
"""
    (OUTPUT_DIR / "validation_test_gaps.md").write_text(content, encoding="utf-8")


def write_human_review_required() -> None:
    checklist_rows = [
        {"Check": "Input data is synthetic or sanitized.", **REVIEWER_FIELDS},
        {"Check": "Risk statements are technically meaningful.", **REVIEWER_FIELDS},
        {"Check": "Severity and likelihood labels are reviewed.", **REVIEWER_FIELDS},
        {"Check": "Assumptions are separated from verified facts.", **REVIEWER_FIELDS},
        {"Check": "Validation/test gaps are correctly scoped.", **REVIEWER_FIELDS},
        {"Check": "Screenshots are generated from synthetic data.", **REVIEWER_FIELDS},
        {"Check": "Publication classification is confirmed.", **REVIEWER_FIELDS},
    ]
    content = f"""# Human Review Required Section

{BANNER}

> {HUMAN_REVIEW}

Publication classification: {PUBLICATION}

## Preparation-Only Boundary

This section is included in every Project 4 design-review preparation output. It states that AI-generated packets, risks, assumptions, gaps, and agenda items are not engineering approvals.

## Problem

AI-assisted preparation artifacts can look authoritative unless review ownership and draft status are explicit.

## Engineering Context

This section applies to the synthetic automotive lighting design-review readiness assistant and all generated Project 4 outputs.

## Workflow

1. Generate draft outputs from synthetic notes.
2. Validate that required labels and risk-register fields are present.
3. Route outputs to a qualified engineer.
4. Record reviewer disposition only after human review.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- Required human-review language for generated Project 4 artifacts.

## Screenshots Or Screenshot Placeholders

- `screenshots/risk_register_export.png`: generated synthetic risk register mockup.

## Sanitized Sample Data

This section uses placeholder reviewer fields only.

## Required Review Statement

AI-generated outputs in this project are draft decision-support artifacts. They may help organize notes, identify candidate risks, separate assumptions from facts, and list missing evidence. They do not approve requirements, electrical designs, calculations, validation plans, test results, risk closures, release decisions, or design readiness.

## Reviewer Disposition Checklist

{markdown_table(["Check", "Reviewer", "Disposition", "Engineering Decision", "Evidence / Rationale", "Date Reviewed"], checklist_rows)}

## Human Review Controls

- Keep all outputs at `{PUBLICATION}` until a qualified engineer reviews them.
- Do not present draft readiness as design approval.
- Do not treat AI-generated severity, likelihood, or mitigation labels as accepted engineering judgment.
- Do not include proprietary employer, customer, supplier, program, schematic, BOM, harness, cost, internal test, internal requirement, ticket, part-number, or internal file-path details.

## Codex Contribution

Codex generates this review-control section and validates that the risk register keeps human review visible.

## Jose Contribution

Jose defines the review boundary and owns the final decision on publication and engineering interpretation.

## AI Fundamentals Demonstrated

- Governance prompt design
- Validation of required safety language
- Human-in-the-loop workflow design

## Engineering Skills Demonstrated

- Engineering governance
- Technical review discipline
- Public-safe documentation

## Risks And Mitigations

- Risk: Readers may infer signoff from a clean packet. Mitigation: use explicit preparation-only and review-required language.

## Next Improvements

- Add a reviewer signoff template after qualified review.
- Add a validation test for reviewer field completeness.

## Safe To Publish Status

{PUBLICATION}. This section is synthetic and public-safe by design, but it is still pending final reviewer disposition.

## Proof Gaps

- Reviewer name and date are not filled in.
- Publication classification has not been independently confirmed.
"""
    (OUTPUT_DIR / "human_review_required.md").write_text(content, encoding="utf-8")


def screenshot_html(title: str, subtitle: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    width: 980px;
    height: 800px;
    background: #f5f7f8;
    color: #182026;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
  .page {{ padding: 34px; max-width: 912px; }}
  .banner {{
    padding: 18px 22px;
    border: 1px solid #d7dee3;
    border-radius: 8px;
    background: #ffffff;
  }}
  h1 {{ margin: 0; font-size: 27px; letter-spacing: 0; }}
  .subtitle {{ margin-top: 6px; color: #53616b; font-size: 16px; }}
  .pill {{
    display: inline-block;
    margin-top: 12px;
    border: 1px solid #b98620;
    background: #fff7e6;
    color: #6e4a00;
    border-radius: 999px;
    padding: 8px 12px;
    font-weight: 700;
    font-size: 13px;
  }}
  .grid {{ display: grid; gap: 18px; margin-top: 22px; }}
  .cards {{ grid-template-columns: repeat(2, 1fr); }}
  .card, .panel {{
    background: #ffffff;
    border: 1px solid #d7dee3;
    border-radius: 8px;
    padding: 18px;
    box-sizing: border-box;
  }}
  .card .label {{ color: #53616b; font-size: 13px; text-transform: uppercase; font-weight: 700; }}
  .card .value {{ margin-top: 8px; font-size: 36px; font-weight: 800; }}
  .ok {{ color: #1b7f63; }}
  .warn {{ color: #b16700; }}
  .risk {{ color: #b13f32; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th {{ text-align: left; color: #53616b; font-size: 12px; text-transform: uppercase; border-bottom: 1px solid #d7dee3; padding: 10px 8px; }}
  td {{ border-bottom: 1px solid #edf1f3; padding: 11px 8px; vertical-align: top; }}
  .two {{ grid-template-columns: 1fr; }}
  .note {{
    margin-top: 18px;
    color: #53616b;
    font-size: 13px;
    line-height: 1.35;
  }}
</style>
</head>
<body>
<div class="page">
  <div class="banner">
    <div>
      <h1>{html.escape(title)}</h1>
      <div class="subtitle">{html.escape(subtitle)}</div>
    </div>
    <div class="pill">Needs review · Synthetic demo</div>
  </div>
  {body}
  <div class="note">{html.escape(BANNER)} · {html.escape(HUMAN_REVIEW)}</div>
</div>
</body>
</html>"""


def render_html_to_png(name: str, markup: str) -> None:
    qlmanage = shutil.which("qlmanage")
    if qlmanage:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            html_path = tmp_path / f"{name}.html"
            html_path.write_text(markup, encoding="utf-8")
            try:
                subprocess.run(
                    [qlmanage, "-t", "-s", "1400", "-o", str(tmp_path), str(html_path)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                generated = tmp_path / f"{html_path.name}.png"
                if generated.exists():
                    shutil.copyfile(generated, SCREENSHOT_DIR / f"{name}.png")
                    return
            except subprocess.CalledProcessError:
                pass

    write_fallback_png(SCREENSHOT_DIR / f"{name}.png", markup)


def write_fallback_png(path: Path, markup: str) -> None:
    """Write a deterministic screenshot mockup when Quick Look is unavailable."""

    width = 960
    height = 620
    canvas = [[(245, 247, 248) for _ in range(width)] for _ in range(height)]
    title = html.unescape(_extract_markup_text(markup, r"<h1>(.*?)</h1>", "Design Review Readiness"))
    subtitle = html.unescape(_extract_markup_text(markup, r'<div class="subtitle">(.*?)</div>', "Synthetic portfolio proof artifact"))

    _draw_rect(canvas, 28, 28, width - 28, 132, (255, 255, 255))
    _draw_rect_outline(canvas, 28, 28, width - 28, 132, (215, 222, 227))
    _draw_text(canvas, 48, 48, title[:42], (24, 32, 38), scale=3)
    _draw_text(canvas, 50, 94, subtitle[:70], (83, 97, 107), scale=1)
    _draw_rect(canvas, 50, 148, 314, 190, (255, 247, 230))
    _draw_rect_outline(canvas, 50, 148, 314, 190, (185, 134, 32))
    _draw_text(canvas, 68, 162, "NEEDS REVIEW", (110, 74, 0), scale=2)

    cards = [
        ("SYNTHETIC DATA", "PUBLIC SAFE DRAFT", (27, 127, 99)),
        ("HUMAN REVIEW", "REQUIRED", (177, 103, 0)),
        ("AI ROLE", "PREPARATION ONLY", (177, 63, 50)),
        ("STATUS", "NEEDS REVIEW", (27, 127, 99)),
    ]
    x_positions = [50, 500]
    y_positions = [220, 362]
    card_index = 0
    for y in y_positions:
        for x in x_positions:
            label, value, color = cards[card_index]
            _draw_rect(canvas, x, y, x + 410, y + 112, (255, 255, 255))
            _draw_rect_outline(canvas, x, y, x + 410, y + 112, (215, 222, 227))
            _draw_text(canvas, x + 24, y + 24, label, (83, 97, 107), scale=1)
            _draw_text(canvas, x + 24, y + 56, value[:22], color, scale=2)
            card_index += 1

    _draw_text(canvas, 52, 532, "AI PREPARES REVIEW ARTIFACTS. QUALIFIED ENGINEERS OWN FINAL JUDGMENT.", (83, 97, 107), scale=1)
    _draw_text(canvas, 52, 560, "NO DESIGN APPROVAL OR RELEASE DECISION IS IMPLIED.", (83, 97, 107), scale=1)
    _write_png(path, canvas)


def _extract_markup_text(markup: str, pattern: str, fallback: str) -> str:
    match = re.search(pattern, markup, re.DOTALL)
    if not match:
        return fallback
    return re.sub(r"\s+", " ", match.group(1)).strip()


def _draw_rect(canvas: list[list[tuple[int, int, int]]], x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
    height = len(canvas)
    width = len(canvas[0])
    left = max(0, min(x0, x1))
    right = min(width - 1, max(x0, x1))
    top = max(0, min(y0, y1))
    bottom = min(height - 1, max(y0, y1))
    for y in range(top, bottom + 1):
        row = canvas[y]
        for x in range(left, right + 1):
            row[x] = color


def _draw_rect_outline(canvas: list[list[tuple[int, int, int]]], x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
    _draw_rect(canvas, x0, y0, x1, y0 + 1, color)
    _draw_rect(canvas, x0, y1 - 1, x1, y1, color)
    _draw_rect(canvas, x0, y0, x0 + 1, y1, color)
    _draw_rect(canvas, x1 - 1, y0, x1, y1, color)


def _draw_text(canvas: list[list[tuple[int, int, int]]], x: int, y: int, text: str, color: tuple[int, int, int], scale: int = 1) -> None:
    cursor = x
    for char in text.upper():
        pattern = FONT_5X7.get(char, FONT_5X7[" "])
        for row_index, row in enumerate(pattern):
            for col_index, pixel in enumerate(row):
                if pixel == "1":
                    _draw_rect(
                        canvas,
                        cursor + col_index * scale,
                        y + row_index * scale,
                        cursor + (col_index + 1) * scale - 1,
                        y + (row_index + 1) * scale - 1,
                        color,
                    )
        cursor += 6 * scale


def _write_png(path: Path, canvas: list[list[tuple[int, int, int]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    height = len(canvas)
    width = len(canvas[0])
    raw_rows = [b"\x00" + b"".join(bytes(pixel) for pixel in row) for row in canvas]
    compressed = zlib.compress(b"".join(raw_rows), level=0)

    def chunk(kind: bytes, data: bytes) -> bytes:
        checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)

    png = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
            chunk(b"IDAT", compressed),
            chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(png)


FONT_5X7 = {
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "11100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
}


def write_screenshots(risks: list[dict[str, str]]) -> None:
    dashboard_body = """
<div class="grid cards">
  <div class="card"><div class="label">Review Topics</div><div class="value ok">8</div></div>
  <div class="card"><div class="label">Draft Risks</div><div class="value risk">8</div></div>
  <div class="card"><div class="label">Assumptions</div><div class="value warn">6</div></div>
  <div class="card"><div class="label">Validation Gaps</div><div class="value warn">7</div></div>
</div>
<div class="grid two">
  <div class="panel">
    <table>
      <tr><th>Area</th><th>Status</th><th>Next Review Action</th></tr>
      <tr><td>Operating-mode traceability</td><td>Open</td><td>Create synthetic mode-to-test matrix</td></tr>
      <tr><td>Thermal evidence</td><td>Mitigation proposed</td><td>Generate demo-only thermal plot</td></tr>
      <tr><td>Diagnostics</td><td>Open</td><td>Draft fault injection checklist</td></tr>
      <tr><td>Human review boundary</td><td>Needs review</td><td>Qualified engineer disposition required</td></tr>
    </table>
  </div>
  <div class="panel">
    <h2>Readiness Boundary</h2>
    <p>AI prepares the review packet, risk register, assumptions, and gap list.</p>
    <p>Qualified engineers own final judgment. No design approval is implied.</p>
  </div>
</div>
"""
    packet_body = """
<div class="grid two">
  <div class="panel">
    <h2>Draft Review Agenda</h2>
    <table>
      <tr><th>#</th><th>Agenda item</th><th>Source</th></tr>
      <tr><td>1</td><td>Confirm operating-mode trace table scope</td><td>DRN-001</td></tr>
      <tr><td>2</td><td>Review input-voltage and start-up gaps</td><td>DRN-002</td></tr>
      <tr><td>3</td><td>Disposition DRL target as demo-defined or open</td><td>DRN-003</td></tr>
      <tr><td>4</td><td>Review thermal evidence and assumptions</td><td>DRN-004</td></tr>
      <tr><td>5</td><td>Define diagnostic fault injection coverage</td><td>DRN-005</td></tr>
    </table>
  </div>
  <div class="panel">
    <h2>Reviewer Placeholders</h2>
    <table>
      <tr><th>Field</th><th>Value</th></tr>
      <tr><td>Reviewer</td><td>TBD - qualified engineer</td></tr>
      <tr><td>Disposition</td><td>Pending review</td></tr>
      <tr><td>Engineering Decision</td><td>No decision - preparation artifact only</td></tr>
      <tr><td>Date Reviewed</td><td>YYYY-MM-DD</td></tr>
    </table>
  </div>
</div>
"""
    risk_rows = "\n".join(
        f"<tr><td>{html.escape(row['Risk ID'])}</td><td>{html.escape(row['Area'])}</td>"
        f"<td>{html.escape(row['Severity'])}</td><td>{html.escape(row['Status'])}</td>"
        f"<td>Pending review</td></tr>"
        for row in risks[:6]
    )
    risk_body = f"""
<div class="panel" style="margin-top:22px">
  <table>
    <tr><th>Risk ID</th><th>Area</th><th>Severity</th><th>Status</th><th>Disposition</th></tr>
    {risk_rows}
  </table>
</div>
<div class="grid cards">
  <div class="card"><div class="label">Allowed Status</div><div class="value warn" style="font-size:24px">Needs review</div></div>
  <div class="card"><div class="label">Human Review</div><div class="value ok" style="font-size:24px">Required</div></div>
  <div class="card"><div class="label">AI Role</div><div class="value risk" style="font-size:24px">Prep only</div></div>
  <div class="card"><div class="label">Data Boundary</div><div class="value ok" style="font-size:24px">Synthetic</div></div>
</div>
"""
    mode_rows = "\n".join(
        f"<tr><td>{html.escape(row['Mode ID'])}</td><td>{html.escape(row['Mode Name'])}</td>"
        f"<td>{html.escape(row['Verification Method'])}</td><td>{html.escape(row['Status'])}</td></tr>"
        for row in MODE_TO_TEST_MATRIX
    )
    mode_body = f"""
<div class="panel" style="margin-top:22px">
  <table>
    <tr><th>Mode ID</th><th>Mode</th><th>Verification Method</th><th>Status</th></tr>
    {mode_rows}
  </table>
</div>
<div class="grid cards">
  <div class="card"><div class="label">Modes</div><div class="value ok" style="font-size:24px">7</div></div>
  <div class="card"><div class="label">Review State</div><div class="value warn" style="font-size:24px">Draft</div></div>
</div>
"""
    diagnostic_rows = "\n".join(
        f"<tr><td>{html.escape(row['Diagnostic ID'])}</td><td>{html.escape(row['Fault Condition'])}</td>"
        f"<td>{html.escape(row['Verification Method'])}</td><td>{html.escape(row['Status'])}</td></tr>"
        for row in DIAGNOSTIC_RESPONSE_TABLE[:7]
    )
    diagnostic_body = f"""
<div class="panel" style="margin-top:22px">
  <table>
    <tr><th>Diagnostic ID</th><th>Fault Condition</th><th>Verification Method</th><th>Status</th></tr>
    {diagnostic_rows}
  </table>
</div>
<div class="grid cards">
  <div class="card"><div class="label">Diagnostic Cases</div><div class="value ok" style="font-size:24px">8</div></div>
  <div class="card"><div class="label">Strategy Status</div><div class="value warn" style="font-size:24px">Review needed</div></div>
</div>
"""
    render_html_to_png(
        "dashboard_overview",
        screenshot_html(
            "Design Review Readiness Dashboard",
            "Synthetic automotive lighting preparation assistant",
            dashboard_body,
        ),
    )
    render_html_to_png(
        "review_packet_preview",
        screenshot_html(
            "Review Packet Preview",
            "Draft agenda, reviewer placeholders, and preparation-only controls",
            packet_body,
        ),
    )
    render_html_to_png(
        "risk_register_export",
        screenshot_html(
            "Risk Register Export",
            "CSV-shaped synthetic risk rows with reviewer disposition fields",
            risk_body,
        ),
    )
    render_html_to_png(
        "mode_to_test_matrix",
        screenshot_html(
            "Mode-To-Test Matrix",
            "Synthetic mode behavior and verification prompts for review preparation",
            mode_body,
        ),
    )
    render_html_to_png(
        "diagnostic_response_table",
        screenshot_html(
            "Diagnostic Response Table",
            "Synthetic fault-response prompts for diagnostic review preparation",
            diagnostic_body,
        ),
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    notes = parse_note_table(INPUT_PATH)
    risks = risk_rows(notes)

    write_design_review_packet(notes, risks)
    write_risk_register(risks)
    write_assumptions_list()
    write_validation_gaps()
    write_human_review_required()
    write_mode_to_test_matrix()
    write_diagnostic_response_table()
    write_screenshots(risks)

    print(f"Generated {len(risks)} risk rows from {len(notes)} synthetic notes.")
    print(f"Generated {len(MODE_TO_TEST_MATRIX)} mode-to-test rows.")
    print(f"Generated {len(DIAGNOSTIC_RESPONSE_TABLE)} diagnostic response rows.")
    print(f"Wrote outputs to {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Wrote screenshots to {SCREENSHOT_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
