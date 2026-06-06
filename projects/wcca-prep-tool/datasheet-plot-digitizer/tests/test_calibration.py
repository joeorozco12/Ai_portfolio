import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import (
    AxisCalibration,
    AxisCalibrationCheckPoint,
    CurveCalibration,
)


class CalibrationTests(unittest.TestCase):
    def test_linear_x_axis_pixel_to_value(self):
        axis = AxisCalibration(
            pixel_low=80.0,
            pixel_high=560.0,
            value_low=2.5,
            value_high=4.5,
        )

        self.assertAlmostEqual(axis.pixel_to_value(260.0), 3.25)
        self.assertAlmostEqual(axis.value_to_pixel(3.25), 260.0)
        self.assertFalse(axis.inverted_image_axis)
        self.assertTrue(axis.value_increases_as_pixel_increases)

    def test_linear_y_axis_inverted_image_axis_pixel_to_value(self):
        axis = AxisCalibration(
            pixel_low=420.0,
            pixel_high=60.0,
            value_low=0.0,
            value_high=4000.0,
        )

        self.assertAlmostEqual(axis.pixel_to_value(330.0), 1000.0)
        self.assertAlmostEqual(axis.value_to_pixel(1000.0), 330.0)
        self.assertTrue(axis.inverted_image_axis)
        self.assertFalse(axis.value_increases_as_pixel_increases)

    def test_log_x_axis_pixel_to_value(self):
        axis = AxisCalibration(
            pixel_low=100.0,
            pixel_high=300.0,
            value_low=10.0,
            value_high=1000.0,
            scale="log",
        )

        self.assertTrue(math.isclose(axis.pixel_to_value(200.0), 100.0))
        self.assertAlmostEqual(axis.value_to_pixel(100.0), 200.0)

    def test_log_y_axis_with_inverted_image_axis_pixel_to_value(self):
        axis = AxisCalibration(
            pixel_low=400.0,
            pixel_high=100.0,
            value_low=1.0,
            value_high=1000.0,
            scale="log",
            label="Forward Current",
            unit="mA",
        )

        self.assertTrue(math.isclose(axis.pixel_to_value(300.0), 10.0))
        self.assertAlmostEqual(axis.value_to_pixel(10.0), 300.0)
        self.assertTrue(axis.inverted_image_axis)

    def test_curve_calibration_preserves_source_pixels(self):
        calibration = CurveCalibration(
            x_axis=AxisCalibration(80.0, 560.0, 2.5, 4.5),
            y_axis=AxisCalibration(420.0, 60.0, 0.0, 4000.0),
        )

        point = calibration.pixel_to_engineering("P04", 260.0, 330.0)

        self.assertEqual(point.point_id, "P04")
        self.assertAlmostEqual(point.x, 3.25)
        self.assertAlmostEqual(point.y, 1000.0)
        self.assertAlmostEqual(point.source_pixel_x, 260.0)
        self.assertAlmostEqual(point.source_pixel_y, 330.0)

    def test_calibration_residuals_report_expected_error(self):
        axis = AxisCalibration(
            pixel_low=0.0,
            pixel_high=100.0,
            value_low=0.0,
            value_high=10.0,
            label="Forward Voltage",
            unit="V",
        )

        residuals = axis.calibration_residuals(
            [
                AxisCalibrationCheckPoint("mid_low", 25.0, 2.4),
                ("mid_high", 75.0, 7.6),
            ]
        )

        self.assertEqual(residuals[0].point_id, "mid_low")
        self.assertAlmostEqual(residuals[0].actual_value, 2.5)
        self.assertAlmostEqual(residuals[0].residual, 0.1)
        self.assertAlmostEqual(residuals[1].residual, -0.1)
        self.assertAlmostEqual(residuals[1].absolute_residual, 0.1)

    def test_axis_sanity_check_returns_report_ready_summary(self):
        axis = AxisCalibration(0.0, 100.0, 0.0, 10.0, label="Voltage", unit="V")

        summary = axis.sanity_check(
            check_points=[("low_mid", 25.0, 2.4), ("high_mid", 75.0, 7.6)],
            tolerance=0.2,
        )
        payload = summary.to_dict()

        self.assertTrue(payload["passes_tolerance"])
        self.assertEqual(payload["label"], "Voltage")
        self.assertEqual(payload["unit"], "V")
        self.assertAlmostEqual(payload["max_abs_residual"], 0.1)
        self.assertAlmostEqual(payload["mean_abs_residual"], 0.1)
        self.assertAlmostEqual(payload["rms_residual"], 0.1)
        self.assertEqual(len(payload["residuals"]), 2)

    def test_curve_sanity_check_combines_x_and_y_outputs(self):
        calibration = CurveCalibration(
            x_axis=AxisCalibration(0.0, 100.0, 0.0, 10.0),
            y_axis=AxisCalibration(200.0, 0.0, 0.0, 20.0),
        )

        payload = calibration.sanity_check(
            x_check_points=[("x_mid", 50.0, 5.0)],
            y_check_points=[("y_mid", 100.0, 10.0)],
            tolerance=0.0,
        )

        self.assertTrue(payload["passes_tolerance"])
        self.assertIn("x_axis", payload)
        self.assertIn("y_axis", payload)
        self.assertTrue(payload["y_axis"]["inverted_image_axis"])

    def test_invalid_calibration_inputs_fail_clearly(self):
        invalid_cases = [
            (
                {"pixel_low": 10.0, "pixel_high": 10.0, "value_low": 0.0, "value_high": 1.0},
                "pixels must be different",
            ),
            (
                {"pixel_low": 0.0, "pixel_high": 10.0, "value_low": 1.0, "value_high": 1.0},
                "values must be different",
            ),
            (
                {
                    "pixel_low": 0.0,
                    "pixel_high": 10.0,
                    "value_low": 0.0,
                    "value_high": 1.0,
                    "scale": "sqrt",
                },
                "Axis scale must be",
            ),
            (
                {
                    "pixel_low": 0.0,
                    "pixel_high": 10.0,
                    "value_low": 0.0,
                    "value_high": 10.0,
                    "scale": "log",
                },
                "Log-scale calibration values must be positive",
            ),
            (
                {
                    "pixel_low": math.inf,
                    "pixel_high": 10.0,
                    "value_low": 0.0,
                    "value_high": 10.0,
                },
                "finite number",
            ),
        ]

        for kwargs, expected_message in invalid_cases:
            with self.subTest(expected_message=expected_message):
                with self.assertRaisesRegex(ValueError, expected_message):
                    AxisCalibration(**kwargs)

    def test_log_value_to_pixel_rejects_non_positive_value(self):
        axis = AxisCalibration(0.0, 10.0, 1.0, 100.0, scale="log")

        with self.assertRaisesRegex(ValueError, "Log-scale values must be positive"):
            axis.value_to_pixel(0.0)


if __name__ == "__main__":
    unittest.main()
