"""Deterministic artifact generation for the synthetic requirements prototype."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


BANNER = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts "
    "only. A qualified engineer owns final review and approval."
)
PUBLICATION_CLASSIFICATION = "Needs review"
REVIEWER_PLACEHOLDER = "TBD - qualified engineer review required"
OWNER_PLACEHOLDER = "TBD - qualified engineer"

REQUIRED_COLUMNS = [
    "Requirement_ID",
    "Source_Type",
    "Requirement_Text",
    "Subsystem",
    "Requirement_Type",
    "Verification_Method",
    "Risk_Level",
    "Assumptions",
    "Ambiguity_Flag",
    "Proposed_Test",
    "Human_Review_Status",
]

TRACE_COLUMNS = [
    "Synthetic_Label",
    "Human_Review_Note",
    "Publication_Classification",
    "Requirement_ID",
    "Requirement_Text",
    "Detected_Domain_Category",
    "Verification_Method",
    "Suggested_Verification_Evidence",
    "Acceptance_Criteria",
    "Risk_Ambiguity_Flag",
    "Reviewer_Notes",
]

AMBIGUITY_COLUMNS = [
    "Synthetic_Label",
    "Human_Review_Note",
    "Publication_Classification",
    "Requirement_ID",
    "Issue_Type",
    "Trigger",
    "Explanation",
    "Recommended_Reviewer_Action",
    "Severity",
    "Human_Review_Status",
]

ASSUMPTION_COLUMNS = [
    "Synthetic_Label",
    "Human_Review_Note",
    "Publication_Classification",
    "Assumption_ID",
    "Linked_Requirement_ID",
    "Assumption_Statement",
    "Rationale",
    "Risk_If_Incorrect",
    "Owner_Reviewer",
    "Status",
]

CHECKLIST_COLUMNS = [
    "Synthetic_Label",
    "Human_Review_Note",
    "Publication_Classification",
    "Check_ID",
    "Review_Area",
    "Checklist_Item",
    "Status",
    "Evidence",
    "Reviewer_Notes",
]

WEAK_LANGUAGE_TERMS = [
    "adequate",
    "sufficient",
    "robust",
    "minimize",
    "optimize",
    "as needed",
    "TBD",
    "should",
    "where appropriate",
]

VERIFICATION_METHODS = ["inspection", "analysis", "test", "demonstration", "review"]
PRODUCT_REQUIREMENT_TYPES = {"electrical", "functional", "analysis"}
NUMERIC_RE = re.compile(r"\d+(?:\.\d+)?")
NUMERIC_WITH_UNIT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:v|volt|volts|a|amp|amps|c|degc|deg c|w|watt|watts|%|percent|ms|s)\b",
    re.IGNORECASE,
)
NUMERIC_RANGE_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:v|volt|volts|a|amp|amps|c|degc|deg c|w|watt|watts|%|percent|ms|s)\s+"
    r"(?:to|-)\s+"
    r"\d+(?:\.\d+)?\s*(?:v|volt|volts|a|amp|amps|c|degc|deg c|w|watt|watts|%|percent|ms|s)\b",
    re.IGNORECASE,
)
NUMERIC_LIMIT_KEYWORDS_RE = re.compile(
    r"\b(voltage|range|current|temperature|thermal|threshold|reduce|reduced|intensity|"
    r"limit|minimum|maximum|min|max|exceeds|operate|operating)\b",
    re.IGNORECASE,
)
OPERATING_CONTEXT_RE = re.compile(
    r"\b(voltage|input|temperature|thermal|ambient|current|command|commanded|mode|"
    r"condition|operating|low|high|normal|full-intensity|on|disabled|enabled)\b",
    re.IGNORECASE,
)
STATE_CRITERIA_RE = re.compile(r"\b(enabled|disabled|on|off|active|inactive)\b", re.IGNORECASE)
OUTPUT_CRITERIA_RE = re.compile(
    r"\b(flag|include|record|separate|labeled|labelled|review status|trace matrix)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class CsvLoadResult:
    rows: List[Dict[str, str]]
    warnings: List[str]


@dataclass(frozen=True)
class ArtifactBundle:
    trace_matrix: List[Dict[str, str]]
    ambiguity_report: List[Dict[str, str]]
    assumptions_register: List[Dict[str, str]]
    review_checklist: List[Dict[str, str]]
    summary: Dict[str, str]


def load_requirements(path: Path) -> CsvLoadResult:
    """Load and validate the synthetic requirements CSV."""

    if not path.exists():
        raise FileNotFoundError(f"Missing requirements CSV: {path}")

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [field.strip() for field in reader.fieldnames or []]
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
        if missing_columns:
            joined = ", ".join(missing_columns)
            raise ValueError(f"{path.name} is missing required columns: {joined}")
        rows = [_strip_row(row) for row in reader]

    warnings: List[str] = []
    for index, row in enumerate(rows, start=2):
        row_id = row.get("Requirement_ID") or f"row {index}"
        for column in REQUIRED_COLUMNS:
            if row.get(column, "") == "":
                warnings.append(f"{row_id}: required field {column} is blank in {path.name}.")

    return CsvLoadResult(rows=rows, warnings=warnings)


def build_artifacts(rows: Sequence[Dict[str, str]]) -> ArtifactBundle:
    ambiguity_report = build_ambiguity_report(rows)
    trace_matrix = build_trace_matrix(rows, ambiguity_report)
    assumptions_register = build_assumptions_register(rows, ambiguity_report)
    review_checklist = build_review_checklist(rows, trace_matrix, ambiguity_report, assumptions_register)
    summary = {
        "Requirements loaded": str(len(rows)),
        "Trace matrix rows": str(len(trace_matrix)),
        "Ambiguity findings": str(len(ambiguity_report)),
        "Assumptions": str(len(assumptions_register)),
        "Checklist items": str(len(review_checklist)),
        "Publication classification": PUBLICATION_CLASSIFICATION,
    }
    return ArtifactBundle(
        trace_matrix=trace_matrix,
        ambiguity_report=ambiguity_report,
        assumptions_register=assumptions_register,
        review_checklist=review_checklist,
        summary=summary,
    )


def build_trace_matrix(
    rows: Sequence[Dict[str, str]], ambiguity_report: Sequence[Dict[str, str]]
) -> List[Dict[str, str]]:
    issues_by_requirement: Dict[str, List[Dict[str, str]]] = {}
    for issue in ambiguity_report:
        issues_by_requirement.setdefault(issue["Requirement_ID"], []).append(issue)

    trace_rows: List[Dict[str, str]] = []
    for row in rows:
        requirement_id = row["Requirement_ID"]
        issues = issues_by_requirement.get(requirement_id, [])
        verification_method = normalize_verification_method(row)
        trace_rows.append(
            {
                "Synthetic_Label": BANNER,
                "Human_Review_Note": HUMAN_REVIEW_NOTE,
                "Publication_Classification": PUBLICATION_CLASSIFICATION,
                "Requirement_ID": requirement_id,
                "Requirement_Text": row["Requirement_Text"],
                "Detected_Domain_Category": detect_domain_category(row),
                "Verification_Method": verification_method,
                "Suggested_Verification_Evidence": suggest_verification_evidence(row, verification_method),
                "Acceptance_Criteria": detect_acceptance_criteria(row),
                "Risk_Ambiguity_Flag": summarize_risk(row, issues),
                "Reviewer_Notes": REVIEWER_PLACEHOLDER,
            }
        )
    return trace_rows


def build_ambiguity_report(rows: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    for row in rows:
        findings.extend(find_ambiguity_findings(row))
    return findings


def build_assumptions_register(
    rows: Sequence[Dict[str, str]], ambiguity_report: Sequence[Dict[str, str]]
) -> List[Dict[str, str]]:
    findings_by_requirement: Dict[str, List[Dict[str, str]]] = {}
    for finding in ambiguity_report:
        findings_by_requirement.setdefault(finding["Requirement_ID"], []).append(finding)

    assumptions: List[Dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add_assumption(requirement_id: str, statement: str, rationale: str, risk: str) -> None:
        key = (requirement_id, statement)
        if key in seen:
            return
        seen.add(key)
        assumptions.append(
            {
                "Synthetic_Label": BANNER,
                "Human_Review_Note": HUMAN_REVIEW_NOTE,
                "Publication_Classification": PUBLICATION_CLASSIFICATION,
                "Assumption_ID": f"SYN-ASM-{len(assumptions) + 1:03d}",
                "Linked_Requirement_ID": requirement_id,
                "Assumption_Statement": statement,
                "Rationale": rationale,
                "Risk_If_Incorrect": risk,
                "Owner_Reviewer": OWNER_PLACEHOLDER,
                "Status": "Needs review",
            }
        )

    for row in rows:
        requirement_id = row["Requirement_ID"]
        if row.get("Assumptions"):
            add_assumption(
                requirement_id=requirement_id,
                statement=row["Assumptions"],
                rationale="Captured from the synthetic input assumption field.",
                risk="Verification scope or interpretation may be wrong if the assumption is not reviewed.",
            )

        for finding in findings_by_requirement.get(requirement_id, []):
            issue_type = finding["Issue_Type"]
            if issue_type == "Missing numeric limits":
                add_assumption(
                    requirement_id,
                    "A reviewer-defined synthetic numeric limit will be added before final verification planning.",
                    "The source text refers to a measurable behavior but does not provide a numeric limit.",
                    "The requirement may remain untestable or may be verified against the wrong threshold.",
                )
            elif issue_type == "Missing operating conditions":
                add_assumption(
                    requirement_id,
                    "Operating conditions will be defined during engineer review before verification execution.",
                    "The requirement lacks explicit voltage, temperature, command, mode, or environmental context.",
                    "Verification coverage may miss an important synthetic operating case.",
                )
            elif issue_type == "Missing verification method":
                add_assumption(
                    requirement_id,
                    "The verification method will be assigned by a qualified reviewer.",
                    "The source row did not provide a recognized verification method.",
                    "The requirement may not trace to a reviewable evidence item.",
                )
            elif issue_type == "Unclear pass/fail criteria":
                add_assumption(
                    requirement_id,
                    "Pass/fail criteria will be converted into measurable synthetic reviewer criteria.",
                    "The deterministic parser could not detect a measurable acceptance criterion.",
                    "The review package may imply readiness before the acceptance criteria are testable.",
                )

    return assumptions


def build_review_checklist(
    rows: Sequence[Dict[str, str]],
    trace_matrix: Sequence[Dict[str, str]],
    ambiguity_report: Sequence[Dict[str, str]],
    assumptions_register: Sequence[Dict[str, str]],
) -> List[Dict[str, str]]:
    issue_counts = _count_issue_types(ambiguity_report)
    missing_trace = len(rows) - len(trace_matrix)
    checklist_specs = [
        (
            "SYN-CHK-001",
            "Traceability",
            "Each source requirement has one trace matrix row with requirement ID, text, domain, method, evidence, and review status.",
            "Ready for review" if missing_trace == 0 else "Needs review",
            f"{len(trace_matrix)} trace rows generated from {len(rows)} requirements.",
        ),
        (
            "SYN-CHK-002",
            "Testability",
            "Each requirement has a recognized verification method or a review flag.",
            "Needs review" if issue_counts.get("Missing verification method", 0) else "Ready for review",
            f"{issue_counts.get('Missing verification method', 0)} missing verification method findings.",
        ),
        (
            "SYN-CHK-003",
            "Measurable acceptance criteria",
            "Requirements with measurable behavior have numeric limits, units, or explicit pass/fail criteria.",
            "Needs review"
            if issue_counts.get("Missing numeric limits", 0)
            or issue_counts.get("Unclear pass/fail criteria", 0)
            else "Ready for review",
            (
                f"{issue_counts.get('Missing numeric limits', 0)} numeric-limit findings; "
                f"{issue_counts.get('Unclear pass/fail criteria', 0)} pass/fail findings."
            ),
        ),
        (
            "SYN-CHK-004",
            "Operating voltage/temp conditions",
            "Operating voltage, temperature, command state, or mode context is explicit where needed.",
            "Needs review" if issue_counts.get("Missing operating conditions", 0) else "Ready for review",
            f"{issue_counts.get('Missing operating conditions', 0)} missing operating-condition findings.",
        ),
        (
            "SYN-CHK-005",
            "Environmental conditions",
            "Environmental assumptions are identified or explicitly marked as not included in the synthetic demo.",
            "Needs review",
            "Environmental conditions are not fully defined in the source sample and require reviewer disposition.",
        ),
        (
            "SYN-CHK-006",
            "Verification evidence",
            "Suggested evidence is present for every trace matrix row.",
            "Ready for review"
            if all(row["Suggested_Verification_Evidence"] for row in trace_matrix)
            else "Needs review",
            "Evidence suggestions generated from proposed tests and method templates.",
        ),
        (
            "SYN-CHK-007",
            "Open assumptions",
            "Assumptions are separated from verified facts and linked back to requirement IDs.",
            "Needs review" if assumptions_register else "Ready for review",
            f"{len(assumptions_register)} linked assumptions require review.",
        ),
        (
            "SYN-CHK-008",
            "Human review signoff",
            "A qualified engineer reviews every output before use or publication.",
            "Needs review",
            "Reviewer name, date, disposition, and comments remain placeholders.",
        ),
    ]

    return [
        {
            "Synthetic_Label": BANNER,
            "Human_Review_Note": HUMAN_REVIEW_NOTE,
            "Publication_Classification": PUBLICATION_CLASSIFICATION,
            "Check_ID": check_id,
            "Review_Area": area,
            "Checklist_Item": item,
            "Status": status,
            "Evidence": evidence,
            "Reviewer_Notes": REVIEWER_PLACEHOLDER,
        }
        for check_id, area, item, status, evidence in checklist_specs
    ]


def find_ambiguity_findings(row: Dict[str, str]) -> List[Dict[str, str]]:
    requirement_id = row["Requirement_ID"]
    requirement_text = row["Requirement_Text"]
    method = row.get("Verification_Method", "")
    findings: List[Dict[str, str]] = []

    def add(
        issue_type: str,
        trigger: str,
        explanation: str,
        action: str,
        severity: str = "Medium",
    ) -> None:
        findings.append(
            {
                "Synthetic_Label": BANNER,
                "Human_Review_Note": HUMAN_REVIEW_NOTE,
                "Publication_Classification": PUBLICATION_CLASSIFICATION,
                "Requirement_ID": requirement_id,
                "Issue_Type": issue_type,
                "Trigger": trigger,
                "Explanation": explanation,
                "Recommended_Reviewer_Action": action,
                "Severity": severity,
                "Human_Review_Status": "Needs review",
            }
        )

    for term in WEAK_LANGUAGE_TERMS:
        if _contains_term(requirement_text, term):
            add(
                "Weak language",
                term,
                "Requirement text contains wording that may be interpreted differently by reviewers.",
                "Replace weak language with measurable synthetic criteria or reviewer disposition.",
            )

    if _needs_numeric_limit(row) and not NUMERIC_WITH_UNIT_RE.search(requirement_text):
        add(
            "Missing numeric limits",
            "No numeric limit with unit detected",
            "Requirement refers to a measurable behavior but no numeric limit with unit was detected.",
            "Add a public-safe synthetic limit or keep the requirement open.",
        )

    if NUMERIC_RE.search(requirement_text) and not NUMERIC_WITH_UNIT_RE.search(requirement_text):
        add(
            "Missing units",
            "Number without recognized engineering unit",
            "Requirement includes a number but no recognized engineering unit near the number.",
            "Add units or clarify that the value is not an engineering limit.",
        )

    if _is_product_requirement(row) and not OPERATING_CONTEXT_RE.search(requirement_text):
        add(
            "Missing operating conditions",
            "No operating context detected",
            "Requirement does not state voltage, temperature, command, mode, or operating-condition context.",
            "Add synthetic operating conditions or mark the gap for review.",
        )

    if not _has_recognized_verification_method(method):
        add(
            "Missing verification method",
            method or "blank",
            "Requirement does not include a recognized verification method.",
            "Assign inspection, analysis, test, demonstration, or review.",
            severity="High",
        )

    if not _has_owner_or_reviewer(row):
        add(
            "Unclear owner",
            "No owner/reviewer column detected",
            "Source row does not identify the qualified reviewer or owner.",
            "Assign a reviewer before using the generated package.",
            severity="Low",
        )

    if detect_acceptance_criteria(row).startswith("TBD"):
        add(
            "Unclear pass/fail criteria",
            "No deterministic acceptance criteria detected",
            "Requirement does not provide clear pass/fail criteria in the synthetic source text.",
            "Define measurable acceptance criteria or keep the row open.",
        )

    if row.get("Ambiguity_Flag", "").strip().lower() in {"yes", "y", "true"}:
        add(
            "Source ambiguity flag",
            row.get("Ambiguity_Flag", ""),
            "Synthetic input row was already marked ambiguous.",
            "Review and disposition the flagged row before publication or review use.",
        )

    return findings


def detect_domain_category(row: Dict[str, str]) -> str:
    subsystem = row.get("Subsystem", "").strip()
    requirement_type = row.get("Requirement_Type", "").strip()
    if subsystem and requirement_type:
        return f"{subsystem} / {requirement_type}"
    if subsystem:
        return subsystem
    if requirement_type:
        return requirement_type

    text = row.get("Requirement_Text", "").lower()
    if "thermal" in text or "temperature" in text:
        return "Thermal / Analysis"
    if "voltage" in text or "input" in text:
        return "Power Input / Electrical"
    if "drl" in text:
        return "DRL / Functional"
    if "low beam" in text:
        return "Low Beam / Functional"
    if "high beam" in text:
        return "High Beam / Functional"
    return "Review Workflow / Process"


def normalize_verification_method(row: Dict[str, str]) -> str:
    raw_method = row.get("Verification_Method", "")
    tokens = [
        token.strip().lower()
        for token in re.split(r"\+|/|,|;|\band\b", raw_method)
        if token.strip()
    ]
    recognized = [method for method in VERIFICATION_METHODS if method in tokens]
    if recognized:
        return " + ".join(recognized)

    requirement_type = row.get("Requirement_Type", "").strip().lower()
    text = row.get("Requirement_Text", "").lower()
    if "test" in text or requirement_type in {"functional", "electrical"}:
        return "test"
    if "analysis" in text or requirement_type == "analysis":
        return "analysis"
    if requirement_type in {"governance", "process"}:
        return "inspection"
    return "review"


def suggest_verification_evidence(row: Dict[str, str], verification_method: str) -> str:
    proposed_test = row.get("Proposed_Test", "").strip()
    if proposed_test:
        return f"{proposed_test} using synthetic data; reviewer to verify evidence and status."

    templates = {
        "inspection": "Inspection checklist or generated report section showing required field presence.",
        "analysis": "Synthetic calculation, trace review, or rules-based analysis output.",
        "test": "Synthetic bench-test outline with logged command, input condition, and observed state.",
        "demonstration": "Synthetic demonstration record with reviewer-observed behavior.",
        "review": "Qualified engineer review record with disposition and open items.",
    }
    evidence = [templates[method] for method in VERIFICATION_METHODS if method in verification_method]
    return " ".join(evidence) if evidence else templates["review"]


def detect_acceptance_criteria(row: Dict[str, str]) -> str:
    text = row.get("Requirement_Text", "")
    criteria: List[str] = []
    range_match = NUMERIC_RANGE_RE.search(text)
    if range_match:
        criteria.append(f"Numeric range detected: {range_match.group(0)}.")
    elif NUMERIC_WITH_UNIT_RE.search(text):
        values = ", ".join(match.group(0) for match in NUMERIC_WITH_UNIT_RE.finditer(text))
        criteria.append(f"Numeric value(s) detected: {values}.")

    if STATE_CRITERIA_RE.search(text):
        criteria.append("Expected commanded state is observed for the synthetic operating case.")
    if "threshold" in text.lower():
        criteria.append("Reviewer-defined synthetic threshold triggers the expected review flag.")
    if OUTPUT_CRITERIA_RE.search(text):
        criteria.append("Required output field, label, or report section is present.")

    if criteria:
        return " ".join(criteria)
    return "TBD - define measurable pass/fail criteria during qualified engineer review."


def summarize_risk(row: Dict[str, str], issues: Sequence[Dict[str, str]]) -> str:
    risk_level = row.get("Risk_Level", "Needs review") or "Needs review"
    if not issues:
        return f"{risk_level} risk; no ambiguity findings from deterministic checks."

    issue_types = sorted({issue["Issue_Type"] for issue in issues})
    return f"{risk_level} risk; needs review for {', '.join(issue_types)}."


def write_outputs(output_dir: Path, bundle: ArtifactBundle) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "trace_matrix_csv": output_dir / "trace_matrix.csv",
        "trace_matrix_md": output_dir / "trace_matrix.md",
        "ambiguity_report_csv": output_dir / "ambiguity_report.csv",
        "ambiguity_report_md": output_dir / "ambiguity_report.md",
        "assumptions_register_csv": output_dir / "assumptions_register.csv",
        "assumptions_register_md": output_dir / "assumptions_register.md",
        "review_checklist_csv": output_dir / "review_checklist.csv",
        "review_checklist_md": output_dir / "review_checklist.md",
        "run_summary_md": output_dir / "run_summary.md",
    }

    _write_csv(paths["trace_matrix_csv"], bundle.trace_matrix, TRACE_COLUMNS)
    _write_markdown_table(paths["trace_matrix_md"], "Trace Matrix", bundle.trace_matrix, TRACE_COLUMNS)
    _write_csv(paths["ambiguity_report_csv"], bundle.ambiguity_report, AMBIGUITY_COLUMNS)
    _write_markdown_table(
        paths["ambiguity_report_md"], "Ambiguity Report", bundle.ambiguity_report, AMBIGUITY_COLUMNS
    )
    _write_csv(paths["assumptions_register_csv"], bundle.assumptions_register, ASSUMPTION_COLUMNS)
    _write_markdown_table(
        paths["assumptions_register_md"],
        "Assumptions Register",
        bundle.assumptions_register,
        ASSUMPTION_COLUMNS,
    )
    _write_csv(paths["review_checklist_csv"], bundle.review_checklist, CHECKLIST_COLUMNS)
    _write_markdown_table(paths["review_checklist_md"], "Review Checklist", bundle.review_checklist, CHECKLIST_COLUMNS)
    _write_run_summary(paths["run_summary_md"], bundle)
    return paths


def write_captures(capture_dir: Path, bundle: ArtifactBundle, command: str) -> Dict[str, Path]:
    capture_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "cli": capture_dir / "cli_tool_run.md",
        "trace": capture_dir / "trace_matrix_preview.md",
        "ambiguity": capture_dir / "ambiguity_report_preview.md",
        "assumptions": capture_dir / "assumptions_register_preview.md",
        "checklist": capture_dir / "review_checklist_preview.md",
    }

    cli_lines = [
        "# CLI Tool Run Capture",
        "",
        BANNER,
        "",
        f"> {HUMAN_REVIEW_NOTE}",
        "",
        "Terminal-style mock capture generated from a deterministic local run.",
        "",
        "```text",
        f"$ {command}",
        f"Requirements loaded: {bundle.summary['Requirements loaded']}",
        f"Trace matrix rows: {bundle.summary['Trace matrix rows']}",
        f"Ambiguity findings: {bundle.summary['Ambiguity findings']}",
        f"Assumptions: {bundle.summary['Assumptions']}",
        f"Checklist items: {bundle.summary['Checklist items']}",
        "Human review required before engineering use.",
        "```",
        "",
    ]
    paths["cli"].write_text("\n".join(cli_lines), encoding="utf-8")

    _write_capture_table(paths["trace"], "Trace Matrix Preview", bundle.trace_matrix, TRACE_COLUMNS, limit=5)
    _write_capture_table(paths["ambiguity"], "Ambiguity Report Preview", bundle.ambiguity_report, AMBIGUITY_COLUMNS, limit=8)
    _write_capture_table(
        paths["assumptions"],
        "Assumptions Register Preview",
        bundle.assumptions_register,
        ASSUMPTION_COLUMNS,
        limit=8,
    )
    _write_capture_table(paths["checklist"], "Review Checklist Preview", bundle.review_checklist, CHECKLIST_COLUMNS, limit=8)
    return paths


def _strip_row(row: Dict[str, str]) -> Dict[str, str]:
    return {(key or "").strip(): (value or "").strip() for key, value in row.items() if key is not None}


def _contains_term(text: str, term: str) -> bool:
    pattern = rf"(?<!\w){re.escape(term)}(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def _is_product_requirement(row: Dict[str, str]) -> bool:
    return row.get("Requirement_Type", "").strip().lower() in PRODUCT_REQUIREMENT_TYPES


def _needs_numeric_limit(row: Dict[str, str]) -> bool:
    return _is_product_requirement(row) and NUMERIC_LIMIT_KEYWORDS_RE.search(row.get("Requirement_Text", "")) is not None


def _has_recognized_verification_method(method: str) -> bool:
    if not method.strip():
        return False
    tokens = [
        token.strip().lower()
        for token in re.split(r"\+|/|,|;|\band\b", method)
        if token.strip()
    ]
    return any(token in VERIFICATION_METHODS for token in tokens)


def _has_owner_or_reviewer(row: Dict[str, str]) -> bool:
    owner_columns = ["Owner", "Reviewer", "Responsible_Engineer", "Requirement_Owner"]
    return any(row.get(column, "").strip() for column in owner_columns)


def _count_issue_types(ambiguity_report: Sequence[Dict[str, str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for finding in ambiguity_report:
        counts[finding["Issue_Type"]] = counts.get(finding["Issue_Type"], 0) + 1
    return counts


def _write_csv(path: Path, rows: Sequence[Dict[str, str]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown_table(
    path: Path, title: str, rows: Sequence[Dict[str, str]], columns: Sequence[str]
) -> None:
    lines = _markdown_header(title)
    lines.extend(_table_lines(rows, columns))
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_capture_table(
    path: Path, title: str, rows: Sequence[Dict[str, str]], columns: Sequence[str], limit: int
) -> None:
    lines = _markdown_header(title)
    lines.append("Terminal-style mock capture generated from deterministic synthetic outputs.")
    lines.append("")
    lines.extend(_table_lines(rows[:limit], columns))
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_run_summary(path: Path, bundle: ArtifactBundle) -> None:
    lines = _markdown_header("Requirements-to-Verification Run Summary")
    for key, value in bundle.summary.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            "- trace_matrix.csv / trace_matrix.md",
            "- ambiguity_report.csv / ambiguity_report.md",
            "- assumptions_register.csv / assumptions_register.md",
            "- review_checklist.csv / review_checklist.md",
            "",
            "## Review Boundary",
            "",
            "These outputs accelerate review preparation only. They do not approve engineering requirements, "
            "verification plans, validation evidence, or design decisions.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _markdown_header(title: str) -> List[str]:
    return [
        f"# {title}",
        "",
        BANNER,
        "",
        f"> {HUMAN_REVIEW_NOTE}",
        "",
        f"Publication classification: {PUBLICATION_CLASSIFICATION}",
        "",
    ]


def _table_lines(rows: Sequence[Dict[str, str]], columns: Sequence[str]) -> List[str]:
    if not rows:
        return ["No rows generated.", ""]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_markdown_cell(row.get(column, "")) for column in columns) + " |")
    lines.append("")
    return lines


def _markdown_cell(value: object) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return text if len(text) <= 180 else text[:177] + "..."
