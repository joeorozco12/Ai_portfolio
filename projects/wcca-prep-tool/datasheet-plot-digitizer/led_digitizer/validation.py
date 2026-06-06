"""Curve-fit validation helpers for digitized LED plot data."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Callable, Literal, Sequence

from .calibration import EngineeringPoint
from .curve_fit import (
    OutOfRangePolicy,
    build_lookup_domain,
    build_pchip_segments,
    describe_out_of_range_policy,
    evaluate_pchip,
    linear_interpolate,
    sort_unique_points,
)

MonotonicDirection = Literal[
    "nondecreasing",
    "nonincreasing",
    "strictly_increasing",
    "strictly_decreasing",
]

PCHIP_MODEL = "pchip_shape_preserving_interpolation"
LINEAR_MODEL = "linear_interpolation"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts "
    "only. A qualified engineer owns final review and approval."
)


@dataclass(frozen=True)
class ResidualRecord:
    """Residual for one raw digitized point compared with the fitted lookup."""

    point_id: str
    x: float
    observed_y: float
    fitted_y: float
    residual: float
    abs_residual: float
    abs_percent_error: float | None

    def to_dict(self) -> dict[str, float | str | None]:
        return {
            "point_id": self.point_id,
            "x": self.x,
            "observed_y": self.observed_y,
            "fitted_y": self.fitted_y,
            "residual": self.residual,
            "abs_residual": self.abs_residual,
            "abs_percent_error": self.abs_percent_error,
        }


@dataclass(frozen=True)
class MonotonicityCheck:
    """Result of checking a numeric sequence for an expected direction."""

    direction: MonotonicDirection
    passed: bool
    violation_count: int
    first_violation_index: int | None
    tolerance: float = 0.0

    def to_dict(self) -> dict[str, float | int | bool | str | None]:
        return {
            "direction": self.direction,
            "passed": self.passed,
            "violation_count": self.violation_count,
            "first_violation_index": self.first_violation_index,
            "tolerance": self.tolerance,
        }


@dataclass(frozen=True)
class FitValidationReport:
    """Serializable validation output suitable for future reports and exports."""

    fit_model: str
    point_count: int
    x_min: float
    x_max: float
    out_of_range_policy: OutOfRangePolicy
    out_of_range_behavior: str
    residuals: list[ResidualRecord]
    max_abs_residual: float
    mean_abs_residual: float
    rms_residual: float
    max_abs_percent_error: float | None
    mean_abs_percent_error: float | None
    monotonic_x_check: MonotonicityCheck
    monotonic_y_check: MonotonicityCheck | None
    review_status_counts: dict[str, int]
    residual_abs_tolerance: float | None
    residual_percent_tolerance: float | None
    passed: bool
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "human_review_required": HUMAN_REVIEW_NOTE,
            "fit_model": self.fit_model,
            "point_count": self.point_count,
            "lookup_domain": {
                "x_min": self.x_min,
                "x_max": self.x_max,
                "out_of_range_policy": self.out_of_range_policy,
                "out_of_range_behavior": self.out_of_range_behavior,
            },
            "residual_metrics": {
                "max_abs_residual": self.max_abs_residual,
                "mean_abs_residual": self.mean_abs_residual,
                "rms_residual": self.rms_residual,
                "max_abs_percent_error": self.max_abs_percent_error,
                "mean_abs_percent_error": self.mean_abs_percent_error,
                "residual_abs_tolerance": self.residual_abs_tolerance,
                "residual_percent_tolerance": self.residual_percent_tolerance,
            },
            "monotonicity": {
                "x": self.monotonic_x_check.to_dict(),
                "y": (
                    self.monotonic_y_check.to_dict()
                    if self.monotonic_y_check is not None
                    else None
                ),
            },
            "review_status_counts": dict(self.review_status_counts),
            "residuals": [record.to_dict() for record in self.residuals],
            "passed": self.passed,
            "warnings": list(self.warnings),
        }

    def to_markdown_section(self) -> str:
        status = "passed" if self.passed else "needs review"
        x_status = "passed" if self.monotonic_x_check.passed else "failed"
        y_check = (
            f"{self.monotonic_y_check.direction}: "
            f"{'passed' if self.monotonic_y_check.passed else 'failed'}"
            if self.monotonic_y_check is not None
            else "not evaluated"
        )
        max_percent = _format_optional_number(self.max_abs_percent_error)
        mean_percent = _format_optional_number(self.mean_abs_percent_error)
        warning_lines = (
            "\n".join(f"- {warning}" for warning in self.warnings)
            if self.warnings
            else "- None"
        )
        return f"""## Curve Fit Validation

> {HUMAN_REVIEW_NOTE}

- Fit model: `{self.fit_model}`
- Point count: `{self.point_count}`
- X domain: `{self.x_min:.6g}` to `{self.x_max:.6g}`
- Out-of-range lookup behavior: {self.out_of_range_behavior}
- Max absolute residual: `{self.max_abs_residual:.6g}`
- Mean absolute residual: `{self.mean_abs_residual:.6g}`
- RMS residual: `{self.rms_residual:.6g}`
- Max absolute percent error: `{max_percent}`
- Mean absolute percent error: `{mean_percent}`
- X monotonicity: `{self.monotonic_x_check.direction}: {x_status}`
- Y monotonicity: `{y_check}`
- Validation status: `{status}`

Warnings:

{warning_lines}
"""


def validate_curve_fit(
    points: Sequence[EngineeringPoint],
    fit_model: str = PCHIP_MODEL,
    expected_y_monotonic: MonotonicDirection | None = None,
    residual_abs_tolerance: float | None = None,
    residual_percent_tolerance: float | None = None,
    out_of_range: OutOfRangePolicy = "raise",
) -> FitValidationReport:
    """Validate a fitted curve against the raw digitized points."""

    sorted_points = sort_unique_points(points)
    _validate_tolerance(residual_abs_tolerance, "residual_abs_tolerance")
    _validate_tolerance(residual_percent_tolerance, "residual_percent_tolerance")

    evaluator = _build_evaluator(sorted_points, fit_model, out_of_range)
    residuals = calculate_residuals(sorted_points, evaluator)
    domain = build_lookup_domain(sorted_points, out_of_range)

    abs_residuals = [record.abs_residual for record in residuals]
    percent_errors = [
        record.abs_percent_error
        for record in residuals
        if record.abs_percent_error is not None
    ]

    max_abs_residual = max(abs_residuals)
    mean_abs_residual = sum(abs_residuals) / len(abs_residuals)
    rms_residual = sqrt(
        sum(record.residual * record.residual for record in residuals)
        / len(residuals)
    )
    max_abs_percent_error = max(percent_errors) if percent_errors else None
    mean_abs_percent_error = (
        sum(percent_errors) / len(percent_errors) if percent_errors else None
    )

    monotonic_x_check = check_monotonicity(
        [point.x for point in sorted_points],
        "strictly_increasing",
    )
    monotonic_y_check = (
        check_monotonicity([point.y for point in sorted_points], expected_y_monotonic)
        if expected_y_monotonic is not None
        else None
    )
    review_status_counts = _review_status_counts(sorted_points)
    warnings = _build_warnings(
        max_abs_residual=max_abs_residual,
        max_abs_percent_error=max_abs_percent_error,
        residual_abs_tolerance=residual_abs_tolerance,
        residual_percent_tolerance=residual_percent_tolerance,
        monotonic_x_check=monotonic_x_check,
        monotonic_y_check=monotonic_y_check,
    )

    return FitValidationReport(
        fit_model=fit_model,
        point_count=len(sorted_points),
        x_min=float(domain.x_min),
        x_max=float(domain.x_max),
        out_of_range_policy=domain.out_of_range_policy,
        out_of_range_behavior=describe_out_of_range_policy(domain.out_of_range_policy),
        residuals=residuals,
        max_abs_residual=max_abs_residual,
        mean_abs_residual=mean_abs_residual,
        rms_residual=rms_residual,
        max_abs_percent_error=max_abs_percent_error,
        mean_abs_percent_error=mean_abs_percent_error,
        monotonic_x_check=monotonic_x_check,
        monotonic_y_check=monotonic_y_check,
        review_status_counts=review_status_counts,
        residual_abs_tolerance=residual_abs_tolerance,
        residual_percent_tolerance=residual_percent_tolerance,
        passed=not warnings,
        warnings=warnings,
    )


def calculate_residuals(
    points: Sequence[EngineeringPoint],
    evaluator: Callable[[float], float],
) -> list[ResidualRecord]:
    """Calculate fitted-minus-observed residuals for raw digitized points."""

    sorted_points = sort_unique_points(points)
    residuals: list[ResidualRecord] = []
    for point in sorted_points:
        _require_finite(point.x, f"x for point {point.point_id}")
        _require_finite(point.y, f"y for point {point.point_id}")
        fitted_y = float(evaluator(point.x))
        _require_finite(fitted_y, f"fitted y for point {point.point_id}")
        residual = fitted_y - point.y
        abs_residual = abs(residual)
        abs_percent_error = (
            None if point.y == 0.0 else abs_residual / abs(point.y) * 100.0
        )
        residuals.append(
            ResidualRecord(
                point_id=point.point_id,
                x=point.x,
                observed_y=point.y,
                fitted_y=fitted_y,
                residual=residual,
                abs_residual=abs_residual,
                abs_percent_error=abs_percent_error,
            )
        )
    return residuals


def check_monotonicity(
    values: Sequence[float],
    direction: MonotonicDirection,
    tolerance: float = 0.0,
) -> MonotonicityCheck:
    """Check whether values follow the expected monotonic direction."""

    _validate_monotonic_direction(direction)
    _validate_tolerance(tolerance, "tolerance")
    if len(values) < 2:
        raise ValueError("At least two values are required for monotonicity checks.")

    violation_count = 0
    first_violation_index: int | None = None
    for index, (left, right) in enumerate(zip(values, values[1:]), start=1):
        left_value = float(left)
        right_value = float(right)
        _require_finite(left_value, f"monotonic value {index - 1}")
        _require_finite(right_value, f"monotonic value {index}")
        if _is_monotonic_violation(left_value, right_value, direction, tolerance):
            violation_count += 1
            if first_violation_index is None:
                first_violation_index = index

    return MonotonicityCheck(
        direction=direction,
        passed=violation_count == 0,
        violation_count=violation_count,
        first_violation_index=first_violation_index,
        tolerance=tolerance,
    )


def _build_evaluator(
    points: Sequence[EngineeringPoint],
    fit_model: str,
    out_of_range: OutOfRangePolicy,
) -> Callable[[float], float]:
    if fit_model == PCHIP_MODEL:
        segments = build_pchip_segments(points)
        return lambda x_value: evaluate_pchip(
            segments,
            x_value,
            out_of_range=out_of_range,
        )
    if fit_model == LINEAR_MODEL:
        return lambda x_value: linear_interpolate(
            points,
            x_value,
            out_of_range=out_of_range,
        )
    raise ValueError(
        "Fit model must be 'pchip_shape_preserving_interpolation' "
        "or 'linear_interpolation'."
    )


def _build_warnings(
    max_abs_residual: float,
    max_abs_percent_error: float | None,
    residual_abs_tolerance: float | None,
    residual_percent_tolerance: float | None,
    monotonic_x_check: MonotonicityCheck,
    monotonic_y_check: MonotonicityCheck | None,
) -> list[str]:
    warnings: list[str] = []
    if residual_abs_tolerance is not None and max_abs_residual > residual_abs_tolerance:
        warnings.append(
            "Maximum absolute residual exceeds the configured tolerance."
        )
    if (
        residual_percent_tolerance is not None
        and max_abs_percent_error is not None
        and max_abs_percent_error > residual_percent_tolerance
    ):
        warnings.append(
            "Maximum absolute percent error exceeds the configured tolerance."
        )
    if not monotonic_x_check.passed:
        warnings.append("X values are not strictly increasing.")
    if monotonic_y_check is not None and not monotonic_y_check.passed:
        warnings.append(
            f"Y values do not satisfy expected {monotonic_y_check.direction} trend."
        )
    return warnings


def _is_monotonic_violation(
    left: float,
    right: float,
    direction: MonotonicDirection,
    tolerance: float,
) -> bool:
    if direction == "nondecreasing":
        return right < left - tolerance
    if direction == "nonincreasing":
        return right > left + tolerance
    if direction == "strictly_increasing":
        return right <= left + tolerance
    if direction == "strictly_decreasing":
        return right >= left - tolerance
    raise ValueError("Unsupported monotonic direction.")


def _review_status_counts(points: Sequence[EngineeringPoint]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for point in points:
        counts[point.review_status] = counts.get(point.review_status, 0) + 1
    return counts


def _validate_tolerance(value: float | None, name: str) -> None:
    if value is None:
        return
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


def _validate_monotonic_direction(direction: str) -> None:
    if direction not in {
        "nondecreasing",
        "nonincreasing",
        "strictly_increasing",
        "strictly_decreasing",
    }:
        raise ValueError("Monotonic direction is not recognized.")


def _require_finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite.")


def _format_optional_number(value: float | None) -> str:
    return "not_applicable" if value is None else f"{value:.6g}"
