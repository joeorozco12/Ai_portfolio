import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import AxisCalibration, CurveCalibration


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

    def test_reversed_y_axis_pixel_to_value(self):
        axis = AxisCalibration(
            pixel_low=420.0,
            pixel_high=60.0,
            value_low=0.0,
            value_high=4000.0,
        )

        self.assertAlmostEqual(axis.pixel_to_value(330.0), 1000.0)
        self.assertAlmostEqual(axis.value_to_pixel(1000.0), 330.0)

    def test_log_axis_pixel_to_value(self):
        axis = AxisCalibration(
            pixel_low=100.0,
            pixel_high=300.0,
            value_low=10.0,
            value_high=1000.0,
            scale="log",
        )

        self.assertTrue(math.isclose(axis.pixel_to_value(200.0), 100.0))

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


if __name__ == "__main__":
    unittest.main()
