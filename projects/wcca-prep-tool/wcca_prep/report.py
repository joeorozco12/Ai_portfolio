"""Markdown report generation for synthetic WCCA prep outputs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import List, Optional, Sequence

from .calculations import WccaResult
from .summary import pass_fail_status, result_margin_pct, worst_results_by_case


REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts only. "
    "A qualified engineer owns final review and approval."
)
SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"


def write_report(
    path: Path,
    results: Sequence[WccaResult],
    warnings: Sequence[str],
    case_count: int,
    condition_count: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        _build_report(results, warnings, case_count, condition_count),
        encoding="utf-8",
    )


def write_warnings(path: Path, warnings: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_build_warnings_report(warnings), encoding="utf-8")


def _build_report(
    results: Sequence[WccaResult],
    warnings: Sequence[str],
    case_count: int,
    condition_count: int,
) -> str:
    status_counts = Counter(result.review_status for result in results)
    pass_fail_counts = Counter(pass_fail_status(result) for result in results)
    worst_cases = worst_results_by_case(results)
    lines: List[str] = [
        "# Synthetic WCCA Preparation Report",
        "",
        SYNTHETIC_LABEL,
        "",
        f"> {REVIEW_NOTE}",
        "",
        "## Publication Classification",
        "",
        "Needs review",
        "",
        "## Executive Summary",
        "",
        "This deterministic WCCA preparation report summarizes synthetic automotive lighting and LED-driver stress calculations. It is a pre-review engineering analysis aid and does not approve any engineering decision.",
        "",
        f"- Synthetic cases analyzed: {case_count}",
        f"- Operating conditions analyzed: {condition_count}",
        f"- Case-condition calculation rows: {len(results)}",
        f"- Pass rows: {pass_fail_counts.get('Pass', 0)}",
        f"- Review rows: {pass_fail_counts.get('Review', 0)}",
        f"- Fail rows: {pass_fail_counts.get('Fail', 0)}",
        "",
        "## Input Summary",
        "",
        f"- Synthetic WCCA cases loaded: {case_count}",
        f"- Synthetic operating conditions loaded: {condition_count}",
        f"- Calculation rows generated: {len(results)}",
        f"- Missing-data warnings generated: {len(warnings)}",
        "",
        "## Assumptions",
        "",
        "- All input data is synthetic or sanitized.",
        "- Status thresholds are deterministic preparation thresholds, not final design-approval thresholds.",
        "- Current tolerance and sense-resistor tolerance are applied as additive high-current contributors.",
        "- VF tolerance is applied to the high-voltage LED-string corner.",
        "- Switching-driver losses use low-corner efficiency.",
        "- Linear-channel thermal loss uses positive voltage headroom only.",
        "",
        "## Deterministic Derating Policy",
        "",
        "- Ratio greater than 1.00: Over synthetic limit.",
        "- Ratio from 0.80 to 1.00: Review required.",
        "- Ratio below 0.80 with complete derating inputs: Within synthetic prep limit.",
        "- Missing derating inputs: Review required.",
        "",
        "## Status Summary",
        "",
    ]

    if status_counts:
        for status, count in sorted(status_counts.items()):
            lines.append(f"- {status}: {count}")
    else:
        lines.append("- No calculation rows generated.")

    lines.extend(
        [
            "",
            "## Worst-Case Conditions",
            "",
            "| Case | Worst Condition | Max Ratio | Margin pct | Pass/Fail Status | Review Status |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    for result in worst_cases:
        lines.append(
            "| "
            f"{result.case_id} | "
            f"{result.condition_id} | "
            f"{_fmt_optional(result.max_ratio)} | "
            f"{_fmt_optional(result_margin_pct(result))} | "
            f"{pass_fail_status(result)} | "
            f"{result.review_status} |"
        )

    lines.extend(
        [
            "",
            "## Calculated Margins",
            "",
            "Margins are calculated as `(1 - max stress ratio) * 100`. Negative margin means at least one synthetic preparation limit is exceeded.",
            "",
            "| Case | Condition | Margin pct | Max Ratio | Status |",
            "|---|---|---:|---:|---|",
        ]
    )
    for result in results:
        lines.append(
            "| "
            f"{result.case_id} | "
            f"{result.condition_id} | "
            f"{_fmt_optional(result_margin_pct(result))} | "
            f"{_fmt_optional(result.max_ratio)} | "
            f"{pass_fail_status(result)} |"
        )

    lines.extend(
        [
            "",
            "## Calculation Results",
            "",
            "| Case | Condition | Topology | Pout W | Iin A | Switch A | Max Ratio | Tj C | Status |",
            "|---|---|---|---:|---:|---:|---:|---:|---|",
        ]
    )

    for result in results:
        lines.append(
            "| "
            f"{result.case_id} | "
            f"{result.condition_id} | "
            f"{result.topology} | "
            f"{result.output_power_w:.2f} | "
            f"{result.input_current_a:.3f} | "
            f"{result.switch_current_stress_a:.3f} | "
            f"{_fmt_optional(result.max_ratio)} | "
            f"{_fmt_optional(result.junction_temp_c)} | "
            f"{result.review_status} |"
        )

    lines.extend(
        [
            "",
            "## Missing-Data Warning Summary",
            "",
        ]
    )
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- No missing-data warnings were generated.")

    lines.extend(
        [
            "",
            "## Human Review Controls",
            "",
            "- Treat all calculations as draft WCCA preparation output.",
            "- Verify formulas, units, ratings, tolerance assumptions, and status labels.",
            "- Confirm all data remains synthetic before public use.",
            "- Do not use this output as approval for any engineering decision.",
            "",
            "## Review Notes Placeholder",
            "",
            "- Reviewer notes: _pending qualified engineering review_",
            "- Open questions: _pending qualified engineering review_",
            "- Required corrections: _pending qualified engineering review_",
            "",
            "## Engineer Signoff Placeholder",
            "",
            "| Field | Entry |",
            "|---|---|",
            "| Reviewer name |  |",
            "| Review date |  |",
            "| Review status | Needs review |",
            "| Final engineering conclusion | Not approved by this tool |",
            "",
            "## Proof Gaps",
            "",
            "- Screenshots are mock captures until real screenshots are captured.",
            "- Plot gallery requires qualified review before publication.",
            "- Equation-review checklist is not completed.",
            "- No reviewed signoff record is included yet.",
            "",
            "## Safe to Publish Status",
            "",
            "Needs review. This report uses synthetic data only, but the calculation approach and outputs require qualified engineering review before publication.",
            "",
        ]
    )
    return "\n".join(lines)


def _build_warnings_report(warnings: Sequence[str]) -> str:
    lines = [
        "# Synthetic WCCA Missing-Data Warnings",
        "",
        SYNTHETIC_LABEL,
        "",
        f"> {REVIEW_NOTE}",
        "",
        "## Publication Classification",
        "",
        "Needs review",
        "",
        "## Warning Output",
        "",
    ]
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- No missing-data warnings were generated.")

    lines.extend(
        [
            "",
            "## Proof Gaps",
            "",
            "- Warnings need human disposition before any output is reused in a public demo.",
            "- Missing fields should be completed with synthetic values or explicitly marked as intentionally unavailable.",
            "",
            "## Safe to Publish Status",
            "",
            "Needs review. Warning text uses synthetic IDs only, but it still requires review before publication.",
            "",
        ]
    )
    return "\n".join(lines)


def _fmt_optional(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}"
