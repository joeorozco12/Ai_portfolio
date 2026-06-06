import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import AxisCalibration, CurveCalibration
from led_digitizer.models import (
    HUMAN_REVIEW_NOTE,
    SYNTHETIC_LABEL,
    CurveData,
    ExtractedPoint,
    LedCurveProject,
    ProjectMetadata,
    SourceMetadata,
)
from led_digitizer.project_io import load_project, save_project


class ProjectIoTests(unittest.TestCase):
    def test_project_model_stores_required_metadata(self):
        project = _build_project()

        self.assertEqual(project.metadata.project_id, "synthetic-forward-current-demo")
        self.assertEqual(project.source.source_category, "synthetic")
        self.assertEqual(project.axis_calibration.x_axis.unit, "V")
        self.assertEqual(project.axis_calibration.y_axis.unit, "mA")
        self.assertEqual(project.review_status, "pending_engineering_review")
        self.assertEqual(project.reviewer_notes, "Overlay review not completed.")
        self.assertEqual(project.assumptions[0], "Synthetic plot shape for demo only.")
        self.assertEqual(len(project.curves), 1)
        self.assertEqual(len(project.curves[0].points), 2)
        self.assertEqual(project.curves[0].reviewer_notes, "Manual point picks need review.")

    def test_curve_and_points_can_be_added(self):
        project = _build_project(curves=[])
        curve = CurveData(
            curve_id="curve_forward_voltage",
            curve_name="Forward Voltage vs Forward Current",
            x_axis_label="Forward Voltage",
            x_axis_unit="V",
            y_axis_label="Forward Current",
            y_axis_unit="mA",
            fit_model="not_fit",
        )
        curve.add_point(
            ExtractedPoint(
                point_id="P01",
                source_pixel_x=80.0,
                source_pixel_y=420.0,
                x=2.5,
                y=0.0,
            )
        )

        project.add_curve(curve)

        self.assertEqual(project.curves[0].curve_id, "curve_forward_voltage")
        self.assertEqual(project.curves[0].points[0].point_id, "P01")

    def test_project_saves_and_loads_ledcurve_json(self):
        project = _build_project()

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "synthetic_forward_current.ledcurve.json"

            saved_path = save_project(project, path)
            loaded = load_project(saved_path)

        self.assertEqual(loaded.to_dict(), project.to_dict())
        self.assertEqual(loaded.curves[0].points[1].x, 3.25)
        self.assertEqual(loaded.curves[0].points[1].review_status, "draft_extraction")

    def test_project_serializes_calibration_sanity_metadata(self):
        project = _build_project()

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "synthetic_forward_current.ledcurve.json"
            save_project(project, path)
            payload = json.loads(path.read_text(encoding="utf-8"))

        calibration = payload["axis_calibration"]
        self.assertFalse(calibration["x_axis"]["inverted_image_axis"])
        self.assertTrue(calibration["y_axis"]["inverted_image_axis"])
        self.assertFalse(
            calibration["y_axis"]["value_increases_as_pixel_increases"]
        )
        self.assertEqual(calibration["sanity_check"]["passes_tolerance"], None)
        self.assertAlmostEqual(
            calibration["sanity_check"]["x_axis"]["max_abs_residual"],
            0.0,
        )
        self.assertAlmostEqual(
            calibration["sanity_check"]["y_axis"]["max_abs_residual"],
            0.0,
        )
        self.assertEqual(
            calibration["sanity_check"]["x_axis"]["residuals"][0]["point_id"],
            "cal_low",
        )

    def test_saved_project_contains_safety_and_review_controls(self):
        project = _build_project()

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "synthetic_forward_current.ledcurve.json"
            save_project(project, path)
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["synthetic_label"], SYNTHETIC_LABEL)
        self.assertEqual(payload["human_review_required"], HUMAN_REVIEW_NOTE)
        self.assertEqual(payload["publication_classification"], "Needs review")
        self.assertEqual(payload["review_status"], "pending_engineering_review")
        self.assertEqual(payload["curves"][0]["reviewer_notes"], "Manual point picks need review.")

    def test_save_rejects_non_project_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "synthetic_forward_current.json"

            with self.assertRaises(ValueError):
                save_project(_build_project(), path)

    def test_old_calibration_payload_loads_without_computed_metadata(self):
        project = _build_project()
        payload = project.to_dict()
        payload["axis_calibration"].pop("sanity_check")
        for axis_key in ("x_axis", "y_axis"):
            payload["axis_calibration"][axis_key].pop("inverted_image_axis")
            payload["axis_calibration"][axis_key].pop(
                "value_increases_as_pixel_increases"
            )

        loaded = LedCurveProject.from_dict(payload)

        self.assertEqual(loaded.axis_calibration.x_axis.scale, "linear")
        self.assertTrue(loaded.axis_calibration.y_axis.inverted_image_axis)


def _build_project(curves=None):
    calibration = CurveCalibration(
        x_axis=AxisCalibration(
            pixel_low=80.0,
            pixel_high=560.0,
            value_low=2.5,
            value_high=4.5,
            scale="linear",
            label="Forward Voltage",
            unit="V",
        ),
        y_axis=AxisCalibration(
            pixel_low=420.0,
            pixel_high=60.0,
            value_low=0.0,
            value_high=4000.0,
            scale="linear",
            label="Forward Current",
            unit="mA",
        ),
    )
    if curves is None:
        curves = [
            CurveData(
                curve_id="curve_forward_voltage_current",
                curve_name="Forward Voltage vs Forward Current",
                x_axis_label="Forward Voltage",
                x_axis_unit="V",
                y_axis_label="Forward Current",
                y_axis_unit="mA",
                extraction_method="manual_curve_pick",
                fit_model="pchip_shape_preserving_interpolation",
                points=[
                    ExtractedPoint(
                        point_id="P01",
                        source_pixel_x=80.0,
                        source_pixel_y=420.0,
                        x=2.5,
                        y=0.0,
                    ),
                    ExtractedPoint(
                        point_id="P02",
                        source_pixel_x=260.0,
                        source_pixel_y=330.0,
                        x=3.25,
                        y=1000.0,
                    ),
                ],
                assumptions=[
                    "Manual synthetic picks represent visible curve markers only."
                ],
                review_status="draft_extraction",
                reviewer_notes="Manual point picks need review.",
                engineering_notes="Reference-only synthetic curve data.",
            )
        ]
    return LedCurveProject(
        metadata=ProjectMetadata(
            project_id="synthetic-forward-current-demo",
            project_name="Synthetic Forward Current Curve",
            led_identifier="SYN-LED-170",
            created_at_utc="2026-06-04T00:00:00Z",
            description="Synthetic LED datasheet-style curve project.",
        ),
        source=SourceMetadata(
            source_id="source_synthetic_plot",
            source_name="synthetic_datasheet_style_plot",
            source_category="synthetic",
            source_page="synthetic_page_20",
            source_section="synthetic_forward_current_characteristics",
            plot_region_px={
                "left": 60.0,
                "top": 40.0,
                "width": 540.0,
                "height": 410.0,
            },
            notes="Synthetic plot source for public-safe demonstration.",
        ),
        axis_calibration=calibration,
        curves=curves,
        assumptions=["Synthetic plot shape for demo only."],
        review_status="pending_engineering_review",
        reviewer_notes="Overlay review not completed.",
    )


if __name__ == "__main__":
    unittest.main()
