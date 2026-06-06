import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.demo_data import (
    DEMO_PROJECT_SPECS,
    available_demo_project_ids,
    build_all_demo_projects,
    build_demo_project,
    write_demo_assets,
)
from led_digitizer.models import HUMAN_REVIEW_NOTE, SYNTHETIC_LABEL
from led_digitizer.project_io import load_project


EXPECTED_PROJECT_IDS = {
    "synthetic_forward_voltage_vs_forward_current",
    "synthetic_junction_temperature_vs_relative_luminous_flux",
    "synthetic_forward_current_vs_relative_luminous_flux",
    "synthetic_thermal_derating_curve",
}

PROHIBITED_SYNTHETIC_FRAGMENTS = {
    "/Users/",
    "theresaorozco",
    "ticket_",
    "program_",
    "schematic_",
    "harness_",
    "bom_",
}


class DemoDataTests(unittest.TestCase):
    def test_catalog_contains_required_led_curve_workflows(self):
        self.assertEqual(set(available_demo_project_ids()), EXPECTED_PROJECT_IDS)
        self.assertEqual(len(DEMO_PROJECT_SPECS), 4)

        curve_names = {
            build_demo_project(project_id).curves[0].curve_name
            for project_id in available_demo_project_ids()
        }

        self.assertEqual(
            curve_names,
            {
                "Forward Voltage vs Forward Current",
                "Junction Temperature vs Relative Luminous Flux",
                "Forward Current vs Relative Luminous Flux",
                "Thermal Derating Style Curve",
            },
        )

    def test_demo_projects_include_source_metadata_and_review_boundaries(self):
        for project in build_all_demo_projects():
            with self.subTest(project_id=project.metadata.project_id):
                self.assertEqual(project.synthetic_label, SYNTHETIC_LABEL)
                self.assertEqual(project.human_review_required, HUMAN_REVIEW_NOTE)
                self.assertEqual(project.metadata.publication_classification, "Safe to publish")
                self.assertEqual(project.source.source_category, "synthetic")
                self.assertEqual(project.source.manufacturer, "Synthetic LED Supplier")
                self.assertTrue(project.source.source_page.startswith("synthetic_page_"))
                self.assertEqual(project.review_status, "pending_engineering_review")
                self.assertIn("engineer review", " ".join(project.assumptions).lower())
                self.assertEqual(len(project.curves), 1)
                self.assertGreaterEqual(len(project.curves[0].points), 5)
                self.assertEqual(
                    project.curves[0].review_status,
                    "pending_engineering_review",
                )

    def test_demo_points_preserve_source_pixels_and_engineering_units(self):
        project = build_demo_project("synthetic_forward_voltage_vs_forward_current")
        curve = project.curves[0]
        first_point = curve.points[0]
        last_point = curve.points[-1]

        self.assertEqual(curve.x_axis_label, "Forward Current")
        self.assertEqual(curve.y_axis_label, "Forward Voltage")
        self.assertAlmostEqual(first_point.x, 0.0)
        self.assertAlmostEqual(first_point.source_pixel_x, 80.0)
        self.assertAlmostEqual(last_point.x, 1500.0)
        self.assertAlmostEqual(last_point.source_pixel_x, 560.0)
        self.assertEqual(first_point.review_status, "synthetic_demo_pending_review")

    def test_write_demo_assets_saves_loadable_project_files_and_point_tables(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output = write_demo_assets(
                synthetic_data_dir=temp_path / "synthetic",
                demo_projects_dir=temp_path / "demo_projects",
            )

            self.assertEqual(len(output["demo_project_files"]), 4)
            self.assertEqual(len(output["synthetic_point_tables"]), 4)

            for project_path in output["demo_project_files"]:
                loaded = load_project(project_path)
                payload = json.loads(project_path.read_text(encoding="utf-8"))
                self.assertEqual(payload["synthetic_label"], SYNTHETIC_LABEL)
                self.assertEqual(payload["human_review_required"], HUMAN_REVIEW_NOTE)
                self.assertEqual(loaded.review_status, "pending_engineering_review")

            for csv_path in output["synthetic_point_tables"]:
                with csv_path.open(newline="", encoding="utf-8") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertGreaterEqual(len(rows), 5)
                self.assertEqual(rows[0]["synthetic_label"], SYNTHETIC_LABEL)
                self.assertEqual(rows[0]["human_review_required"], HUMAN_REVIEW_NOTE)
                self.assertEqual(rows[0]["publication_classification"], "Safe to publish")

    def test_generated_payloads_do_not_include_obvious_private_identifiers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output = write_demo_assets(
                synthetic_data_dir=temp_path / "synthetic",
                demo_projects_dir=temp_path / "demo_projects",
            )

            generated_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in [
                    *output["demo_project_files"],
                    *output["synthetic_point_tables"],
                ]
            ).lower()

        for fragment in PROHIBITED_SYNTHETIC_FRAGMENTS:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment.lower(), generated_text)


if __name__ == "__main__":
    unittest.main()
