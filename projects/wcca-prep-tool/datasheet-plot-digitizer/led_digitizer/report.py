"""Review-report builders for LED Datasheet Curve Studio exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .calibration import EngineeringPoint


SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts "
    "only. A qualified engineer owns final review and approval."
)
EXPORT_PACKAGE_SCHEMA_VERSION = "led_curve_export_package_1.0"
VALIDATION_STATUS_PENDING_REVIEW = "draft_validation_pending_engineer_review"
DEFAULT_ASSUMPTIONS = [
    "Source plot is synthetic or public and cleared for demonstration use.",
    "Manual axis calibration points were entered by the operator.",
    "Manual curve picks are treated as draft until overlay review is complete.",
    "Digitized plot data is reference-only and not a guaranteed device limit.",
]
DOWNSTREAM_USE_WARNINGS = [
    "Do not use this export for WCCA, feasibility simulation, thermal derating, luminous-flux prediction, design review, or design decisions until a qualified engineer reviews and accepts it.",
    "Lookup functions clamp outside the digitized x-range; they are not validated extrapolation models.",
    "Curve-fit coefficients must be checked against the raw points and overlay image before downstream use.",
    "Synthetic demo identifiers are not real device, supplier, customer, program, schematic, BOM, harness, cost, validation, ticket, repository, or internal-document references.",
]


def build_report_context(
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
    artifacts: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build the structured, JSON-safe context shared by reports and manifests."""

    sorted_points = _sorted_points(points)
    return {
        "schema_version": EXPORT_PACKAGE_SCHEMA_VERSION,
        "synthetic_label": SYNTHETIC_LABEL,
        "human_review_required": HUMAN_REVIEW_NOTE,
        "publication_classification": metadata.get(
            "publication_classification", "Needs review"
        ),
        "curve_metadata": build_curve_metadata(metadata, sorted_points),
        "source_metadata": build_source_metadata(metadata),
        "calibration_metadata": build_calibration_metadata(metadata),
        "assumptions": build_assumptions(metadata),
        "method": build_method_metadata(metadata),
        "fit_model": build_fit_model_metadata(metadata, sorted_points),
        "validation_status": build_validation_status(metadata, sorted_points),
        "review_status": build_review_status(metadata),
        "downstream_use_warnings": list(DOWNSTREAM_USE_WARNINGS),
        "artifacts": dict(artifacts or {}),
    }


def build_curve_metadata(
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> dict[str, Any]:
    """Summarize the exported curve and engineering-unit range."""

    first = points[0]
    last = points[-1]
    y_values = [point.y for point in points]
    return {
        "part_number": metadata.get("part_number", ""),
        "manufacturer": metadata.get("manufacturer", ""),
        "curve_name": metadata.get("curve_name", ""),
        "x_axis": dict(metadata.get("x_axis", {})),
        "y_axis": dict(metadata.get("y_axis", {})),
        "point_count": len(points),
        "x_range": {
            "min": first.x,
            "max": last.x,
            "unit": metadata.get("x_axis", {}).get("unit", ""),
        },
        "y_range": {
            "min": min(y_values),
            "max": max(y_values),
            "unit": metadata.get("y_axis", {}).get("unit", ""),
        },
        "engineering_note": metadata.get("engineering_note", ""),
    }


def build_source_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Normalize source traceability fields for export."""

    return {
        "source_category": metadata.get("source_category", "synthetic"),
        "source_type": metadata.get("source_type", "datasheet_plot_image"),
        "source_name": metadata.get("datasheet_source", ""),
        "source_page": metadata.get("source_page", ""),
        "source_section": metadata.get("source_section", ""),
        "source_uri": metadata.get("source_uri", ""),
        "manufacturer": metadata.get("manufacturer", ""),
        "crop_region_px": dict(metadata.get("crop_region_px", {})),
        "source_note": (
            "Synthetic or public source only. No proprietary source details are "
            "included in this package."
        ),
    }


def build_calibration_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Normalize axis calibration details for package review."""

    calibration = dict(metadata.get("axis_calibration", {}))
    x_axis = dict(metadata.get("x_axis", {}))
    y_axis = dict(metadata.get("y_axis", {}))
    return {
        "x_axis": {
            "label": x_axis.get("label", ""),
            "unit": x_axis.get("unit", ""),
            "scale": x_axis.get("scale", "linear"),
            "pixel_low": calibration.get("x_pixel_low"),
            "pixel_high": calibration.get("x_pixel_high"),
            "value_low": calibration.get("x_value_low"),
            "value_high": calibration.get("x_value_high"),
        },
        "y_axis": {
            "label": y_axis.get("label", ""),
            "unit": y_axis.get("unit", ""),
            "scale": y_axis.get("scale", "linear"),
            "pixel_low": calibration.get("y_pixel_low"),
            "pixel_high": calibration.get("y_pixel_high"),
            "value_low": calibration.get("y_value_low"),
            "value_high": calibration.get("y_value_high"),
        },
        "calibration_review_status": metadata.get("calibration_review_status", "draft"),
        "calibration_note": (
            "Calibration values must be checked against the source plot before "
            "the exported curve is used downstream."
        ),
    }


def build_assumptions(metadata: dict[str, Any]) -> list[str]:
    """Return explicit assumptions, falling back to safe demo defaults."""

    assumptions = metadata.get("assumptions")
    if assumptions is None:
        return list(DEFAULT_ASSUMPTIONS)
    if not isinstance(assumptions, list) or not all(
        isinstance(item, str) for item in assumptions
    ):
        raise ValueError("metadata['assumptions'] must be a list of strings.")
    return list(assumptions)


def build_method_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Describe the extraction and package-generation method."""

    return {
        "digitization_method": metadata.get("digitization_method", ""),
        "operator_workflow": [
            "select source plot",
            "calibrate x and y axes",
            "pick curve points manually",
            "generate overlay for review",
            "export raw points, metadata, lookup functions, and report",
        ],
        "package_generator": "LED Datasheet Curve Studio deterministic exporter",
        "ai_boundary": (
            "AI-assisted output is decision support only; the exporter does not "
            "approve engineering data."
        ),
    }


def build_fit_model_metadata(
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> dict[str, Any]:
    """Describe the fitted lookup model without implying validation approval."""

    return {
        "model_name": metadata.get("fit_model", "not_fit"),
        "model_family": "shape_preserving_piecewise_cubic_interpolation",
        "segment_count": max(0, len(points) - 1),
        "fit_domain": {
            "x_min": points[0].x,
            "x_max": points[-1].x,
            "x_unit": metadata.get("x_axis", {}).get("unit", ""),
        },
        "out_of_range_behavior": (
            "Endpoint clamping in generated lookup functions; not approved for "
            "engineering extrapolation."
        ),
        "raw_points_exported": True,
    }


def build_validation_status(
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> dict[str, Any]:
    """Create deterministic validation prechecks for review packages."""

    point_count_ok = len(points) >= 2
    unique_x_ok = len({round(point.x, 12) for point in points}) == len(points)
    monotonic_x_ok = all(left.x < right.x for left, right in zip(points, points[1:]))
    source_pixels_ok = all(
        point.source_pixel_x is not None and point.source_pixel_y is not None
        for point in points
    )
    precheck_ok = point_count_ok and unique_x_ok and monotonic_x_ok and source_pixels_ok
    status = metadata.get("validation_status")
    if status is None:
        status = (
            VALIDATION_STATUS_PENDING_REVIEW
            if precheck_ok
            else "failed_export_precheck"
        )

    return {
        "status": status,
        "summary": (
            "Deterministic export prechecks completed; manual overlay and "
            "qualified engineering review remain required."
        ),
        "checks": [
            _check("point_count_at_least_two", point_count_ok),
            _check("unique_x_values", unique_x_ok),
            _check("strictly_increasing_x", monotonic_x_ok),
            _check("source_pixels_available", source_pixels_ok),
            {
                "name": "manual_overlay_review",
                "status": "pending_engineer_review",
                "detail": "Overlay image must be reviewed against the source plot.",
            },
        ],
    }


def build_review_status(metadata: dict[str, Any]) -> dict[str, Any]:
    """Normalize review state without implying approval."""

    return {
        "status": metadata.get("review_status", "draft_extraction"),
        "reviewer": metadata.get("reviewer", "not_assigned"),
        "reviewed_at_utc": metadata.get("reviewed_at_utc", "not_reviewed"),
        "reviewer_notes": metadata.get("reviewer_notes", ""),
        "requires_qualified_engineer_review": True,
    }


def write_markdown_report(
    path: Path,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
    overlay_path: str,
    csv_path: str,
    json_path: str,
    python_path: str,
    matlab_path: str,
    source_metadata_path: str = "",
    calibration_metadata_path: str = "",
) -> None:
    """Write the reviewable Markdown extraction report."""

    artifacts = {
        "csv_points": csv_path,
        "json_metadata": json_path,
        "python_lookup": python_path,
        "matlab_lookup": matlab_path,
        "overlay_png": overlay_path,
        "markdown_report": "this file",
    }
    if source_metadata_path:
        artifacts["source_metadata_json"] = source_metadata_path
    if calibration_metadata_path:
        artifacts["calibration_metadata_json"] = calibration_metadata_path

    context = build_report_context(metadata, points, artifacts)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_markdown_report(context), encoding="utf-8")


def format_markdown_report(context: dict[str, Any]) -> str:
    """Render a public-safe report from a structured report context."""

    curve = context["curve_metadata"]
    source = context["source_metadata"]
    calibration = context["calibration_metadata"]
    method = context["method"]
    fit_model = context["fit_model"]
    validation = context["validation_status"]
    review = context["review_status"]
    artifacts = context["artifacts"]
    x_axis = curve["x_axis"]
    y_axis = curve["y_axis"]

    return f"""# LED Datasheet Curve Export Package

{context["synthetic_label"]}

> {context["human_review_required"]}

## Problem

LED datasheet-style plots often contain useful voltage, current, temperature, and flux behavior in image form. Engineers need structured, traceable curve data for WCCA preparation, feasibility screening, simulation, and design-review discussion.

## Engineering Context

This package demonstrates a synthetic automotive-lighting data-prep workflow. It uses synthetic LED identifiers and synthetic plot points only. It does not include proprietary datasheets, customer programs, supplier records, internal requirements, schematics, BOM data, harness data, cost data, validation results, ticket numbers, repository names, file paths, or internal-document details.

## Workflow

1. Load synthetic curve points or a public/synthetic datasheet-style source record.
2. Record plot-region and source metadata for review.
3. Calibrate the x and y axes from known reference points.
4. Digitize curve points by manual picking first.
5. Fit a shape-preserving interpolation model for lookup generation.
6. Export raw points, metadata, lookup functions, overlay, and this report for review.
7. Require qualified engineering review before downstream use.

## Inputs

- Curve name: `{curve["curve_name"]}`
- Source: `{source["source_name"]}`
- Source page: `{source["source_page"]}`
- Source section: `{source["source_section"]}`
- X axis: `{x_axis.get("label", "")}` `{x_axis.get("unit", "")}`
- Y axis: `{y_axis.get("label", "")}` `{y_axis.get("unit", "")}`
- Digitization method: `{method["digitization_method"]}`
- Digitized points: `{curve["point_count"]}`

## Outputs

{_format_artifact_list(artifacts)}

## Screenshots Or Screenshot Placeholders

- Overlay verification image: `{artifacts.get("overlay_png", "")}`
- Streamlit workflow placeholder: `captures/streamlit_workflow_mock.md`
- Future capture: export package review screen after Streamlit/browser verification

## Sanitized Sample Data

The sample extraction uses `{curve["part_number"]}` from `{curve["manufacturer"]}`. These are synthetic demonstration labels, not real device or supplier identifiers. The extracted x range is `{curve["x_range"]["min"]:.3f}` to `{curve["x_range"]["max"]:.3f}` {curve["x_range"]["unit"]}; the extracted y range is `{curve["y_range"]["min"]:.1f}` to `{curve["y_range"]["max"]:.1f}` {curve["y_range"]["unit"]}.

## Source Metadata

- Source category: `{source["source_category"]}`
- Source type: `{source["source_type"]}`
- Source name: `{source["source_name"]}`
- Source page: `{source["source_page"]}`
- Source section: `{source["source_section"]}`
- Crop region px: `{source["crop_region_px"]}`
- Source note: {source["source_note"]}

## Calibration Metadata

- X axis calibration: `{calibration["x_axis"]}`
- Y axis calibration: `{calibration["y_axis"]}`
- Calibration review status: `{calibration["calibration_review_status"]}`
- Calibration note: {calibration["calibration_note"]}

## Assumptions

{_format_bullets(context["assumptions"])}

## Method

- Digitization method: `{method["digitization_method"]}`
- Package generator: `{method["package_generator"]}`
- AI boundary: {method["ai_boundary"]}

## Fit Model

- Model name: `{fit_model["model_name"]}`
- Model family: `{fit_model["model_family"]}`
- Segment count: `{fit_model["segment_count"]}`
- Fit domain: `{fit_model["fit_domain"]}`
- Out-of-range behavior: {fit_model["out_of_range_behavior"]}
- Raw points exported: `{fit_model["raw_points_exported"]}`

## Validation Status

- Status: `{validation["status"]}`
- Summary: {validation["summary"]}
- Checks: `{validation["checks"]}`

## Review Status

- Status: `{review["status"]}`
- Reviewer: `{review["reviewer"]}`
- Reviewed at UTC: `{review["reviewed_at_utc"]}`
- Requires qualified engineer review: `{review["requires_qualified_engineer_review"]}`

## Downstream Use Warnings

{_format_bullets(context["downstream_use_warnings"])}

## Human Review Controls

- Manual axis calibration is required before export.
- Curve points remain draft until a qualified reviewer checks them.
- Overlay review is required before use in WCCA or feasibility inputs.
- Source page, crop region, calibration metadata, method, fit model, validation status, and review status are preserved.
- The reviewer must confirm that plot data is reference-only and not a guaranteed device limit.
- The tool does not approve LED design values.

## Codex Contribution

Codex scaffolded the deterministic export package, report builder, lookup artifacts, synthetic sample package, and focused tests.

## Jose Contribution

Jose defines the LED engineering data-prep use case, WCCA and feasibility workflow boundary, required review controls, acceptable public/synthetic source boundary, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured data extraction workflow
- Metadata modeling for engineering traceability
- Deterministic transformation from source-pixel records to engineering units
- Curve-fit generation from review-controlled samples
- Human-in-the-loop review gates
- Public-safe artifact generation

## Engineering Skills Demonstrated

- LED forward-voltage and current curve interpretation
- Datasheet plot traceability
- WCCA input preparation
- Simulation lookup-table preparation
- Engineering review governance
- Reviewable export-package design

## Risks And Mitigations

- Risk: Digitized plot points could be mistaken for guaranteed limits. Mitigation: every export states that plot data is reference-only and requires engineering review.
- Risk: Calibration errors could distort the curve. Mitigation: manual axis calibration, overlay review, source-pixel export, and reviewer status are required.
- Risk: A curve fit could oversmooth engineering behavior. Mitigation: raw points, fit metadata, validation status, and PCHIP coefficients are exported for review.
- Risk: Lookup functions could be used as unreviewed downstream inputs. Mitigation: report and JSON metadata warn that WCCA, feasibility, thermal, optical, and design-review use requires qualified engineering review.
- Risk: Public output could reveal controlled data. Mitigation: included samples are synthetic and public use requires sanitized/public source review.

## Completed Work

- Synthetic source metadata, crop metadata, calibration metadata, assumptions, method, fit model, validation status, and review status are exported.
- Raw source-pixel points are preserved alongside engineering-unit values.
- Python and MATLAB lookup artifacts are generated from draft PCHIP coefficients.
- Overlay image and Markdown report artifacts are generated for review.
- Downstream-use warnings and human-review controls are visible in the package.

## Next Improvements

- Add a reviewed-status gate for downstream WCCA and feasibility adapters.
- Add browser-verified image click capture for calibration and curve picking.
- Add optional assisted extraction after manual-review controls are stable.
- Integrate the full curve-fit validation report into this generated package and the Streamlit review workflow.
- Add multi-curve export packaging from one source plot.
- Replace mock captures with reviewed screenshots.

## Proof Gaps

- The current generated sample is synthetic and does not prove extraction quality on a real public datasheet.
- Validation status is an export precheck in this generated report; qualified engineering review is still required.
- Interactive Streamlit image click/crop behavior is pending browser verification and still needs a browser component or custom canvas package.
- Optional PDF rendering and assisted extraction require runtime dependencies from `requirements.txt`.
- A qualified engineering review signoff has not been completed.

## Publication Classification

{context["publication_classification"]}

## Safe To Publish Status

Needs review. The code and sample data are synthetic and sanitized, but the tool behavior, screenshots, and public framing still require qualified engineering review before publication.
"""


def _sorted_points(points: Sequence[EngineeringPoint]) -> list[EngineeringPoint]:
    sorted_points = sorted(points, key=lambda point: point.x)
    if not sorted_points:
        raise ValueError("At least one point is required for an export report.")
    return sorted_points


def _check(name: str, passed: bool) -> dict[str, str]:
    return {
        "name": name,
        "status": "pass" if passed else "fail",
        "detail": "deterministic export precheck",
    }


def _format_artifact_list(artifacts: dict[str, str]) -> str:
    labels = {
        "csv_points": "CSV points",
        "json_metadata": "JSON metadata",
        "source_metadata_json": "Source metadata JSON",
        "calibration_metadata_json": "Calibration metadata JSON",
        "python_lookup": "Python lookup function",
        "matlab_lookup": "MATLAB lookup function",
        "overlay_png": "Overlay verification image",
        "markdown_report": "Markdown extraction report",
    }
    return "\n".join(
        f"- {labels.get(key, key)}: `{value}`"
        for key, value in artifacts.items()
        if value
    )


def _format_bullets(items: Sequence[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
