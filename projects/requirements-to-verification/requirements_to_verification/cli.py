"""CLI entry point for the deterministic Requirements-to-Verification prototype."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .core import HUMAN_REVIEW_NOTE, build_artifacts, load_requirements, write_captures, write_outputs


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate synthetic Requirements-to-Verification portfolio artifacts."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Synthetic requirements CSV input.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("projects/requirements-to-verification/generated_outputs"),
        help="Output folder for generated CSV and Markdown artifacts.",
    )
    parser.add_argument(
        "--captures",
        type=Path,
        default=None,
        help="Output folder for terminal-style mock captures. Defaults to a sibling captures folder.",
    )
    args = parser.parse_args(argv)

    load_result = load_requirements(args.input)
    bundle = build_artifacts(load_result.rows)
    output_paths = write_outputs(args.output, bundle)
    capture_dir = args.captures if args.captures is not None else args.output.parent / "captures"
    capture_paths = write_captures(capture_dir, bundle, _format_command(args.input, args.output, capture_dir))

    for warning in load_result.warnings:
        print(f"Input warning: {warning}")
    print(f"Requirements loaded: {bundle.summary['Requirements loaded']}")
    print(f"Trace matrix rows: {bundle.summary['Trace matrix rows']}")
    print(f"Ambiguity findings: {bundle.summary['Ambiguity findings']}")
    print(f"Assumptions: {bundle.summary['Assumptions']}")
    print(f"Checklist items: {bundle.summary['Checklist items']}")
    print(f"Trace matrix: {output_paths['trace_matrix_csv']}")
    print(f"Ambiguity report: {output_paths['ambiguity_report_csv']}")
    print(f"Assumptions register: {output_paths['assumptions_register_csv']}")
    print(f"Review checklist: {output_paths['review_checklist_csv']}")
    print(f"Captures: {capture_paths['cli'].parent}")
    print(HUMAN_REVIEW_NOTE)
    return 0


def _format_command(input_path: Path, output_path: Path, capture_path: Path) -> str:
    return (
        "python3 tools/requirements_to_verification.py "
        f'--input "{input_path}" '
        f'--output "{output_path}" '
        f'--captures "{capture_path}"'
    )


if __name__ == "__main__":
    raise SystemExit(main())
