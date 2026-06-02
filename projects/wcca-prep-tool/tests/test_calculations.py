import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wcca_prep.calculations import (
    OperatingCondition,
    WccaCase,
    calculate_case_condition,
)


class CalculationEngineTests(unittest.TestCase):
    def test_buck_lowline_stress_is_deterministic(self):
        case = WccaCase(
            case_id="SYN-WCCA-TEST",
            topology="Buck LED Driver",
            vin_min_v=9.0,
            vin_nom_v=13.5,
            vin_max_v=16.0,
            led_string_vf_nom_v=6.4,
            led_string_vf_tol_pct=3.0,
            led_current_a=0.70,
            ambient_temp_c=85.0,
            efficiency_assumption=0.88,
            efficiency_tol_pct=3.0,
            current_tol_pct=5.0,
            sense_res_tol_pct=1.0,
            switch_current_rating_a=1.5,
            input_voltage_rating_v=40.0,
            inductor_current_rating_a=1.4,
            thermal_rise_c_per_w=18.0,
            max_junction_temp_c=150.0,
        )
        condition = OperatingCondition(
            condition_id="SYN-OC-TEST",
            description="Synthetic low-line test",
            vin_v=9.0,
            ambient_temp_c=105.0,
            load_current_factor=1.0,
        )

        result = calculate_case_condition(case, condition)

        self.assertAlmostEqual(result.led_current_high_a, 0.742, places=3)
        self.assertAlmostEqual(result.led_vf_high_v, 6.592, places=3)
        self.assertAlmostEqual(result.output_power_w, 4.891, places=3)
        self.assertAlmostEqual(result.switch_current_stress_a, 0.816, places=3)
        self.assertEqual(result.review_status, "Review required")

    def test_over_limit_status_when_current_ratio_exceeds_rating(self):
        case = WccaCase(
            case_id="SYN-WCCA-TEST",
            topology="SEPIC LED Driver",
            vin_min_v=9.0,
            vin_nom_v=13.5,
            vin_max_v=16.0,
            led_string_vf_nom_v=13.2,
            led_string_vf_tol_pct=4.0,
            led_current_a=1.00,
            ambient_temp_c=105.0,
            efficiency_assumption=0.84,
            efficiency_tol_pct=5.0,
            current_tol_pct=5.0,
            sense_res_tol_pct=1.0,
            switch_current_rating_a=2.5,
            input_voltage_rating_v=40.0,
            inductor_current_rating_a=2.2,
            thermal_rise_c_per_w=24.0,
            max_junction_temp_c=150.0,
        )
        condition = OperatingCondition(
            condition_id="SYN-OC-TEST",
            description="Synthetic hot corner",
            vin_v=9.0,
            ambient_temp_c=105.0,
            load_current_factor=1.0,
        )

        result = calculate_case_condition(case, condition)

        self.assertGreater(result.switch_current_ratio, 1.0)
        self.assertEqual(result.review_status, "Over synthetic limit")

    def test_linear_channel_has_no_inductor_ratio(self):
        case = WccaCase(
            case_id="SYN-WCCA-TEST",
            topology="Linear LED Channel",
            vin_min_v=9.0,
            vin_nom_v=13.5,
            vin_max_v=16.0,
            led_string_vf_nom_v=10.5,
            led_string_vf_tol_pct=3.0,
            led_current_a=0.35,
            ambient_temp_c=85.0,
            efficiency_assumption=0.75,
            efficiency_tol_pct=0.0,
            current_tol_pct=5.0,
            sense_res_tol_pct=1.0,
            switch_current_rating_a=0.8,
            input_voltage_rating_v=24.0,
            inductor_current_rating_a=None,
            thermal_rise_c_per_w=32.0,
            max_junction_temp_c=150.0,
        )
        condition = OperatingCondition(
            condition_id="SYN-OC-TEST",
            description="Synthetic nominal test",
            vin_v=13.5,
            ambient_temp_c=85.0,
            load_current_factor=1.0,
        )

        result = calculate_case_condition(case, condition)

        self.assertIsNone(result.inductor_current_stress_a)
        self.assertIsNone(result.inductor_current_ratio)
        self.assertIsNotNone(result.thermal_ratio)


if __name__ == "__main__":
    unittest.main()
