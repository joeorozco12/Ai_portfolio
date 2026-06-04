import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.curve_fit import build_pchip_segments, evaluate_pchip, linear_interpolate
from led_digitizer.sample_project import load_sample_points


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CurveFitTests(unittest.TestCase):
    def setUp(self):
        self.points = load_sample_points(PROJECT_ROOT / "data" / "synthetic_manual_points.csv")

    def test_linear_interpolation_hits_known_point(self):
        self.assertAlmostEqual(linear_interpolate(self.points, 3.25), 1000.0)

    def test_pchip_segments_hit_endpoints(self):
        segments = build_pchip_segments(self.points)

        self.assertEqual(len(segments), len(self.points) - 1)
        self.assertAlmostEqual(evaluate_pchip(segments, self.points[0].x), self.points[0].y)
        self.assertAlmostEqual(evaluate_pchip(segments, self.points[-1].x), self.points[-1].y)

    def test_pchip_midpoint_stays_inside_neighbor_range(self):
        segments = build_pchip_segments(self.points)
        x_mid = (self.points[3].x + self.points[4].x) / 2.0
        y_mid = evaluate_pchip(segments, x_mid)

        lower = min(self.points[3].y, self.points[4].y)
        upper = max(self.points[3].y, self.points[4].y)
        self.assertGreaterEqual(y_mid, lower)
        self.assertLessEqual(y_mid, upper)


if __name__ == "__main__":
    unittest.main()
