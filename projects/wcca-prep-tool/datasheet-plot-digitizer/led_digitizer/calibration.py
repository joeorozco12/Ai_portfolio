"""Pixel-to-engineering calibration helpers.

The math is intentionally small and reviewable. The Streamlit app can collect
calibration clicks later; the deterministic core only needs pixel/value pairs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log10


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
        if self.pixel_low == self.pixel_high:
            raise ValueError("Calibration pixels must be different.")
        if self.value_low == self.value_high:
            raise ValueError("Calibration values must be different.")
        if self.scale not in {"linear", "log"}:
            raise ValueError("Axis scale must be 'linear' or 'log'.")
        if self.scale == "log" and (self.value_low <= 0 or self.value_high <= 0):
            raise ValueError("Log-scale calibration values must be positive.")

    def pixel_to_value(self, pixel: float) -> float:
        """Convert a pixel coordinate into the calibrated engineering value."""

        fraction = (pixel - self.pixel_low) / (self.pixel_high - self.pixel_low)
        if self.scale == "linear":
            return self.value_low + fraction * (self.value_high - self.value_low)

        log_low = log10(self.value_low)
        log_high = log10(self.value_high)
        return 10 ** (log_low + fraction * (log_high - log_low))

    def value_to_pixel(self, value: float) -> float:
        """Convert an engineering value back into a pixel coordinate."""

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


@dataclass(frozen=True)
class CurveCalibration:
    """Pair of calibrated axes used to transform plot points."""

    x_axis: AxisCalibration
    y_axis: AxisCalibration

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
