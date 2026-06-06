"""Manual extraction helpers with explicit review boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .calibration import CurveCalibration, EngineeringPoint


DRAFT_REVIEW_STATUS = "draft_extraction"
MANUAL_METHOD = "manual_curve_pick"
REVIEWED_STATUSES = {"engineer_reviewed", "engineer_reviewed_demo"}


@dataclass(frozen=True)
class ManualPixelPick:
    """One manually selected pixel before calibration conversion."""

    point_id: str
    source_pixel_x: float
    source_pixel_y: float
    review_status: str = DRAFT_REVIEW_STATUS
    notes: str = ""

    def __post_init__(self) -> None:
        _require_text(self.point_id, "point_id")
        _require_text(self.review_status, "review_status")
        if self.source_pixel_x < 0 or self.source_pixel_y < 0:
            raise ValueError("Manual source pixels must be non-negative.")


@dataclass(frozen=True)
class ExtractedCurvePoint:
    """Calibrated curve point with traceable source-pixel metadata."""

    point_id: str
    source_pixel_x: float
    source_pixel_y: float
    x: float
    y: float
    method: str
    confidence: float
    review_status: str
    notes: str = ""

    def __post_init__(self) -> None:
        _require_text(self.point_id, "point_id")
        _require_text(self.method, "method")
        _require_text(self.review_status, "review_status")
        if self.source_pixel_x < 0 or self.source_pixel_y < 0:
            raise ValueError("Source pixels must be non-negative.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0.")

    def to_engineering_point(self) -> EngineeringPoint:
        return EngineeringPoint(
            point_id=self.point_id,
            source_pixel_x=self.source_pixel_x,
            source_pixel_y=self.source_pixel_y,
            x=self.x,
            y=self.y,
            review_status=self.review_status,
            notes=self.notes,
        )

    def to_dict(self) -> dict[str, float | str]:
        return {
            "point_id": self.point_id,
            "source_pixel_x": self.source_pixel_x,
            "source_pixel_y": self.source_pixel_y,
            "x": self.x,
            "y": self.y,
            "method": self.method,
            "confidence": self.confidence,
            "review_status": self.review_status,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ReviewControlStatus:
    """Downstream-use gate for manual or assisted extraction output."""

    manual_calibration_present: bool
    overlay_review_completed: bool
    qualified_engineer_review_completed: bool = False
    review_status: str = DRAFT_REVIEW_STATUS

    @property
    def downstream_use_allowed(self) -> bool:
        return (
            self.manual_calibration_present
            and self.overlay_review_completed
            and self.qualified_engineer_review_completed
            and self.review_status in REVIEWED_STATUSES
        )

    @property
    def missing_controls(self) -> list[str]:
        missing = []
        if not self.manual_calibration_present:
            missing.append("manual_axis_calibration")
        if not self.overlay_review_completed:
            missing.append("overlay_review")
        if not self.qualified_engineer_review_completed:
            missing.append("qualified_engineer_review")
        if self.review_status not in REVIEWED_STATUSES:
            missing.append("reviewed_status")
        return missing

    def to_dict(self) -> dict[str, bool | str | list[str]]:
        return {
            "manual_calibration_present": self.manual_calibration_present,
            "overlay_review_completed": self.overlay_review_completed,
            "qualified_engineer_review_completed": (
                self.qualified_engineer_review_completed
            ),
            "review_status": self.review_status,
            "downstream_use_allowed": self.downstream_use_allowed,
            "missing_controls": self.missing_controls,
        }


def convert_manual_picks(
    picks: Iterable[ManualPixelPick],
    calibration: CurveCalibration,
) -> list[ExtractedCurvePoint]:
    """Convert reviewed manual pixel picks through an explicit calibration."""

    _require_curve_calibration(calibration)
    converted = []
    for pick in picks:
        if not isinstance(pick, ManualPixelPick):
            raise ValueError("Manual extraction expects ManualPixelPick records.")
        point = calibration.pixel_to_engineering(
            point_id=pick.point_id,
            source_pixel_x=pick.source_pixel_x,
            source_pixel_y=pick.source_pixel_y,
            review_status=pick.review_status,
            notes=pick.notes,
        )
        converted.append(
            ExtractedCurvePoint(
                point_id=point.point_id,
                source_pixel_x=point.source_pixel_x,
                source_pixel_y=point.source_pixel_y,
                x=point.x,
                y=point.y,
                method=MANUAL_METHOD,
                confidence=1.0,
                review_status=point.review_status,
                notes=point.notes,
            )
        )
    if not converted:
        raise ValueError("At least one manual pick is required.")
    return converted


def build_review_control_status(
    *,
    manual_calibration_present: bool,
    overlay_review_completed: bool = False,
    qualified_engineer_review_completed: bool = False,
    review_status: str = DRAFT_REVIEW_STATUS,
) -> ReviewControlStatus:
    """Build the review gate that blocks unreviewed downstream use."""

    _require_text(review_status, "review_status")
    return ReviewControlStatus(
        manual_calibration_present=manual_calibration_present,
        overlay_review_completed=overlay_review_completed,
        qualified_engineer_review_completed=qualified_engineer_review_completed,
        review_status=review_status,
    )


def _require_curve_calibration(calibration: CurveCalibration) -> None:
    if not isinstance(calibration, CurveCalibration):
        raise ValueError("Manual extraction requires CurveCalibration.")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
