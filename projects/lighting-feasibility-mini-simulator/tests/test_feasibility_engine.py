import csv
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from feasibility_engine import (  # noqa: E402
    FAIL_STATUS,
    MARGINAL_STATUS,
    PASS_STATUS,
    SENSITIVITY_FIELDNAMES,
    FeasibilityCase,
    calculate_case,
    load_cases,
    run_from_csv,
    run_sensitivity_sweeps,
    write_csv_summary,
    write_sensitivity_outputs,
)


class FeasibilityEngineTests(unittest.TestCase):
    def test_buck_case_calculates_core_equations_and_passes(self):
        case = FeasibilityCase(
            case_id="SYN-LGT-UNIT-PASS",
            load_name="Synthetic two-LED unit case",
            driver_topology="Buck LED Driver",
            led_count=2,
            led_forward_voltage_nom_v=3.0,
            led_vf_tol_pct=5.0,
            led_current_nom_a=0.35,
            current_tol_pct=5.0,
            duty_cycle=0.80,
            supply_min_v=9.0,
            supply_max_v=16.0,
            driver_dropout_v=1.0,
            driver_efficiency=0.90,
            efficiency_tol_pct=3.0,
            max_input_current_a=1.20,
            max_input_voltage_v=40.0,
            max_output_power_w=8.0,
            board_thermal_resistance_c_per_w=18.0,
            max_driver_case_temp_c=125.0,
            led_thermal_resistance_c_per_w=25.0,
            max_led_junction_temp_c=135.0,
            ambient_temp_c=85.0,
            max_boost_duty_cycle=0.85,
        )

        result = calculate_case(case)

        self.assertAlmostEqual(result.led_string_vf_high_v, 6.300, places=3)
        self.assertAlmostEqual(result.led_current_high_a, 0.3675, places=4)
        self.assertAlmostEqual(result.output_power_w, 1.852, places=3)
        self.assertAlmostEqual(result.input_current_at_min_v, 0.236, places=3)
        self.assertAlmostEqual(result.voltage_headroom_v, 1.700, places=3)
        self.assertAlmostEqual(result.led_junction_temp_c, 108.1525, places=4)
        self.assertEqual(result.status, PASS_STATUS)

    def test_low_voltage_headroom_is_marginal(self):
        case = FeasibilityCase(
            case_id="SYN-LGT-UNIT-MARGINAL",
            load_name="Synthetic headroom unit case",
            driver_topology="Buck LED Driver",
            led_count=3,
            led_forward_voltage_nom_v=2.7,
            led_vf_tol_pct=5.0,
            led_current_nom_a=0.25,
            current_tol_pct=5.0,
            duty_cycle=1.00,
            supply_min_v=9.0,
            supply_max_v=16.0,
            driver_dropout_v=0.3,
            driver_efficiency=0.90,
            efficiency_tol_pct=3.0,
            max_input_current_a=0.80,
            max_input_voltage_v=40.0,
            max_output_power_w=4.0,
            board_thermal_resistance_c_per_w=18.0,
            max_driver_case_temp_c=125.0,
            led_thermal_resistance_c_per_w=20.0,
            max_led_junction_temp_c=135.0,
            ambient_temp_c=85.0,
            max_boost_duty_cycle=0.85,
        )

        result = calculate_case(case)

        self.assertAlmostEqual(result.voltage_headroom_v, 0.195, places=3)
        self.assertEqual(result.status, MARGINAL_STATUS)
        self.assertIn("voltage headroom", result.reason)

    def test_exact_ratio_marginal_threshold_is_marginal(self):
        case = FeasibilityCase(
            case_id="SYN-LGT-UNIT-RATIO-MARGINAL",
            load_name="Synthetic exact threshold unit case",
            driver_topology="Linear LED Channel",
            led_count=1,
            led_forward_voltage_nom_v=2.0,
            led_vf_tol_pct=0.0,
            led_current_nom_a=0.85,
            current_tol_pct=0.0,
            duty_cycle=1.00,
            supply_min_v=12.0,
            supply_max_v=14.0,
            driver_dropout_v=1.0,
            driver_efficiency=1.00,
            efficiency_tol_pct=0.0,
            max_input_current_a=1.00,
            max_input_voltage_v=40.0,
            max_output_power_w=8.0,
            board_thermal_resistance_c_per_w=2.0,
            max_driver_case_temp_c=125.0,
            led_thermal_resistance_c_per_w=10.0,
            max_led_junction_temp_c=135.0,
            ambient_temp_c=40.0,
            max_boost_duty_cycle=0.85,
        )

        result = calculate_case(case)

        self.assertAlmostEqual(result.input_current_ratio, 0.85, places=6)
        self.assertEqual(result.status, MARGINAL_STATUS)
        self.assertIn("input current ratio", result.reason)

    def test_boost_case_fails_when_duty_exceeds_synthetic_limit(self):
        case = FeasibilityCase(
            case_id="SYN-LGT-UNIT-FAIL",
            load_name="Synthetic boost duty unit case",
            driver_topology="Boost LED Driver",
            led_count=7,
            led_forward_voltage_nom_v=3.0,
            led_vf_tol_pct=5.0,
            led_current_nom_a=0.50,
            current_tol_pct=5.0,
            duty_cycle=1.00,
            supply_min_v=9.0,
            supply_max_v=16.0,
            driver_dropout_v=0.0,
            driver_efficiency=0.85,
            efficiency_tol_pct=5.0,
            max_input_current_a=1.60,
            max_input_voltage_v=40.0,
            max_output_power_w=13.0,
            board_thermal_resistance_c_per_w=10.0,
            max_driver_case_temp_c=125.0,
            led_thermal_resistance_c_per_w=20.0,
            max_led_junction_temp_c=135.0,
            ambient_temp_c=95.0,
            max_boost_duty_cycle=0.62,
        )

        result = calculate_case(case)

        self.assertAlmostEqual(result.boost_duty_cycle, 0.670, places=3)
        self.assertEqual(result.status, FAIL_STATUS)
        self.assertIn("boost duty", result.reason)

    def test_sample_csv_loads_and_produces_all_statuses(self):
        bundle = run_from_csv(PROJECT_DIR / "data" / "synthetic_lighting_cases.csv")
        statuses = {result.status for result in bundle.results}

        self.assertEqual(len(bundle.cases), 5)
        self.assertFalse(bundle.warnings)
        self.assertIn(PASS_STATUS, statuses)
        self.assertIn(MARGINAL_STATUS, statuses)
        self.assertIn(FAIL_STATUS, statuses)

    def test_invalid_numeric_input_is_skipped_with_warning(self):
        csv_text = (
            "Case_ID,Load_Name,Driver_Topology,LED_Count,LED_Forward_Voltage_Nom_V,"
            "LED_VF_Tol_pct,LED_Current_Nom_A,Current_Tol_pct,Duty_Cycle,VSupply_Min_V,"
            "VSupply_Max_V,Driver_Dropout_V,Driver_Efficiency,Efficiency_Tol_pct,"
            "Max_Input_Current_A,Max_Input_Voltage_V,Max_Output_Power_W,"
            "Board_Thermal_Resistance_C_per_W,Max_Driver_Case_Temp_C,"
            "LED_Thermal_Resistance_C_per_W,Max_LED_Junction_Temp_C,Ambient_Temp_C,"
            "Max_Boost_Duty_Cycle\n"
            "SYN-BAD,Synthetic invalid row,Buck LED Driver,not-a-number,3.0,5,0.35,5,"
            "0.8,9,16,1,0.9,3,1.2,40,8,18,125,25,135,85,0.85\n"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad.csv"
            path.write_text(csv_text, encoding="utf-8")

            cases, warnings = load_cases(path)

        self.assertEqual(cases, [])
        self.assertTrue(any("invalid numeric value" in warning for warning in warnings))
        self.assertTrue(any("row skipped" in warning for warning in warnings))

    def test_csv_output_schema(self):
        bundle = run_from_csv(PROJECT_DIR / "data" / "synthetic_lighting_cases.csv")
        expected_columns = [
            "Synthetic_Label",
            "Human_Review_Note",
            "Publication_Classification",
            "Case_ID",
            "Load_Name",
            "Driver_Topology",
            "Output_Power_W",
            "Input_Current_at_Min_V_A",
            "Voltage_Headroom_V",
            "Boost_Duty_Cycle",
            "Driver_Case_Temp_C",
            "LED_Junction_Temp_C",
            "Max_Ratio",
            "Status",
            "Reason",
            "Recommended_Next_Step",
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "summary.csv"
            write_csv_summary(path, bundle.results)

            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)

        self.assertEqual(reader.fieldnames, expected_columns)
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["Synthetic_Label"], "[SYNTHETIC — FOR DEMONSTRATION ONLY]")
        self.assertEqual(rows[0]["Publication_Classification"], "Needs review")

    def test_sensitivity_csv_files_are_generated(self):
        bundle = run_from_csv(PROJECT_DIR / "data" / "synthetic_lighting_cases.csv")
        rows = run_sensitivity_sweeps(bundle.cases)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sensitivity"
            write_sensitivity_outputs(output_dir, rows)

            expected_files = [
                "sensitivity_summary.md",
                "sensitivity_summary.csv",
                "ambient_temperature_sweep.csv",
                "led_current_sweep.csv",
                "thermal_resistance_sweep.csv",
                "optical_efficiency_sweep.csv",
                "plots/ambient_temperature_sweep.png",
                "plots/led_current_sweep.png",
                "plots/thermal_resistance_sweep.png",
                "plots/optical_efficiency_sweep.png",
            ]
            for filename in expected_files:
                self.assertTrue((output_dir / filename).exists(), filename)

        self.assertEqual(len(rows), 100)

    def test_sensitivity_schema_is_stable(self):
        bundle = run_from_csv(PROJECT_DIR / "data" / "synthetic_lighting_cases.csv")
        rows = run_sensitivity_sweeps(bundle.cases)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sensitivity"
            write_sensitivity_outputs(output_dir, rows)

            with (output_dir / "sensitivity_summary.csv").open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                csv_rows = list(reader)

        self.assertEqual(reader.fieldnames, SENSITIVITY_FIELDNAMES)
        self.assertEqual(len(csv_rows), 100)
        self.assertEqual(csv_rows[0]["Engineering_Review_Required"], "Yes - synthetic thresholds require qualified engineering review.")

    def test_sensitivity_sweep_produces_status_variation(self):
        bundle = run_from_csv(PROJECT_DIR / "data" / "synthetic_lighting_cases.csv")
        rows = run_sensitivity_sweeps(bundle.cases)
        ambient_statuses = {
            row.sweep_status
            for row in rows
            if row.sweep_name == "ambient_temperature_sweep"
        }

        self.assertGreaterEqual(len(ambient_statuses), 2)
        self.assertIn(PASS_STATUS, {row.sweep_status for row in rows})
        self.assertIn(MARGINAL_STATUS, {row.sweep_status for row in rows})
        self.assertIn(FAIL_STATUS, {row.sweep_status for row in rows})


if __name__ == "__main__":
    unittest.main()
