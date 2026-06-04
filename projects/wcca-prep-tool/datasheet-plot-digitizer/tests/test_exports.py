import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.exports import (
    HUMAN_REVIEW_NOTE,
    SYNTHETIC_LABEL,
    safe_name,
    write_markdown_report,
    write_metadata_json,
    write_overlay_png,
    write_points_csv,
    write_python_lookup,
)
from led_digitizer.sample_project import SAMPLE_METADATA, load_sample_points


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.points = load_sample_points(PROJECT_ROOT / "data" / "synthetic_manual_points.csv")

    def test_safe_name_returns_function_safe_slug(self):
        self.assertEqual(
            safe_name("Forward Voltage vs Forward Current"),
            "forward_voltage_vs_forward_current",
        )

    def test_csv_and_json_include_review_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            csv_path = temp_root / "points.csv"
            json_path = temp_root / "metadata.json"

            write_points_csv(csv_path, SAMPLE_METADATA, self.points)
            write_metadata_json(json_path, SAMPLE_METADATA)

            with csv_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            metadata = json.loads(json_path.read_text(encoding="utf-8"))

            self.assertEqual(len(rows), len(self.points))
            self.assertEqual(rows[0]["review_status"], "draft_extraction")
            self.assertEqual(metadata["synthetic_label"], SYNTHETIC_LABEL)
            self.assertEqual(metadata["human_review_required"], HUMAN_REVIEW_NOTE)

    def test_overlay_png_has_png_signature(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "overlay.png"

            write_overlay_png(path, self.points)

            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_python_lookup_exports_callable_function(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "lookup_forward_voltage_vs_forward_current.py"

            write_python_lookup(
                path,
                "lookup_forward_voltage_vs_forward_current",
                SAMPLE_METADATA,
                self.points,
            )
            namespace = {}
            exec(path.read_text(encoding="utf-8"), namespace)

            value = namespace["lookup_forward_voltage_vs_forward_current"](3.25)
            self.assertAlmostEqual(value, 1000.0)

    def test_report_contains_required_publication_controls(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "report.md"

            write_markdown_report(
                path,
                SAMPLE_METADATA,
                self.points,
                overlay_path="overlay.png",
                csv_path="points.csv",
                json_path="metadata.json",
                python_path="lookup.py",
                matlab_path="lookup.m",
            )
            text = path.read_text(encoding="utf-8")

            self.assertIn(SYNTHETIC_LABEL, text)
            self.assertIn(HUMAN_REVIEW_NOTE, text)
            self.assertIn("## Proof Gaps", text)
            self.assertIn("## Safe To Publish Status", text)


if __name__ == "__main__":
    unittest.main()
