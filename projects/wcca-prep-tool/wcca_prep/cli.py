"""Command-line entry point for the synthetic WCCA prep prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

from .calculations import calculate_wcca
from .captures import write_capture_files
from .loaders import load_operating_conditions, load_wcca_cases
from .plots import write_plot_gallery
from .report import write_report, write_warnings
from .summary import write_summary_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic WCCA prep pipeline.")
    parser.add_argument("--cases", type=Path, default=Path("data/synthetic_wcca_cases.csv"))
    parser.add_argument("--conditions", type=Path, default=Path("data/operating_conditions.csv"))
    parser.add_argument("--report", type=Path, default=Path("outputs/synthetic_wcca_report.md"))
    parser.add_argument("--summary", type=Path, default=Path("outputs/synthetic_wcca_summary.csv"))
    parser.add_argument("--warnings", type=Path, default=Path("outputs/missing_data_warnings.md"))
    parser.add_argument("--plots-dir", type=Path, default=Path("outputs/plots"))
    parser.add_argument("--captures-dir", type=Path, default=Path("captures"))
    args = parser.parse_args()

    case_load = load_wcca_cases(args.cases)
    condition_load = load_operating_conditions(args.conditions)
    bundle = calculate_wcca(case_load.rows, condition_load.rows)
    warnings = [*case_load.warnings, *condition_load.warnings, *bundle.warnings]

    write_report(args.report, bundle.results, warnings, len(case_load.rows), len(condition_load.rows))
    write_summary_csv(args.summary, bundle.results)
    write_warnings(args.warnings, warnings)
    plot_paths = write_plot_gallery(args.plots_dir, bundle.results)
    capture_paths = write_capture_files(
        args.captures_dir,
        bundle.results,
        warnings,
        plot_paths,
        args.summary,
        args.report,
    )

    print(f"WCCA results: {len(bundle.results)} rows")
    print(f"Warnings: {len(warnings)}")
    print(f"Summary CSV: {args.summary}")
    print(f"Report: {args.report}")
    print(f"Warning output: {args.warnings}")
    print(f"Plots: {args.plots_dir}")
    print(f"Captures: {args.captures_dir}")
    print(f"Capture files: {len(capture_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
