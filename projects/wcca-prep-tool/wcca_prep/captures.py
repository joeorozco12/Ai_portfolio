"""Clearly labeled mock capture artifacts for the synthetic WCCA portfolio demo."""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence

from .calculations import WccaResult
from .report import REVIEW_NOTE
from .summary import pass_fail_status, result_margin_pct, worst_results_by_case


SYNTHETIC_LABEL = "[SYNTHETIC -- FOR DEMONSTRATION ONLY]"
MOCK_NOTE = "Mock capture: terminal-style portfolio proof artifact, not a live screenshot."


def write_capture_files(
    path: Path,
    results: Sequence[WccaResult],
    warnings: Sequence[str],
    plot_paths: Sequence[Path],
    summary_path: Path,
    report_path: Path,
) -> List[Path]:
    path.mkdir(parents=True, exist_ok=True)
    files = [
        path / "cli_run_mock.md",
        path / "generated_summary_table_mock.md",
        path / "plot_gallery_preview_mock.md",
        path / "report_preview_mock.md",
        path / "test_run_output_mock.md",
    ]
    files[0].write_text(_cli_capture(results, warnings, summary_path, report_path), encoding="utf-8")
    files[1].write_text(_summary_capture(results), encoding="utf-8")
    files[2].write_text(_plot_capture(plot_paths), encoding="utf-8")
    files[3].write_text(_report_capture(report_path), encoding="utf-8")
    files[4].write_text(_test_capture(), encoding="utf-8")
    return files


def _header(title: str) -> List[str]:
    return [
        f"# {title}",
        "",
        SYNTHETIC_LABEL,
        "",
        f"> {REVIEW_NOTE}",
        "",
        f"> {MOCK_NOTE}",
        "",
    ]


def _cli_capture(
    results: Sequence[WccaResult],
    warnings: Sequence[str],
    summary_path: Path,
    report_path: Path,
) -> str:
    lines = _header("CLI Run Mock Capture")
    lines.extend(
        [
            "```text",
            "python3 -m wcca_prep.cli",
            f"WCCA results: {len(results)} rows",
            f"Warnings: {len(warnings)}",
            f"Summary CSV: {summary_path.as_posix()}",
            f"Report: {report_path.as_posix()}",
            "Plots: outputs/plots",
            "Captures: captures",
            "```",
            "",
            "This capture demonstrates repeatable regeneration of deterministic WCCA proof assets.",
            "",
        ]
    )
    return "\n".join(lines)


def _summary_capture(results: Sequence[WccaResult]) -> str:
    lines = _header("Generated WCCA Summary Table Mock Capture")
    lines.extend(
        [
            "| Case | Worst Condition | Margin pct | Status |",
            "|---|---|---:|---|",
        ]
    )
    for result in worst_results_by_case(results)[:15]:
        margin = result_margin_pct(result)
        margin_text = "N/A" if margin is None else f"{margin:.2f}"
        lines.append(
            f"| {result.case_id} | {result.condition_id} | {margin_text} | {pass_fail_status(result)} |"
        )
    lines.append("")
    return "\n".join(lines)


def _plot_capture(plot_paths: Sequence[Path]) -> str:
    lines = _header("Plot Gallery Preview Mock Capture")
    lines.extend(["## Generated Plot Assets", ""])
    for plot_path in plot_paths:
        lines.append(f"- `{plot_path.as_posix()}`")
    lines.extend(["", "These PNG files are generated from synthetic deterministic WCCA output."])
    return "\n".join(lines)


def _report_capture(report_path: Path) -> str:
    lines = _header("Report Preview Mock Capture")
    lines.extend(
        [
            f"Report artifact: `{report_path.as_posix()}`",
            "",
            "Preview sections:",
            "",
            "- Executive summary",
            "- Input dataset summary",
            "- Worst-case conditions",
            "- Calculated margins",
            "- Assumptions",
            "- Review notes placeholder",
            "- Engineer signoff placeholder",
            "",
        ]
    )
    return "\n".join(lines)


def _test_capture() -> str:
    lines = _header("Test Run Output Mock Capture")
    lines.extend(
        [
            "```text",
            "python3 -m unittest discover -s tests",
            "OK",
            "",
            "python3 -m unittest discover -s projects/wcca-prep-tool/tests",
            "OK",
            "```",
            "",
            "This capture is a placeholder until a real terminal screenshot is captured.",
            "",
        ]
    )
    return "\n".join(lines)
