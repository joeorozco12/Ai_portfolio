"""Command-line entry point for the synthetic WCCA prep prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

from .calculations import calculate_wcca
from .loaders import load_operating_conditions, load_wcca_cases
from .report import write_report, write_warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic WCCA prep pipeline.")
    parser.add_argument("--cases", type=Path, default=Path("data/synthetic_wcca_cases.csv"))
    parser.add_argument("--conditions", type=Path, default=Path("data/operating_conditions.csv"))
    parser.add_argument("--report", type=Path, default=Path("outputs/synthetic_wcca_report.md"))
    parser.add_argument("--warnings", type=Path, default=Path("outputs/missing_data_warnings.md"))
    args = parser.parse_args()

    case_load = load_wcca_cases(args.cases)
    condition_load = load_operating_conditions(args.conditions)
    bundle = calculate_wcca(case_load.rows, condition_load.rows)
    warnings = [*case_load.warnings, *condition_load.warnings, *bundle.warnings]

    write_report(args.report, bundle.results, warnings, len(case_load.rows), len(condition_load.rows))
    write_warnings(args.warnings, warnings)

    print(f"WCCA results: {len(bundle.results)} rows")
    print(f"Warnings: {len(warnings)}")
    print(f"Report: {args.report}")
    print(f"Warning output: {args.warnings}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
