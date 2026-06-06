"""Reusable synthetic demo projects for LED curve workflows."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .calibration import AxisCalibration, CurveCalibration
from .models import (
    HUMAN_REVIEW_NOTE,
    SYNTHETIC_LABEL,
    CurveData,
    ExtractedPoint,
    LedCurveProject,
    ProjectMetadata,
    SourceMetadata,
)
from .project_io import save_project


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SYNTHETIC_DATA_DIR = PROJECT_ROOT / "data" / "synthetic"
DEFAULT_DEMO_PROJECTS_DIR = PROJECT_ROOT / "data" / "demo_projects"
DEMO_CREATED_AT_UTC = "2026-06-04T00:00:00Z"

COMMON_ASSUMPTIONS = [
    "Synthetic demo points approximate common LED datasheet curve shapes only.",
    "Data is reference-only and is not a manufacturer guarantee.",
    (
        "Qualified engineer review is required before WCCA, simulation, thermal "
        "derating, luminous-flux prediction, feasibility screening, or "
        "design-review use."
    ),
]


@dataclass(frozen=True)
class DemoPointSpec:
    """One synthetic curve point in engineering units."""

    point_id: str
    x: float
    y: float
    notes: str


@dataclass(frozen=True)
class DemoProjectSpec:
    """Definition used to build a complete synthetic `.ledcurve.json` project."""

    project_id: str
    project_name: str
    led_identifier: str
    curve_id: str
    curve_name: str
    x_axis_label: str
    x_axis_unit: str
    x_value_low: float
    x_value_high: float
    y_axis_label: str
    y_axis_unit: str
    y_value_low: float
    y_value_high: float
    source_page: str
    source_section: str
    intended_use: str
    description: str
    assumptions: tuple[str, ...]
    engineering_notes: str
    points: tuple[DemoPointSpec, ...]

    @property
    def project_filename(self) -> str:
        return f"{self.project_id}.ledcurve.json"

    @property
    def point_table_filename(self) -> str:
        return f"{self.project_id}_points.csv"


DEMO_PROJECT_SPECS = (
    DemoProjectSpec(
        project_id="synthetic_forward_voltage_vs_forward_current",
        project_name="Synthetic Forward Voltage vs Forward Current Demo",
        led_identifier="SYN-LED-FVIF-001",
        curve_id="curve_forward_voltage_vs_forward_current",
        curve_name="Forward Voltage vs Forward Current",
        x_axis_label="Forward Current",
        x_axis_unit="mA",
        x_value_low=0.0,
        x_value_high=1500.0,
        y_axis_label="Forward Voltage",
        y_axis_unit="V",
        y_value_low=2.4,
        y_value_high=3.9,
        source_page="synthetic_page_01",
        source_section="synthetic_forward_voltage_current_curve",
        intended_use="forward_voltage_lookup_seed",
        description="Synthetic seed project for voltage lookup versus drive current.",
        assumptions=(
            "Curve shape is monotonic and intended for lookup workflow demonstration.",
            "Low-current knee is simplified for deterministic demo data.",
        ),
        engineering_notes=(
            "Use this project to demonstrate preserving source pixels, axis "
            "calibration, and draft voltage lookup points."
        ),
        points=(
            DemoPointSpec("P01", 0.0, 2.55, "Synthetic near-off reference point."),
            DemoPointSpec("P02", 100.0, 2.78, "Synthetic low-current operating point."),
            DemoPointSpec("P03", 350.0, 3.02, "Synthetic nominal-lighting point."),
            DemoPointSpec("P04", 700.0, 3.25, "Synthetic mid-drive point."),
            DemoPointSpec("P05", 1000.0, 3.43, "Synthetic high-drive review point."),
            DemoPointSpec("P06", 1500.0, 3.72, "Synthetic upper demo range point."),
        ),
    ),
    DemoProjectSpec(
        project_id="synthetic_junction_temperature_vs_relative_luminous_flux",
        project_name="Synthetic Junction Temperature vs Relative Luminous Flux Demo",
        led_identifier="SYN-LED-TJFLUX-001",
        curve_id="curve_junction_temperature_vs_relative_luminous_flux",
        curve_name="Junction Temperature vs Relative Luminous Flux",
        x_axis_label="Junction Temperature",
        x_axis_unit="degC",
        x_value_low=-40.0,
        x_value_high=150.0,
        y_axis_label="Relative Luminous Flux",
        y_axis_unit="%",
        y_value_low=50.0,
        y_value_high=120.0,
        source_page="synthetic_page_02",
        source_section="synthetic_temperature_flux_curve",
        intended_use="thermal_flux_correction_seed",
        description="Synthetic seed project for luminous-flux correction versus junction temperature.",
        assumptions=(
            "Flux is normalized to 100 percent at the synthetic 25 degC reference.",
            "Temperature behavior is simplified for review-workflow demonstration.",
        ),
        engineering_notes=(
            "Use this project to demonstrate temperature-dependent optical "
            "correction data with explicit review boundaries."
        ),
        points=(
            DemoPointSpec("P01", -40.0, 113.0, "Synthetic cold-condition point."),
            DemoPointSpec("P02", 0.0, 105.0, "Synthetic low-temperature point."),
            DemoPointSpec("P03", 25.0, 100.0, "Synthetic normalization point."),
            DemoPointSpec("P04", 60.0, 91.0, "Synthetic warm-condition point."),
            DemoPointSpec("P05", 100.0, 79.0, "Synthetic high-temperature point."),
            DemoPointSpec("P06", 150.0, 64.0, "Synthetic upper-temperature point."),
        ),
    ),
    DemoProjectSpec(
        project_id="synthetic_forward_current_vs_relative_luminous_flux",
        project_name="Synthetic Forward Current vs Relative Luminous Flux Demo",
        led_identifier="SYN-LED-IFFLUX-001",
        curve_id="curve_forward_current_vs_relative_luminous_flux",
        curve_name="Forward Current vs Relative Luminous Flux",
        x_axis_label="Forward Current",
        x_axis_unit="mA",
        x_value_low=0.0,
        x_value_high=1500.0,
        y_axis_label="Relative Luminous Flux",
        y_axis_unit="%",
        y_value_low=0.0,
        y_value_high=180.0,
        source_page="synthetic_page_03",
        source_section="synthetic_current_flux_curve",
        intended_use="current_flux_lookup_seed",
        description="Synthetic seed project for luminous-flux response versus drive current.",
        assumptions=(
            "Flux is normalized to 100 percent at the synthetic 700 mA point.",
            "Droop and thermal interactions are simplified for deterministic demo data.",
        ),
        engineering_notes=(
            "Use this project to demonstrate optical-output lookup preparation "
            "without implying reviewed device performance."
        ),
        points=(
            DemoPointSpec("P01", 0.0, 0.0, "Synthetic off-current point."),
            DemoPointSpec("P02", 100.0, 17.0, "Synthetic low-output point."),
            DemoPointSpec("P03", 350.0, 52.0, "Synthetic partial-drive point."),
            DemoPointSpec("P04", 700.0, 100.0, "Synthetic normalization point."),
            DemoPointSpec("P05", 1000.0, 136.0, "Synthetic high-output point."),
            DemoPointSpec("P06", 1500.0, 168.0, "Synthetic upper-current point."),
        ),
    ),
    DemoProjectSpec(
        project_id="synthetic_thermal_derating_curve",
        project_name="Synthetic Thermal Derating Curve Demo",
        led_identifier="SYN-LED-DERATE-001",
        curve_id="curve_thermal_derating",
        curve_name="Thermal Derating Style Curve",
        x_axis_label="Ambient Temperature",
        x_axis_unit="degC",
        x_value_low=-40.0,
        x_value_high=125.0,
        y_axis_label="Allowable Forward Current",
        y_axis_unit="mA",
        y_value_low=0.0,
        y_value_high=1200.0,
        source_page="synthetic_page_04",
        source_section="synthetic_thermal_derating_curve",
        intended_use="thermal_derating_review_seed",
        description="Synthetic seed project for current derating versus ambient temperature.",
        assumptions=(
            "Flat region and roll-off are simplified to show derating workflow shape.",
            "Ambient-temperature derating is not a substitute for junction-temperature analysis.",
        ),
        engineering_notes=(
            "Use this project to demonstrate thermal derating data preparation "
            "with clear review status before downstream screening."
        ),
        points=(
            DemoPointSpec("P01", -40.0, 1000.0, "Synthetic cold-condition limit point."),
            DemoPointSpec("P02", 25.0, 1000.0, "Synthetic nominal ambient point."),
            DemoPointSpec("P03", 60.0, 900.0, "Synthetic derating onset point."),
            DemoPointSpec("P04", 85.0, 650.0, "Synthetic warm ambient derating point."),
            DemoPointSpec("P05", 105.0, 350.0, "Synthetic high ambient derating point."),
            DemoPointSpec("P06", 125.0, 0.0, "Synthetic maximum ambient cutoff point."),
        ),
    ),
)


def available_demo_project_ids() -> list[str]:
    """Return the stable project IDs available from this module."""

    return [spec.project_id for spec in DEMO_PROJECT_SPECS]


def build_demo_project(project_id: str) -> LedCurveProject:
    """Build one synthetic demo project by ID."""

    spec = _get_spec(project_id)
    calibration = _build_calibration(spec)
    curve = CurveData(
        curve_id=spec.curve_id,
        curve_name=spec.curve_name,
        x_axis_label=spec.x_axis_label,
        x_axis_unit=spec.x_axis_unit,
        y_axis_label=spec.y_axis_label,
        y_axis_unit=spec.y_axis_unit,
        extraction_method="synthetic_manual_curve_points",
        fit_model="shape_preserving_interpolation_ready",
        points=[
            _build_extracted_point(calibration, point)
            for point in spec.points
        ],
        assumptions=[*COMMON_ASSUMPTIONS, *spec.assumptions],
        review_status="pending_engineering_review",
        reviewer_notes="Synthetic demo points require overlay and engineering review.",
        engineering_notes=spec.engineering_notes,
    )
    return LedCurveProject(
        metadata=ProjectMetadata(
            project_id=spec.project_id,
            project_name=spec.project_name,
            led_identifier=spec.led_identifier,
            created_at_utc=DEMO_CREATED_AT_UTC,
            intended_use=spec.intended_use,
            description=spec.description,
            publication_classification="Safe to publish",
        ),
        source=SourceMetadata(
            source_id=f"source_{spec.project_id}",
            source_name=f"{spec.project_id}_synthetic_datasheet_plot",
            source_category="synthetic",
            source_type="synthetic_datasheet_style_plot",
            manufacturer="Synthetic LED Supplier",
            source_page=spec.source_page,
            source_section=spec.source_section,
            source_uri=f"synthetic://led-curve-studio/{spec.project_id}",
            plot_region_px={
                "left": 60.0,
                "top": 40.0,
                "width": 540.0,
                "height": 410.0,
            },
            notes="Synthetic plot source created for public-safe demonstration.",
        ),
        axis_calibration=calibration,
        curves=[curve],
        assumptions=[*COMMON_ASSUMPTIONS, *spec.assumptions],
        review_status="pending_engineering_review",
        reviewer_notes=(
            "Safe to publish as synthetic demo data; not reviewed for engineering use."
        ),
    )


def build_all_demo_projects() -> list[LedCurveProject]:
    """Build every reusable synthetic demo project."""

    return [build_demo_project(spec.project_id) for spec in DEMO_PROJECT_SPECS]


def write_demo_assets(
    synthetic_data_dir: str | Path = DEFAULT_SYNTHETIC_DATA_DIR,
    demo_projects_dir: str | Path = DEFAULT_DEMO_PROJECTS_DIR,
) -> dict[str, list[Path]]:
    """Write synthetic point tables and `.ledcurve.json` demo projects."""

    data_dir = Path(synthetic_data_dir)
    projects_dir = Path(demo_projects_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    projects_dir.mkdir(parents=True, exist_ok=True)

    point_tables = []
    project_files = []
    for spec in DEMO_PROJECT_SPECS:
        project = build_demo_project(spec.project_id)
        point_tables.append(_write_point_table(project, spec, data_dir))
        project_files.append(save_project(project, projects_dir / spec.project_filename))

    return {
        "synthetic_point_tables": point_tables,
        "demo_project_files": project_files,
    }


def _get_spec(project_id: str) -> DemoProjectSpec:
    for spec in DEMO_PROJECT_SPECS:
        if spec.project_id == project_id:
            return spec
    raise ValueError(f"Unknown synthetic demo project: {project_id}")


def _build_calibration(spec: DemoProjectSpec) -> CurveCalibration:
    return CurveCalibration(
        x_axis=AxisCalibration(
            pixel_low=80.0,
            pixel_high=560.0,
            value_low=spec.x_value_low,
            value_high=spec.x_value_high,
            scale="linear",
            label=spec.x_axis_label,
            unit=spec.x_axis_unit,
        ),
        y_axis=AxisCalibration(
            pixel_low=420.0,
            pixel_high=60.0,
            value_low=spec.y_value_low,
            value_high=spec.y_value_high,
            scale="linear",
            label=spec.y_axis_label,
            unit=spec.y_axis_unit,
        ),
    )


def _build_extracted_point(
    calibration: CurveCalibration,
    point: DemoPointSpec,
) -> ExtractedPoint:
    source_pixel_x = calibration.x_axis.value_to_pixel(point.x)
    source_pixel_y = calibration.y_axis.value_to_pixel(point.y)
    return ExtractedPoint(
        point_id=point.point_id,
        source_pixel_x=round(source_pixel_x, 3),
        source_pixel_y=round(source_pixel_y, 3),
        x=point.x,
        y=point.y,
        review_status="synthetic_demo_pending_review",
        notes=point.notes,
    )


def _write_point_table(
    project: LedCurveProject,
    spec: DemoProjectSpec,
    output_dir: Path,
) -> Path:
    output_path = output_dir / spec.point_table_filename
    curve = project.curves[0]
    fieldnames = [
        "synthetic_label",
        "human_review_required",
        "publication_classification",
        "project_id",
        "curve_id",
        "curve_name",
        "point_id",
        "x_axis_label",
        "x_axis_unit",
        "x_value",
        "y_axis_label",
        "y_axis_unit",
        "y_value",
        "source_pixel_x",
        "source_pixel_y",
        "review_status",
        "notes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for point in curve.points:
            writer.writerow(
                {
                    "synthetic_label": SYNTHETIC_LABEL,
                    "human_review_required": HUMAN_REVIEW_NOTE,
                    "publication_classification": project.metadata.publication_classification,
                    "project_id": project.metadata.project_id,
                    "curve_id": curve.curve_id,
                    "curve_name": curve.curve_name,
                    "point_id": point.point_id,
                    "x_axis_label": curve.x_axis_label,
                    "x_axis_unit": curve.x_axis_unit,
                    "x_value": f"{point.x:.6g}",
                    "y_axis_label": curve.y_axis_label,
                    "y_axis_unit": curve.y_axis_unit,
                    "y_value": f"{point.y:.6g}",
                    "source_pixel_x": f"{point.source_pixel_x:.3f}",
                    "source_pixel_y": f"{point.source_pixel_y:.3f}",
                    "review_status": point.review_status,
                    "notes": point.notes,
                }
            )
    return output_path


def main() -> None:
    """Generate checked-in synthetic demo data assets."""

    written = write_demo_assets()
    for output_group in written.values():
        for path in output_group:
            print(path.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    main()
