"""Draft assisted extraction helpers.

Assisted extraction is optional and produces draft candidates only. The output
must still pass manual calibration, overlay review, and qualified engineering
review before any downstream WCCA, simulation, or feasibility use.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .calibration import CurveCalibration
from .extraction_manual import ExtractedCurvePoint
from .image_tools import CandidatePixel, PlotRegion


ASSISTED_DRAFT_REVIEW_STATUS = "draft_assisted_extraction"
ASSISTED_DRAFT_METHOD = "draft_assisted_candidate_grouping_v1"
ASSISTED_REVIEW_NOTE = (
    "Draft assisted extraction candidate. Manual calibration and overlay review "
    "are required before downstream use."
)


@dataclass(frozen=True)
class AssistedExtractionSettings:
    """Deterministic settings for grouping draft candidate pixels."""

    method: str = ASSISTED_DRAFT_METHOD
    x_bin_size_px: float = 24.0
    min_confidence: float = 0.10

    def __post_init__(self) -> None:
        if "draft" not in self.method:
            raise ValueError("Assisted extraction method must be marked draft.")
        if self.x_bin_size_px <= 0:
            raise ValueError("x_bin_size_px must be positive.")
        if not 0.0 <= self.min_confidence <= 1.0:
            raise ValueError("min_confidence must be between 0.0 and 1.0.")


def maybe_extract_assisted_points(
    *,
    enabled: bool,
    candidate_pixels: Iterable[CandidatePixel],
    calibration: CurveCalibration,
    plot_region: PlotRegion | None = None,
    settings: AssistedExtractionSettings | None = None,
) -> list[ExtractedCurvePoint]:
    """Return draft assisted candidates only when the optional path is enabled."""

    if not enabled:
        return []
    return draft_assisted_points_from_candidate_pixels(
        candidate_pixels=candidate_pixels,
        calibration=calibration,
        plot_region=plot_region,
        settings=settings or AssistedExtractionSettings(),
    )


def draft_assisted_points_from_candidate_pixels(
    *,
    candidate_pixels: Iterable[CandidatePixel],
    calibration: CurveCalibration,
    plot_region: PlotRegion | None = None,
    settings: AssistedExtractionSettings | None = None,
) -> list[ExtractedCurvePoint]:
    """Group candidate pixels into draft extraction points.

    This function does not run image recognition itself. Optional UI/runtime
    code can provide public or synthetic candidate pixels; the deterministic
    core only groups them and preserves source-pixel traceability.
    """

    if not isinstance(calibration, CurveCalibration):
        raise ValueError("Assisted extraction requires manual CurveCalibration.")
    settings = settings or AssistedExtractionSettings()
    grouped = _group_candidate_pixels(candidate_pixels, plot_region, settings)
    points: list[ExtractedCurvePoint] = []
    for index, pixels in enumerate(grouped, start=1):
        source_pixel_x = _weighted_average(
            [pixel.source_pixel_x for pixel in pixels],
            [pixel.signal_strength for pixel in pixels],
        )
        source_pixel_y = _weighted_average(
            [pixel.source_pixel_y for pixel in pixels],
            [pixel.signal_strength for pixel in pixels],
        )
        confidence = sum(pixel.signal_strength for pixel in pixels) / len(pixels)
        engineering_point = calibration.pixel_to_engineering(
            point_id=f"A{index:02d}",
            source_pixel_x=source_pixel_x,
            source_pixel_y=source_pixel_y,
            review_status=ASSISTED_DRAFT_REVIEW_STATUS,
            notes=ASSISTED_REVIEW_NOTE,
        )
        points.append(
            ExtractedCurvePoint(
                point_id=engineering_point.point_id,
                source_pixel_x=engineering_point.source_pixel_x,
                source_pixel_y=engineering_point.source_pixel_y,
                x=engineering_point.x,
                y=engineering_point.y,
                method=settings.method,
                confidence=confidence,
                review_status=ASSISTED_DRAFT_REVIEW_STATUS,
                notes=engineering_point.notes,
            )
        )
    if not points:
        raise ValueError("No assisted candidate pixels passed the draft filters.")
    return points


def assisted_extraction_boundary() -> dict[str, str | bool]:
    """Return report-ready wording for the assisted extraction boundary."""

    return {
        "optional": True,
        "status": "draft",
        "manual_calibration_required": True,
        "overlay_review_required": True,
        "qualified_engineer_review_required": True,
        "downstream_use": "blocked_until_manual_overlay_and_engineer_review",
    }


def _group_candidate_pixels(
    candidate_pixels: Iterable[CandidatePixel],
    plot_region: PlotRegion | None,
    settings: AssistedExtractionSettings,
) -> list[list[CandidatePixel]]:
    groups: dict[int, list[CandidatePixel]] = {}
    for pixel in candidate_pixels:
        if not isinstance(pixel, CandidatePixel):
            raise ValueError("Assisted extraction expects CandidatePixel records.")
        if pixel.signal_strength < settings.min_confidence:
            continue
        if plot_region is not None and not plot_region.contains(
            pixel.source_pixel_x, pixel.source_pixel_y
        ):
            continue
        bin_index = int(pixel.source_pixel_x // settings.x_bin_size_px)
        groups.setdefault(bin_index, []).append(pixel)
    return [groups[key] for key in sorted(groups)]


def _weighted_average(values: list[float], weights: list[float]) -> float:
    weight_total = sum(weights)
    if weight_total <= 0:
        raise ValueError("Candidate pixel weights must be positive.")
    return sum(value * weight for value, weight in zip(values, weights)) / weight_total
