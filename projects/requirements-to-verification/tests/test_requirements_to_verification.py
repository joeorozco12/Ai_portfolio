import csv
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_DIR.parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from requirements_to_verification.core import (  # noqa: E402
    REQUIRED_COLUMNS,
    build_artifacts,
    load_requirements,
    write_outputs,
)


class RequirementsToVerificationTests(unittest.TestCase):
    def test_csv_input_can_be_loaded(self):
        result = load_requirements(REPO_ROOT / "Synthetic Requirements Sample.csv")

        self.assertEqual(len(result.rows), 12)
        self.assertEqual(result.rows[0]["Requirement_ID"], "SYN-REQ-001")
        self.assertFalse(result.warnings)

    def test_required_columns_are_enforced(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing_columns.csv"
            path.write_text("Requirement_ID,Requirement_Text\nSYN-REQ-BAD,Missing schema\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                load_requirements(path)

        self.assertIn("missing required columns", str(context.exception))
        self.assertIn("Verification_Method", str(context.exception))

    def test_trace_matrix_output_is_generated(self):
        rows = load_requirements(REPO_ROOT / "Synthetic Requirements Sample.csv").rows
        bundle = build_artifacts(rows)

        self.assertEqual(len(bundle.trace_matrix), len(rows))
        first_row = bundle.trace_matrix[0]
        self.assertEqual(first_row["Requirement_ID"], "SYN-REQ-001")
        self.assertEqual(first_row["Detected_Domain_Category"], "Power Input / Electrical")
        self.assertIn("test", first_row["Verification_Method"])
        self.assertIn("9.0 V to 16.0 V", first_row["Acceptance_Criteria"])

    def test_ambiguity_report_flags_known_weak_terms(self):
        rows = load_requirements(PROJECT_DIR / "fixtures" / "ambiguous_requirements_fixture.csv").rows
        bundle = build_artifacts(rows)
        triggers = {finding["Trigger"].lower() for finding in bundle.ambiguity_report}

        self.assertIn("should", triggers)
        self.assertIn("adequate", triggers)
        self.assertIn("as needed", triggers)
        self.assertIn("tbd", triggers)
        self.assertIn("where appropriate", triggers)

    def test_assumptions_register_links_back_to_requirement_ids(self):
        rows = load_requirements(REPO_ROOT / "Synthetic Requirements Sample.csv").rows
        bundle = build_artifacts(rows)
        source_ids = {row["Requirement_ID"] for row in rows}
        linked_ids = {row["Linked_Requirement_ID"] for row in bundle.assumptions_register}

        self.assertTrue(bundle.assumptions_register)
        self.assertTrue(linked_ids)
        self.assertTrue(linked_ids.issubset(source_ids))

    def test_review_checklist_output_exists(self):
        rows = load_requirements(REPO_ROOT / "Synthetic Requirements Sample.csv").rows
        bundle = build_artifacts(rows)

        self.assertEqual(len(bundle.review_checklist), 8)
        areas = {row["Review_Area"] for row in bundle.review_checklist}
        self.assertIn("Traceability", areas)
        self.assertIn("Human review signoff", areas)

    def test_writes_csv_and_markdown_outputs(self):
        rows = load_requirements(REPO_ROOT / "Synthetic Requirements Sample.csv").rows
        bundle = build_artifacts(rows)

        with tempfile.TemporaryDirectory() as temp_dir:
            paths = write_outputs(Path(temp_dir), bundle)

            self.assertTrue(paths["trace_matrix_csv"].exists())
            self.assertTrue(paths["ambiguity_report_md"].exists())
            self.assertTrue(paths["assumptions_register_csv"].exists())
            self.assertTrue(paths["review_checklist_md"].exists())

            with paths["trace_matrix_csv"].open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames[0], "Synthetic_Label")
                self.assertIn("Reviewer_Notes", reader.fieldnames)

    def test_required_column_constant_matches_fixture_schema(self):
        fixture_header = (
            PROJECT_DIR / "fixtures" / "ambiguous_requirements_fixture.csv"
        ).read_text(encoding="utf-8").splitlines()[0]

        for column in REQUIRED_COLUMNS:
            self.assertIn(column, fixture_header)


if __name__ == "__main__":
    unittest.main()
