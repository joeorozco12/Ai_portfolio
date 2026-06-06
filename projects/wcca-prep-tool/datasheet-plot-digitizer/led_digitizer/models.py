"""Project model for LED Datasheet Curve Studio project files."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .calibration import AxisCalibration, CurveCalibration, EngineeringPoint


SCHEMA_VERSION = "1.0"
SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts "
    "only. A qualified engineer owns final review and approval."
)
PUBLICATION_CLASSIFICATIONS = {
    "Safe to publish",
    "Needs review",
    "Internal only",
    "Do not publish",
}
SOURCE_CATEGORIES = {"synthetic", "public"}


@dataclass
class ProjectMetadata:
    """Top-level project identifiers and intended engineering use."""

    project_id: str
    project_name: str
    led_identifier: str
    created_by: str = "Jose Orozco"
    created_at_utc: str = "not_recorded"
    intended_use: str = "reviewable_led_curve_data_prep"
    description: str = ""
    publication_classification: str = "Needs review"

    def __post_init__(self) -> None:
        _require_text(self.project_id, "project_id")
        _require_text(self.project_name, "project_name")
        _require_text(self.led_identifier, "led_identifier")
        _require_text(self.created_by, "created_by")
        _require_text(self.intended_use, "intended_use")
        if self.publication_classification not in PUBLICATION_CLASSIFICATIONS:
            raise ValueError("Project publication classification is not recognized.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "led_identifier": self.led_identifier,
            "created_by": self.created_by,
            "created_at_utc": self.created_at_utc,
            "intended_use": self.intended_use,
            "description": self.description,
            "publication_classification": self.publication_classification,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProjectMetadata":
        return cls(
            project_id=str(payload["project_id"]),
            project_name=str(payload["project_name"]),
            led_identifier=str(payload["led_identifier"]),
            created_by=str(payload.get("created_by", "Jose Orozco")),
            created_at_utc=str(payload.get("created_at_utc", "not_recorded")),
            intended_use=str(
                payload.get("intended_use", "reviewable_led_curve_data_prep")
            ),
            description=str(payload.get("description", "")),
            publication_classification=str(
                payload.get("publication_classification", "Needs review")
            ),
        )


@dataclass
class SourceMetadata:
    """Traceability details for the public or synthetic plot source."""

    source_id: str
    source_name: str
    source_category: str = "synthetic"
    source_type: str = "datasheet_plot_image"
    manufacturer: str = "Synthetic LED Supplier"
    source_page: str = ""
    source_section: str = ""
    source_uri: str = ""
    plot_region_px: dict[str, float] = field(default_factory=dict)
    notes: str = ""

    def __post_init__(self) -> None:
        _require_text(self.source_id, "source_id")
        _require_text(self.source_name, "source_name")
        _require_text(self.source_type, "source_type")
        if self.source_category not in SOURCE_CATEGORIES:
            raise ValueError("Source category must be 'synthetic' or 'public'.")
        self.plot_region_px = _float_dict(self.plot_region_px, "plot_region_px")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_category": self.source_category,
            "source_type": self.source_type,
            "manufacturer": self.manufacturer,
            "source_page": self.source_page,
            "source_section": self.source_section,
            "source_uri": self.source_uri,
            "plot_region_px": dict(self.plot_region_px),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceMetadata":
        return cls(
            source_id=str(payload["source_id"]),
            source_name=str(payload["source_name"]),
            source_category=str(payload.get("source_category", "synthetic")),
            source_type=str(payload.get("source_type", "datasheet_plot_image")),
            manufacturer=str(payload.get("manufacturer", "Synthetic LED Supplier")),
            source_page=str(payload.get("source_page", "")),
            source_section=str(payload.get("source_section", "")),
            source_uri=str(payload.get("source_uri", "")),
            plot_region_px=dict(payload.get("plot_region_px", {})),
            notes=str(payload.get("notes", "")),
        )


@dataclass
class ExtractedPoint:
    """One curve point with source-pixel and engineering-unit coordinates."""

    point_id: str
    source_pixel_x: float
    source_pixel_y: float
    x: float
    y: float
    review_status: str = "draft_extraction"
    notes: str = ""

    def __post_init__(self) -> None:
        _require_text(self.point_id, "point_id")
        _require_text(self.review_status, "review_status")
        self.source_pixel_x = float(self.source_pixel_x)
        self.source_pixel_y = float(self.source_pixel_y)
        self.x = float(self.x)
        self.y = float(self.y)

    @classmethod
    def from_engineering_point(cls, point: EngineeringPoint) -> "ExtractedPoint":
        return cls(
            point_id=point.point_id,
            source_pixel_x=point.source_pixel_x,
            source_pixel_y=point.source_pixel_y,
            x=point.x,
            y=point.y,
            review_status=point.review_status,
            notes=point.notes,
        )

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

    def to_dict(self) -> dict[str, Any]:
        return {
            "point_id": self.point_id,
            "source_pixel_x": self.source_pixel_x,
            "source_pixel_y": self.source_pixel_y,
            "x": self.x,
            "y": self.y,
            "review_status": self.review_status,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExtractedPoint":
        return cls(
            point_id=str(payload["point_id"]),
            source_pixel_x=float(payload["source_pixel_x"]),
            source_pixel_y=float(payload["source_pixel_y"]),
            x=float(payload["x"]),
            y=float(payload["y"]),
            review_status=str(payload.get("review_status", "draft_extraction")),
            notes=str(payload.get("notes", "")),
        )


@dataclass
class CurveData:
    """Curve definition, extracted points, assumptions, and review metadata."""

    curve_id: str
    curve_name: str
    x_axis_label: str
    x_axis_unit: str
    y_axis_label: str
    y_axis_unit: str
    extraction_method: str = "manual_curve_pick"
    fit_model: str = "not_fit"
    points: list[ExtractedPoint] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    review_status: str = "draft_extraction"
    reviewer_notes: str = ""
    engineering_notes: str = ""

    def __post_init__(self) -> None:
        _require_text(self.curve_id, "curve_id")
        _require_text(self.curve_name, "curve_name")
        _require_text(self.x_axis_label, "x_axis_label")
        _require_text(self.y_axis_label, "y_axis_label")
        _require_text(self.extraction_method, "extraction_method")
        _require_text(self.fit_model, "fit_model")
        _require_text(self.review_status, "review_status")
        self.points = [
            point if isinstance(point, ExtractedPoint) else ExtractedPoint.from_dict(point)
            for point in self.points
        ]
        self.assumptions = _string_list(self.assumptions, "assumptions")

    def add_point(self, point: ExtractedPoint) -> None:
        self.points.append(point)

    def to_dict(self) -> dict[str, Any]:
        return {
            "curve_id": self.curve_id,
            "curve_name": self.curve_name,
            "x_axis_label": self.x_axis_label,
            "x_axis_unit": self.x_axis_unit,
            "y_axis_label": self.y_axis_label,
            "y_axis_unit": self.y_axis_unit,
            "extraction_method": self.extraction_method,
            "fit_model": self.fit_model,
            "points": [point.to_dict() for point in self.points],
            "assumptions": list(self.assumptions),
            "review_status": self.review_status,
            "reviewer_notes": self.reviewer_notes,
            "engineering_notes": self.engineering_notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CurveData":
        return cls(
            curve_id=str(payload["curve_id"]),
            curve_name=str(payload["curve_name"]),
            x_axis_label=str(payload["x_axis_label"]),
            x_axis_unit=str(payload.get("x_axis_unit", "")),
            y_axis_label=str(payload["y_axis_label"]),
            y_axis_unit=str(payload.get("y_axis_unit", "")),
            extraction_method=str(payload.get("extraction_method", "manual_curve_pick")),
            fit_model=str(payload.get("fit_model", "not_fit")),
            points=[
                ExtractedPoint.from_dict(point)
                for point in payload.get("points", [])
            ],
            assumptions=_string_list(payload.get("assumptions", []), "assumptions"),
            review_status=str(payload.get("review_status", "draft_extraction")),
            reviewer_notes=str(payload.get("reviewer_notes", "")),
            engineering_notes=str(payload.get("engineering_notes", "")),
        )


@dataclass
class LedCurveProject:
    """Complete `.ledcurve.json` project payload."""

    metadata: ProjectMetadata
    source: SourceMetadata
    axis_calibration: CurveCalibration
    curves: list[CurveData] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    review_status: str = "draft_extraction"
    reviewer_notes: str = ""
    schema_version: str = SCHEMA_VERSION
    synthetic_label: str = SYNTHETIC_LABEL
    human_review_required: str = HUMAN_REVIEW_NOTE

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"Unsupported project schema version: {self.schema_version}")
        if self.synthetic_label != SYNTHETIC_LABEL:
            raise ValueError("Project synthetic label is missing or modified.")
        if self.human_review_required != HUMAN_REVIEW_NOTE:
            raise ValueError("Project human-review note is missing or modified.")
        if not isinstance(self.metadata, ProjectMetadata):
            self.metadata = ProjectMetadata.from_dict(self.metadata)
        if not isinstance(self.source, SourceMetadata):
            self.source = SourceMetadata.from_dict(self.source)
        if not isinstance(self.axis_calibration, CurveCalibration):
            self.axis_calibration = curve_calibration_from_dict(self.axis_calibration)
        self.curves = [
            curve if isinstance(curve, CurveData) else CurveData.from_dict(curve)
            for curve in self.curves
        ]
        self.assumptions = _string_list(self.assumptions, "assumptions")
        _require_text(self.review_status, "review_status")

    def add_curve(self, curve: CurveData) -> None:
        self.curves.append(curve)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "synthetic_label": self.synthetic_label,
            "human_review_required": self.human_review_required,
            "publication_classification": self.metadata.publication_classification,
            "project_metadata": self.metadata.to_dict(),
            "source_metadata": self.source.to_dict(),
            "axis_calibration": curve_calibration_to_dict(self.axis_calibration),
            "curves": [curve.to_dict() for curve in self.curves],
            "assumptions": list(self.assumptions),
            "review_status": self.review_status,
            "reviewer_notes": self.reviewer_notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "LedCurveProject":
        return cls(
            schema_version=str(payload["schema_version"]),
            synthetic_label=str(payload.get("synthetic_label", "")),
            human_review_required=str(payload.get("human_review_required", "")),
            metadata=ProjectMetadata.from_dict(payload["project_metadata"]),
            source=SourceMetadata.from_dict(payload["source_metadata"]),
            axis_calibration=curve_calibration_from_dict(payload["axis_calibration"]),
            curves=[
                CurveData.from_dict(curve)
                for curve in payload.get("curves", [])
            ],
            assumptions=_string_list(payload.get("assumptions", []), "assumptions"),
            review_status=str(payload.get("review_status", "draft_extraction")),
            reviewer_notes=str(payload.get("reviewer_notes", "")),
        )


def axis_calibration_to_dict(axis: AxisCalibration) -> dict[str, Any]:
    return {
        "pixel_low": axis.pixel_low,
        "pixel_high": axis.pixel_high,
        "value_low": axis.value_low,
        "value_high": axis.value_high,
        "scale": axis.scale,
        "label": axis.label,
        "unit": axis.unit,
        "inverted_image_axis": axis.inverted_image_axis,
        "value_increases_as_pixel_increases": (
            axis.value_increases_as_pixel_increases
        ),
    }


def axis_calibration_from_dict(payload: dict[str, Any]) -> AxisCalibration:
    return AxisCalibration(
        pixel_low=float(payload["pixel_low"]),
        pixel_high=float(payload["pixel_high"]),
        value_low=float(payload["value_low"]),
        value_high=float(payload["value_high"]),
        scale=str(payload.get("scale", "linear")),
        label=str(payload.get("label", "")),
        unit=str(payload.get("unit", "")),
    )


def curve_calibration_to_dict(calibration: CurveCalibration) -> dict[str, Any]:
    return {
        "x_axis": axis_calibration_to_dict(calibration.x_axis),
        "y_axis": axis_calibration_to_dict(calibration.y_axis),
        "sanity_check": calibration.sanity_check(),
    }


def curve_calibration_from_dict(payload: dict[str, Any]) -> CurveCalibration:
    return CurveCalibration(
        x_axis=axis_calibration_from_dict(payload["x_axis"]),
        y_axis=axis_calibration_from_dict(payload["y_axis"]),
    )


def _float_dict(values: dict[str, Any], field_name: str) -> dict[str, float]:
    if values is None:
        return {}
    if not isinstance(values, dict):
        raise ValueError(f"{field_name} must be a dictionary.")
    return {str(key): float(value) for key, value in values.items()}


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _string_list(values: list[str], field_name: str) -> list[str]:
    if values is None:
        return []
    if not isinstance(values, list):
        raise ValueError(f"{field_name} must be a list of strings.")
    normalized = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must contain only strings.")
        normalized.append(value)
    return normalized
