from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPO_ROOT / "tools" / "generate_ux_console_data.py"
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_ux_console_review.py"
REVIEW_LOG_PATH = REPO_ROOT / "ux-console" / "review" / "review_log.csv"
CONSOLE_DATA_PATH = REPO_ROOT / "ux-console" / "data" / "portfolio_workflows.js"
SCREENSHOT_INDEX_PATH = REPO_ROOT / "Screenshot Index.md"
DEPLOYMENT_NOTES_PATH = REPO_ROOT / "ux-console" / "DEPLOYMENT.md"
CONSOLE_SCREENSHOTS = [
    "ux-console/screenshots/portfolio_overview.png",
    "ux-console/screenshots/project1_requirements_to_verification.png",
    "ux-console/screenshots/project2_wcca_prep.png",
    "ux-console/screenshots/project4_design_review_readiness.png",
    "ux-console/screenshots/project5_lighting_feasibility.png",
    "ux-console/screenshots/mobile_project5_lighting_feasibility.png",
]
PUBLIC_ROUTE_FILES = [
    ("ux-console/tools/index.html", "#tools"),
    ("ux-console/tools/requirements/index.html", "#tools/requirements"),
    ("ux-console/tools/feasibility/index.html", "#tools/feasibility"),
    ("ux-console/tools/wcca/index.html", "#tools/wcca"),
    ("ux-console/tools/design-review/index.html", "#tools/design-review"),
    ("ux-console/tools/evidence/index.html", "#tools/evidence"),
]


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_ux_console_data", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ux_console_review", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class UXConsoleDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()
        cls.validator = load_validator()
        cls.payload = cls.generator.build_portfolio_workflows()

    def test_includes_four_project_workflows(self):
        project_ids = {project["project_id"] for project in self.payload["projects"]}

        self.assertEqual(
            project_ids,
            {
                "requirements-to-verification",
                "wcca-prep",
                "design-review-readiness",
                "lighting-feasibility",
            },
        )

    def test_each_project_preserves_publication_safety_contract(self):
        for project in self.payload["projects"]:
            with self.subTest(project=project["project_id"]):
                self.assertEqual(project["synthetic_label"], self.generator.SYNTHETIC_LABEL)
                self.assertIn("Human Review Required", project["human_review_note"])
                self.assertEqual(project["publication_classification"], "Needs review")
                self.assertTrue(project["route"].startswith("#"))
                self.assertTrue(project["review_items"])
                self.assertTrue(project["artifacts"])
                self.assertTrue(project["proof_screens"])

    def test_safe_to_publish_gate_stays_needs_review(self):
        for project in self.payload["projects"]:
            states = {check["state"] for check in project["safe_to_publish_checks"]}
            with self.subTest(project=project["project_id"]):
                self.assertIn("Needs review", states)
                self.assertNotIn("Safe to publish", states)

    def test_reviewer_decisions_remain_separate_from_generated_outputs(self):
        self.assertIn("separately", self.payload["review_log_policy"])
        for project in self.payload["projects"]:
            with self.subTest(project=project["project_id"]):
                boundary = project["project_boundary"].lower()
                self.assertTrue("review" in boundary or "approval" in boundary or "approve" in boundary)
                self.assertNotIn("approval", project["publication_classification"].lower())

    def test_project_specific_proof_screens_are_present(self):
        proof_screens = {
            project["project_id"]: set(project["proof_screens"])
            for project in self.payload["projects"]
        }

        self.assertIn("Ambiguity triage", proof_screens["requirements-to-verification"])
        self.assertIn("Equation review checklist", proof_screens["wcca-prep"])
        self.assertIn("Risk register", proof_screens["design-review-readiness"])
        self.assertIn("Sensitivity sweep explorer", proof_screens["lighting-feasibility"])

    def test_payload_validator_accepts_generated_payload(self):
        errors = self.generator.validate_payload(self.payload)

        self.assertEqual(errors, [])

    def test_review_log_template_has_required_fields(self):
        fieldnames, rows = self.validator.read_review_log(REVIEW_LOG_PATH)

        self.assertEqual(fieldnames, self.validator.REQUIRED_FIELDS)
        self.assertEqual(rows, [])

    def test_review_log_template_validates(self):
        errors = self.validator.validate_review_log(REVIEW_LOG_PATH, CONSOLE_DATA_PATH)

        self.assertEqual(errors, [])

    def test_export_ready_requires_reviewer_role_and_note(self):
        review_log = self.write_review_log(
            [
                {
                    "project_id": "wcca-prep",
                    "object_id": "SYN-WCCA-001",
                    "object_type": "WCCA result",
                    "prior_state": "Needs review",
                    "new_state": "Export ready",
                    "reviewer_role": "",
                    "review_note": "",
                    "blocker_reason": "",
                    "publication_check": "",
                    "run_marker": "unit-test",
                }
            ]
        )

        errors = self.validator.validate_review_log(review_log, CONSOLE_DATA_PATH)

        self.assertTrue(any("requires non-empty reviewer_role and review_note" in error for error in errors))

    def test_safe_to_publish_requires_all_publication_checks_and_no_open_rows(self):
        review_log = self.write_review_log(
            [
                {
                    "project_id": "lighting-feasibility",
                    "object_id": "SYN-LGT-001",
                    "object_type": "Feasibility case",
                    "prior_state": "Export ready",
                    "new_state": "Safe to publish",
                    "reviewer_role": "Qualified reviewer",
                    "review_note": "Reviewed for publication.",
                    "blocker_reason": "",
                    "publication_check": "synthetic_label|human_review",
                    "run_marker": "unit-test",
                },
                {
                    "project_id": "lighting-feasibility",
                    "object_id": "SYN-LGT-002",
                    "object_type": "Feasibility case",
                    "prior_state": "Needs review",
                    "new_state": "Needs review",
                    "reviewer_role": "",
                    "review_note": "",
                    "blocker_reason": "",
                    "publication_check": "",
                    "run_marker": "unit-test",
                },
            ]
        )

        errors = self.validator.validate_review_log(review_log, CONSOLE_DATA_PATH)

        self.assertTrue(any("missing publication checks" in error for error in errors))
        self.assertTrue(any("blocked while any row remains" in error for error in errors))

    def test_generated_artifact_fields_are_not_allowed_in_review_log(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
            handle.write(",".join(self.validator.REQUIRED_FIELDS + ["artifacts"]) + "\n")
            review_log = Path(handle.name)

        errors = self.validator.validate_review_log(review_log, CONSOLE_DATA_PATH)

        self.assertTrue(any("generated artifact fields" in error for error in errors))

    def test_console_screenshots_exist_and_are_indexed(self):
        screenshot_index = SCREENSHOT_INDEX_PATH.read_text(encoding="utf-8")

        for screenshot in CONSOLE_SCREENSHOTS:
            with self.subTest(screenshot=screenshot):
                path = REPO_ROOT / screenshot
                self.assertTrue(path.exists(), screenshot)
                self.assertGreater(path.stat().st_size, 10_000)
                self.assertIn(screenshot, screenshot_index)

    def test_public_qr_route_shims_exist(self):
        for route_file, hash_route in PUBLIC_ROUTE_FILES:
            with self.subTest(route_file=route_file):
                content = (REPO_ROOT / route_file).read_text(encoding="utf-8")
                self.assertIn(hash_route, content)
                self.assertIn("index.html", content)

    def test_browser_demo_hooks_exist(self):
        app_js = (REPO_ROOT / "ux-console" / "app.js").read_text(encoding="utf-8")

        self.assertIn("calculateFeasibilityCase", app_js)
        self.assertIn("generateRequirementsReview", app_js)
        self.assertIn("localStorage", app_js)
        self.assertIn("#tools/feasibility", app_js)
        self.assertIn("#tools/requirements", app_js)

    def test_github_pages_deployment_notes_are_static(self):
        deployment_notes = DEPLOYMENT_NOTES_PATH.read_text(encoding="utf-8")

        for route_file, hash_route in PUBLIC_ROUTE_FILES:
            route = "/" + route_file.removeprefix("ux-console/").removesuffix("/index.html")
            with self.subTest(route=route):
                self.assertIn(route, deployment_notes)
                self.assertIn(hash_route, (REPO_ROOT / route_file).read_text(encoding="utf-8"))

        self.assertIn("GitHub Pages", deployment_notes)
        self.assertIn("https://<github-user>.github.io/<repo>/tools", deployment_notes)
        self.assertIn("uploads only the `ux-console/` directory", deployment_notes)
        self.assertNotIn("Netlify", deployment_notes)

    def write_review_log(self, rows):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
            handle.write(",".join(self.validator.REQUIRED_FIELDS) + "\n")
            for row in rows:
                handle.write(",".join(row[field] for field in self.validator.REQUIRED_FIELDS) + "\n")
            return Path(handle.name)


if __name__ == "__main__":
    unittest.main()
