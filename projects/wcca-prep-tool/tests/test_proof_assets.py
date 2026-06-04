import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wcca_prep.calculations import calculate_wcca
from wcca_prep.captures import write_capture_files
from wcca_prep.loaders import load_operating_conditions, load_wcca_cases
from wcca_prep.plots import write_plot_gallery
from wcca_prep.report import write_report, write_warnings
from wcca_prep.summary import (
    pass_fail_status,
    result_margin_pct,
    write_summary_csv,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ProofAssetTests(unittest.TestCase):
    def _load_bundle(self):
        case_load = load_wcca_cases(PROJECT_ROOT / "data" / "synthetic_wcca_cases.csv")
        condition_load = load_operating_conditions(PROJECT_ROOT / "data" / "operating_conditions.csv")
        bundle = calculate_wcca(case_load.rows, condition_load.rows)
        warnings = [*case_load.warnings, *condition_load.warnings, *bundle.warnings]
        return case_load, condition_load, bundle, warnings

    def test_at_least_15_synthetic_cases_load(self):
        case_load, condition_load, bundle, _ = self._load_bundle()

        self.assertGreaterEqual(len(case_load.rows), 15)
        self.assertEqual(len(condition_load.rows), 4)
        self.assertEqual(len(bundle.results), len(case_load.rows) * len(condition_load.rows))

    def test_margin_and_pass_fail_status_are_deterministic(self):
        _, _, bundle, _ = self._load_bundle()
        target = next(
            result
            for result in bundle.results
            if result.case_id == "SYN-WCCA-001" and result.condition_id == "SYN-OC-LOWLINE-HOT"
        )
        over_limit = next(result for result in bundle.results if result.review_status == "Over synthetic limit")

        self.assertAlmostEqual(result_margin_pct(target), 19.93, places=2)
        self.assertEqual(pass_fail_status(target), "Review")
        self.assertEqual(pass_fail_status(over_limit), "Fail")

    def test_generated_proof_outputs_exist(self):
        case_load, condition_load, bundle, warnings = self._load_bundle()
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp)
            report_path = output_root / "synthetic_wcca_report.md"
            summary_path = output_root / "synthetic_wcca_summary.csv"
            warnings_path = output_root / "missing_data_warnings.md"
            plots_dir = output_root / "plots"
            captures_dir = output_root / "captures"

            write_report(
                report_path,
                bundle.results,
                warnings,
                len(case_load.rows),
                len(condition_load.rows),
            )
            write_summary_csv(summary_path, bundle.results)
            write_warnings(warnings_path, warnings)
            plot_paths = write_plot_gallery(plots_dir, bundle.results)
            capture_paths = write_capture_files(
                captures_dir,
                bundle.results,
                warnings,
                plot_paths,
                summary_path,
                report_path,
            )

            for path in [report_path, summary_path, warnings_path, *plot_paths, *capture_paths]:
                self.assertTrue(path.exists(), path)
                self.assertGreater(path.stat().st_size, 0, path)
            self.assertGreaterEqual(len(plot_paths), 5)
            self.assertGreaterEqual(len(capture_paths), 5)
            for plot_path in plot_paths:
                self.assertEqual(plot_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_equation_checklist_exists(self):
        checklist_path = PROJECT_ROOT / "docs" / "equation_review_checklist.md"
        checklist = checklist_path.read_text(encoding="utf-8")

        self.assertIn("Ohm's law current estimate", checklist)
        self.assertIn("Junction temperature estimate", checklist)
        self.assertIn("Percent margin calculation", checklist)
        self.assertIn("Review Status", checklist)


if __name__ == "__main__":
    unittest.main()
