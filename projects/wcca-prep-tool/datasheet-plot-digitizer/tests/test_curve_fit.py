import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import EngineeringPoint
from led_digitizer.curve_fit import (
    build_lookup_domain,
    build_pchip_segments,
    describe_out_of_range_policy,
    evaluate_pchip,
    linear_interpolate,
)
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

    def test_default_out_of_range_behavior_clamps_endpoint_values(self):
        segments = build_pchip_segments(self.points)

        self.assertEqual(
            linear_interpolate(self.points, self.points[0].x - 0.5),
            self.points[0].y,
        )
        self.assertEqual(
            evaluate_pchip(segments, self.points[-1].x + 0.5),
            self.points[-1].y,
        )

    def test_raise_out_of_range_behavior_is_explicit(self):
        segments = build_pchip_segments(self.points)

        with self.assertRaises(ValueError):
            linear_interpolate(
                self.points,
                self.points[0].x - 0.5,
                out_of_range="raise",
            )
        with self.assertRaises(ValueError):
            evaluate_pchip(
                segments,
                self.points[-1].x + 0.5,
                out_of_range="raise",
            )

    def test_lookup_domain_serializes_out_of_range_policy(self):
        domain = build_lookup_domain(self.points, out_of_range="raise")

        self.assertEqual(domain.x_min, self.points[0].x)
        self.assertEqual(domain.x_max, self.points[-1].x)
        self.assertEqual(domain.to_dict()["out_of_range_policy"], "raise")
        self.assertIn("raise ValueError", domain.to_dict()["out_of_range_behavior"])

    def test_invalid_out_of_range_policy_fails_clearly(self):
        with self.assertRaises(ValueError):
            linear_interpolate(self.points, self.points[0].x, out_of_range="hold")

    def test_duplicate_x_values_are_rejected(self):
        duplicate_points = [
            EngineeringPoint("p1", 10.0, 20.0, 1.0, 100.0),
            EngineeringPoint("p2", 12.0, 18.0, 1.0, 110.0),
        ]

        with self.assertRaises(ValueError):
            build_pchip_segments(duplicate_points)

    def test_policy_description_is_report_ready(self):
        self.assertEqual(
            describe_out_of_range_policy("clamp"),
            "Inputs below or above the digitized x-domain return endpoint y-values.",
        )


if __name__ == "__main__":
    unittest.main()
