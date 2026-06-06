"""Pixel-to-engineering calibration helpers.

The math is intentionally small and reviewable. The Streamlit app can collect
calibration clicks later; the deterministic core only needs pixel/value pairs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log10, sqrt
from typing import Any, Iterable


SUPPORTED_AXIS_SCALES = {"linear", "log"}


@dataclass(frozen=True)
class AxisCalibration:
    """Maps one image axis from pixel coordinates to engineering units."""

    pixel_low: float
    pixel_high: float
    value_low: float
    value_high: float
    scale: str = "linear"
    label: str = ""
    unit: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "pixel_low",
            _finite_float(self.pixel_low, "pixel_low"),
        )
        object.__setattr__(
            self,
            "pixel_high",
            _finite_float(self.pixel_high, "pixel_high"),
        )
        object.__setattr__(
            self,
            "value_low",
            _finite_float(self.value_low, "value_low"),
        )
        object.__setattr__(
            self,
            "value_high",
            _finite_float(self.value_high, "value_high"),
        )
        if not isinstance(self.scale, str):
            raise ValueError("Axis scale must be 'linear' or 'log'.")
        object.__setattr__(self, "scale", self.scale.strip().lower())
        object.__setattr__(self, "label", str(self.label))
        object.__setattr__(self, "unit", str(self.unit))
        if self.pixel_low == self.pixel_high:
            raise ValueError("Calibration pixels must be different for an axis.")
        if self.value_low == self.value_high:
            raise ValueError("Calibration values must be different for an axis.")
        if self.scale not in SUPPORTED_AXIS_SCALES:
            raise ValueError("Axis scale must be 'linear' or 'log'.")
        if self.scale == "log" and (self.value_low <= 0 or self.value_high <= 0):
            raise ValueError("Log-scale calibration values must be positive.")

    @property
    def inverted_image_axis(self) -> bool:
        """Return true when the calibrated image coordinate decreases upward/left."""

        return self.pixel_high < self.pixel_low

    @property
    def value_increases_as_pixel_increases(self) -> bool:
        """Return true when larger pixel coordinates map to larger values."""

        return (self.value_high - self.value_low) / (
            self.pixel_high - self.pixel_low
        ) > 0

    def pixel_to_value(self, pixel: float) -> float:
        """Convert a pixel coordinate into the calibrated engineering value."""

        pixel = _finite_float(pixel, "pixel")
        fraction = (pixel - self.pixel_low) / (self.pixel_high - self.pixel_low)
        if self.scale == "linear":
            return self.value_low + fraction * (self.value_high - self.value_low)

        log_low = log10(self.value_low)
        log_high = log10(self.value_high)
        return 10 ** (log_low + fraction * (log_high - log_low))

    def value_to_pixel(self, value: float) -> float:
        """Convert an engineering value back into a pixel coordinate."""

        value = _finite_float(value, "value")
        if self.scale == "log":
            if value <= 0:
                raise ValueError("Log-scale values must be positive.")
            value_fraction = (log10(value) - log10(self.value_low)) / (
                log10(self.value_high) - log10(self.value_low)
            )
        else:
            value_fraction = (value - self.value_low) / (
                self.value_high - self.value_low
            )

        return self.pixel_low + value_fraction * (self.pixel_high - self.pixel_low)

    def calibration_residuals(
        self,
        check_points: Iterable["AxisCalibrationCheckPoint | dict[str, Any] | tuple[Any, ...]"],
    ) -> tuple["AxisCalibrationResidual", ...]:
        """Compare known check points against the calibrated transform."""

        residuals = []
        for index, check_point in enumerate(check_points, start=1):
            normalized = AxisCalibrationCheckPoint.from_value(check_point, index)
            actual_value = self.pixel_to_value(normalized.pixel)
            residuals.append(
                AxisCalibrationResidual(
                    point_id=normalized.point_id,
                    pixel=normalized.pixel,
                    expected_value=normalized.expected_value,
                    actual_value=actual_value,
                )
            )
        return tuple(residuals)

    def sanity_check(
        self,
        check_points: Iterable["AxisCalibrationCheckPoint | dict[str, Any] | tuple[Any, ...]"] | None = None,
        tolerance: float | None = None,
    ) -> "AxisCalibrationSanityCheck":
        """Return report-ready calibration metadata and residual statistics."""

        if tolerance is not None:
            tolerance = _finite_float(tolerance, "tolerance")
            if tolerance < 0:
                raise ValueError("Calibration tolerance must be non-negative.")
        if check_points is None:
            check_points = (
                AxisCalibrationCheckPoint("cal_low", self.pixel_low, self.value_low),
                AxisCalibrationCheckPoint("cal_high", self.pixel_high, self.value_high),
            )
        residuals = self.calibration_residuals(check_points)
        absolute_residuals = [residual.absolute_residual for residual in residuals]
        max_abs_residual = max(absolute_residuals, default=0.0)
        mean_abs_residual = (
            sum(absolute_residuals) / len(absolute_residuals)
            if absolute_residuals
            else 0.0
        )
        rms_residual = (
            sqrt(
                sum(residual.residual * residual.residual for residual in residuals)
                / len(residuals)
            )
            if residuals
            else 0.0
        )
        passes_tolerance = (
            None if tolerance is None else max_abs_residual <= tolerance
        )
        return AxisCalibrationSanityCheck(
            label=self.label,
            unit=self.unit,
            scale=self.scale,
            pixel_low=self.pixel_low,
            pixel_high=self.pixel_high,
            value_low=self.value_low,
            value_high=self.value_high,
            inverted_image_axis=self.inverted_image_axis,
            value_increases_as_pixel_increases=(
                self.value_increases_as_pixel_increases
            ),
            residuals=residuals,
            max_abs_residual=max_abs_residual,
            mean_abs_residual=mean_abs_residual,
            rms_residual=rms_residual,
            tolerance=tolerance,
            passes_tolerance=passes_tolerance,
        )


@dataclass(frozen=True)
class AxisCalibrationCheckPoint:
    """Known pixel/value pair used to sanity-check a calibrated axis."""

    point_id: str
    pixel: float
    expected_value: float

    def __post_init__(self) -> None:
        if not isinstance(self.point_id, str) or not self.point_id.strip():
            raise ValueError("Calibration check point_id must be a non-empty string.")
        object.__setattr__(self, "point_id", self.point_id.strip())
        object.__setattr__(self, "pixel", _finite_float(self.pixel, "pixel"))
        object.__setattr__(
            self,
            "expected_value",
            _finite_float(self.expected_value, "expected_value"),
        )

    @classmethod
    def from_value(
        cls,
        value: "AxisCalibrationCheckPoint | dict[str, Any] | tuple[Any, ...]",
        index: int,
    ) -> "AxisCalibrationCheckPoint":
        if isinstance(value, AxisCalibrationCheckPoint):
            return value
        if isinstance(value, dict):
            point_id = str(value.get("point_id", f"check_{index}"))
            return cls(
                point_id=point_id,
                pixel=value["pixel"],
                expected_value=value["expected_value"],
            )
        if isinstance(value, tuple):
            if len(value) == 2:
                pixel, expected_value = value
                point_id = f"check_{index}"
            elif len(value) == 3:
                point_id, pixel, expected_value = value
            else:
                raise ValueError(
                    "Calibration check tuples must be (pixel, expected_value) "
                    "or (point_id, pixel, expected_value)."
                )
            return cls(str(point_id), pixel, expected_value)
        raise ValueError(
            "Calibration check points must be AxisCalibrationCheckPoint, "
            "dict, or tuple values."
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "point_id": self.point_id,
            "pixel": self.pixel,
            "expected_value": self.expected_value,
        }


@dataclass(frozen=True)
class AxisCalibrationResidual:
    """Residual between a known value and the calibrated value at one pixel."""

    point_id: str
    pixel: float
    expected_value: float
    actual_value: float

    def __post_init__(self) -> None:
        if not isinstance(self.point_id, str) or not self.point_id.strip():
            raise ValueError("Calibration residual point_id must be non-empty.")
        object.__setattr__(self, "point_id", self.point_id.strip())
        object.__setattr__(self, "pixel", _finite_float(self.pixel, "pixel"))
        object.__setattr__(
            self,
            "expected_value",
            _finite_float(self.expected_value, "expected_value"),
        )
        object.__setattr__(
            self,
            "actual_value",
            _finite_float(self.actual_value, "actual_value"),
        )

    @property
    def residual(self) -> float:
        return self.actual_value - self.expected_value

    @property
    def absolute_residual(self) -> float:
        return abs(self.residual)

    @property
    def relative_residual_percent(self) -> float | None:
        if self.expected_value == 0:
            return None
        return 100.0 * self.residual / self.expected_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "point_id": self.point_id,
            "pixel": self.pixel,
            "expected_value": self.expected_value,
            "actual_value": self.actual_value,
            "residual": self.residual,
            "absolute_residual": self.absolute_residual,
            "relative_residual_percent": self.relative_residual_percent,
        }


@dataclass(frozen=True)
class AxisCalibrationSanityCheck:
    """Report-ready residual summary for one calibrated axis."""

    label: str
    unit: str
    scale: str
    pixel_low: float
    pixel_high: float
    value_low: float
    value_high: float
    inverted_image_axis: bool
    value_increases_as_pixel_increases: bool
    residuals: tuple[AxisCalibrationResidual, ...]
    max_abs_residual: float
    mean_abs_residual: float
    rms_residual: float
    tolerance: float | None = None
    passes_tolerance: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "unit": self.unit,
            "scale": self.scale,
            "pixel_low": self.pixel_low,
            "pixel_high": self.pixel_high,
            "value_low": self.value_low,
            "value_high": self.value_high,
            "inverted_image_axis": self.inverted_image_axis,
            "value_increases_as_pixel_increases": (
                self.value_increases_as_pixel_increases
            ),
            "residuals": [residual.to_dict() for residual in self.residuals],
            "max_abs_residual": self.max_abs_residual,
            "mean_abs_residual": self.mean_abs_residual,
            "rms_residual": self.rms_residual,
            "tolerance": self.tolerance,
            "passes_tolerance": self.passes_tolerance,
        }


@dataclass(frozen=True)
class EngineeringPoint:
    """A digitized point with both source-pixel and engineering coordinates."""

    point_id: str
    source_pixel_x: float
    source_pixel_y: float
    x: float
    y: float
    review_status: str = "draft_extraction"
    notes: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.point_id, str) or not self.point_id.strip():
            raise ValueError("Engineering point_id must be a non-empty string.")
        if not isinstance(self.review_status, str) or not self.review_status.strip():
            raise ValueError("Engineering point review_status must be non-empty.")
        object.__setattr__(self, "point_id", self.point_id.strip())
        object.__setattr__(
            self,
            "source_pixel_x",
            _finite_float(self.source_pixel_x, "source_pixel_x"),
        )
        object.__setattr__(
            self,
            "source_pixel_y",
            _finite_float(self.source_pixel_y, "source_pixel_y"),
        )
        object.__setattr__(self, "x", _finite_float(self.x, "x"))
        object.__setattr__(self, "y", _finite_float(self.y, "y"))
        object.__setattr__(self, "notes", str(self.notes))


@dataclass(frozen=True)
class CurveCalibration:
    """Pair of calibrated axes used to transform plot points."""

    x_axis: AxisCalibration
    y_axis: AxisCalibration

    def __post_init__(self) -> None:
        if not isinstance(self.x_axis, AxisCalibration):
            raise ValueError("Curve calibration x_axis must be an AxisCalibration.")
        if not isinstance(self.y_axis, AxisCalibration):
            raise ValueError("Curve calibration y_axis must be an AxisCalibration.")

    def pixel_to_engineering(
        self,
        point_id: str,
        source_pixel_x: float,
        source_pixel_y: float,
        review_status: str = "draft_extraction",
        notes: str = "",
    ) -> EngineeringPoint:
        return EngineeringPoint(
            point_id=point_id,
            source_pixel_x=source_pixel_x,
            source_pixel_y=source_pixel_y,
            x=self.x_axis.pixel_to_value(source_pixel_x),
            y=self.y_axis.pixel_to_value(source_pixel_y),
            review_status=review_status,
            notes=notes,
        )

    def sanity_check(
        self,
        x_check_points: Iterable["AxisCalibrationCheckPoint | dict[str, Any] | tuple[Any, ...]"] | None = None,
        y_check_points: Iterable["AxisCalibrationCheckPoint | dict[str, Any] | tuple[Any, ...]"] | None = None,
        tolerance: float | None = None,
    ) -> dict[str, Any]:
        """Return serializable x/y calibration residual summaries."""

        x_check = self.x_axis.sanity_check(x_check_points, tolerance)
        y_check = self.y_axis.sanity_check(y_check_points, tolerance)
        if tolerance is None:
            passes_tolerance = None
        else:
            passes_tolerance = bool(
                x_check.passes_tolerance and y_check.passes_tolerance
            )
        return {
            "x_axis": x_check.to_dict(),
            "y_axis": y_check.to_dict(),
            "passes_tolerance": passes_tolerance,
        }


def _finite_float(value: Any, field_name: str) -> float:
    try:
        converted = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a finite number.") from exc
    if not isfinite(converted):
        raise ValueError(f"{field_name} must be a finite number.")
    return converted
