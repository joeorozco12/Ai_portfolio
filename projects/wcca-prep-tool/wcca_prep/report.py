"""Markdown report generation for synthetic WCCA prep outputs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import List, Optional, Sequence

from .calculations import WccaResult


REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts only. "
    "A qualified engineer owns final review and approval."
)


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
    lines: List[str] = [
        "# Synthetic WCCA Preparation Report",
        "",
        "[SYNTHETIC -- FOR DEMONSTRATION ONLY]",
        "",
        f"> {REVIEW_NOTE}",
        "",
        "## Publication Classification",
        "",
        "Needs review",
        "",
        "## Input Summary",
        "",
        f"- Synthetic WCCA cases loaded: {case_count}",
        f"- Synthetic operating conditions loaded: {condition_count}",
        f"- Calculation rows generated: {len(results)}",
        f"- Missing-data warnings generated: {len(warnings)}",
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
            "## Proof Gaps",
            "",
            "- No screenshots are included yet.",
            "- No plots are included yet.",
            "- No equation-review checklist is included yet.",
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
        "[SYNTHETIC -- FOR DEMONSTRATION ONLY]",
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
