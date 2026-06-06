import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import EngineeringPoint
from led_digitizer.sample_project import load_sample_points
from led_digitizer.validation import (
    HUMAN_REVIEW_NOTE,
    LINEAR_MODEL,
    PCHIP_MODEL,
    calculate_residuals,
    check_monotonicity,
    validate_curve_fit,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.points = load_sample_points(PROJECT_ROOT / "data" / "synthetic_manual_points.csv")

    def test_validate_pchip_fit_reports_zero_knot_residuals(self):
        report = validate_curve_fit(
            self.points,
            fit_model=PCHIP_MODEL,
            expected_y_monotonic="nondecreasing",
            residual_abs_tolerance=1.0e-9,
            residual_percent_tolerance=1.0e-9,
            out_of_range="raise",
        )

        self.assertTrue(report.passed)
        self.assertEqual(report.point_count, len(self.points))
        self.assertAlmostEqual(report.max_abs_residual, 0.0)
        self.assertTrue(report.monotonic_x_check.passed)
        self.assertTrue(report.monotonic_y_check.passed)
        self.assertEqual(
            report.review_status_counts,
            {"draft_extraction": len(self.points)},
        )

    def test_validation_output_is_serializable_for_reports_and_exports(self):
        report = validate_curve_fit(
            self.points,
            expected_y_monotonic="nondecreasing",
            out_of_range="raise",
        )
        payload = report.to_dict()
        markdown = report.to_markdown_section()

        self.assertEqual(payload["human_review_required"], HUMAN_REVIEW_NOTE)
        self.assertEqual(payload["lookup_domain"]["out_of_range_policy"], "raise")
        self.assertEqual(payload["fit_model"], PCHIP_MODEL)
        self.assertIn("Curve Fit Validation", markdown)
        self.assertIn("Human Review Required", markdown)

    def test_linear_fit_validation_is_available(self):
        report = validate_curve_fit(
            self.points,
            fit_model=LINEAR_MODEL,
            expected_y_monotonic="nondecreasing",
        )

        self.assertEqual(report.fit_model, LINEAR_MODEL)
        self.assertTrue(report.passed)
        self.assertAlmostEqual(report.rms_residual, 0.0)

    def test_monotonicity_check_detects_y_direction_violation(self):
        points = [
            EngineeringPoint("p1", 10.0, 30.0, 1.0, 10.0),
            EngineeringPoint("p2", 20.0, 20.0, 2.0, 15.0),
            EngineeringPoint("p3", 30.0, 10.0, 3.0, 14.0),
        ]

        report = validate_curve_fit(
            points,
            expected_y_monotonic="nondecreasing",
        )

        self.assertFalse(report.passed)
        self.assertFalse(report.monotonic_y_check.passed)
        self.assertEqual(report.monotonic_y_check.first_violation_index, 2)
        self.assertIn("nondecreasing", report.warnings[0])

    def test_check_monotonicity_supports_nonincreasing_sequences(self):
        check = check_monotonicity([10.0, 8.0, 8.0, 4.0], "nonincreasing")

        self.assertTrue(check.passed)
        self.assertEqual(check.violation_count, 0)

    def test_calculate_residuals_uses_fitted_minus_observed_convention(self):
        residuals = calculate_residuals(
            self.points[:2],
            evaluator=lambda x_value: 125.0 if x_value == self.points[0].x else 250.0,
        )

        self.assertEqual(len(residuals), 2)
        self.assertAlmostEqual(residuals[0].residual, 125.0 - self.points[0].y)
        self.assertAlmostEqual(residuals[1].fitted_y, 250.0)

    def test_invalid_inputs_fail_clearly(self):
        duplicate_x_points = [
            EngineeringPoint("p1", 10.0, 20.0, 1.0, 100.0),
            EngineeringPoint("p2", 11.0, 19.0, 1.0, 110.0),
        ]

        with self.assertRaises(ValueError):
            validate_curve_fit(duplicate_x_points)
        with self.assertRaises(ValueError):
            validate_curve_fit(self.points, fit_model="polynomial")
        with self.assertRaises(ValueError):
            check_monotonicity([1.0, 2.0], "flat")
        with self.assertRaises(ValueError):
            validate_curve_fit(self.points, residual_abs_tolerance=-1.0)


if __name__ == "__main__":
    unittest.main()
