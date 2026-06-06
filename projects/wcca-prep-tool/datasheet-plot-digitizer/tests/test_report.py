import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.report import (
    HUMAN_REVIEW_NOTE,
    SYNTHETIC_LABEL,
    build_report_context,
    write_markdown_report,
)
from led_digitizer.sample_project import SAMPLE_METADATA, load_sample_points


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.points = load_sample_points(PROJECT_ROOT / "data" / "synthetic_manual_points.csv")

    def test_report_context_includes_task5_review_fields(self):
        context = build_report_context(
            SAMPLE_METADATA,
            self.points,
            {
                "csv_points": "data/digitized_curve_points.csv",
                "json_metadata": "metadata/export_manifest.json",
                "overlay_png": "review/overlay_forward_voltage_vs_forward_current.png",
            },
        )

        self.assertEqual(context["synthetic_label"], SYNTHETIC_LABEL)
        self.assertEqual(context["human_review_required"], HUMAN_REVIEW_NOTE)
        self.assertEqual(context["source_metadata"]["source_category"], "synthetic")
        self.assertEqual(
            context["calibration_metadata"]["x_axis"]["scale"],
            "linear",
        )
        self.assertIn("assumptions", context)
        self.assertIn("method", context)
        self.assertEqual(
            context["fit_model"]["model_name"],
            "pchip_shape_preserving_interpolation",
        )
        self.assertEqual(
            context["validation_status"]["status"],
            "draft_validation_pending_engineer_review",
        )
        self.assertEqual(context["review_status"]["status"], "draft_extraction")
        self.assertTrue(context["downstream_use_warnings"])

    def test_markdown_report_contains_review_package_sections(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "extraction_report.md"

            write_markdown_report(
                report_path,
                SAMPLE_METADATA,
                self.points,
                overlay_path="review/overlay_forward_voltage_vs_forward_current.png",
                csv_path="data/digitized_curve_points.csv",
                json_path="metadata/export_manifest.json",
                python_path="lookups/python/lookup_forward_voltage_vs_forward_current.py",
                matlab_path="lookups/matlab/lookup_forward_voltage_vs_forward_current.m",
                source_metadata_path="metadata/source_metadata.json",
                calibration_metadata_path="metadata/calibration_metadata.json",
            )
            text = report_path.read_text(encoding="utf-8")

            self.assertIn(SYNTHETIC_LABEL, text)
            self.assertIn(HUMAN_REVIEW_NOTE, text)
            self.assertIn("## Source Metadata", text)
            self.assertIn("## Calibration Metadata", text)
            self.assertIn("## Assumptions", text)
            self.assertIn("## Method", text)
            self.assertIn("## Fit Model", text)
            self.assertIn("## Validation Status", text)
            self.assertIn("## Review Status", text)
            self.assertIn("## Downstream Use Warnings", text)
            self.assertIn("metadata/source_metadata.json", text)
            self.assertIn("metadata/calibration_metadata.json", text)
            self.assertIn("The tool does not approve LED design values.", text)
            self.assertIn("## Safe To Publish Status", text)


if __name__ == "__main__":
    unittest.main()
