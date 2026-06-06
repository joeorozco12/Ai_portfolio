import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import AxisCalibration, CurveCalibration
from led_digitizer.extraction_manual import (
    MANUAL_METHOD,
    ManualPixelPick,
    build_review_control_status,
    convert_manual_picks,
)


class ManualExtractionTests(unittest.TestCase):
    def test_manual_pick_conversion_preserves_pixels_and_review_status(self):
        points = convert_manual_picks(
            [
                ManualPixelPick(
                    point_id="P04",
                    source_pixel_x=260.0,
                    source_pixel_y=330.0,
                    review_status="draft_extraction",
                    notes="synthetic manual point",
                )
            ],
            _calibration(),
        )

        self.assertEqual(len(points), 1)
        self.assertEqual(points[0].point_id, "P04")
        self.assertEqual(points[0].method, MANUAL_METHOD)
        self.assertEqual(points[0].confidence, 1.0)
        self.assertEqual(points[0].review_status, "draft_extraction")
        self.assertAlmostEqual(points[0].source_pixel_x, 260.0)
        self.assertAlmostEqual(points[0].source_pixel_y, 330.0)
        self.assertAlmostEqual(points[0].x, 3.25)
        self.assertAlmostEqual(points[0].y, 1000.0)

    def test_manual_extraction_requires_calibration_and_points(self):
        with self.assertRaises(ValueError):
            convert_manual_picks([], _calibration())

        with self.assertRaises(ValueError):
            convert_manual_picks([ManualPixelPick("P01", 80.0, 420.0)], None)

    def test_manual_pick_rejects_invalid_source_pixels(self):
        with self.assertRaises(ValueError):
            ManualPixelPick("P01", -1.0, 420.0)

    def test_review_controls_block_downstream_use_until_reviewed(self):
        draft_status = build_review_control_status(
            manual_calibration_present=True,
            overlay_review_completed=False,
            qualified_engineer_review_completed=False,
            review_status="draft_extraction",
        )

        self.assertFalse(draft_status.downstream_use_allowed)
        self.assertIn("overlay_review", draft_status.missing_controls)
        self.assertIn("qualified_engineer_review", draft_status.missing_controls)
        self.assertIn("reviewed_status", draft_status.missing_controls)

        reviewed_status = build_review_control_status(
            manual_calibration_present=True,
            overlay_review_completed=True,
            qualified_engineer_review_completed=True,
            review_status="engineer_reviewed_demo",
        )

        self.assertTrue(reviewed_status.downstream_use_allowed)
        self.assertEqual(reviewed_status.missing_controls, [])


def _calibration() -> CurveCalibration:
    return CurveCalibration(
        x_axis=AxisCalibration(80.0, 560.0, 2.5, 4.5),
        y_axis=AxisCalibration(420.0, 60.0, 0.0, 4000.0),
    )


if __name__ == "__main__":
    unittest.main()
