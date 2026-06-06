import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from led_digitizer.calibration import AxisCalibration, CurveCalibration
from led_digitizer.extraction_assisted import (
    ASSISTED_DRAFT_METHOD,
    ASSISTED_DRAFT_REVIEW_STATUS,
    AssistedExtractionSettings,
    assisted_extraction_boundary,
    draft_assisted_points_from_candidate_pixels,
    maybe_extract_assisted_points,
)
from led_digitizer.image_tools import (
    CandidatePixel,
    PlotRegion,
    inspect_image_bytes,
    load_public_or_synthetic_image,
)
from led_digitizer.pdf_import import PdfImportRequest, load_pdf_bytes


class AssistedExtractionTests(unittest.TestCase):
    def test_assisted_extraction_is_optional(self):
        points = maybe_extract_assisted_points(
            enabled=False,
            candidate_pixels=[object()],
            calibration=_calibration(),
        )

        self.assertEqual(points, [])

    def test_draft_assisted_points_preserve_traceability(self):
        points = draft_assisted_points_from_candidate_pixels(
            candidate_pixels=[
                CandidatePixel(100.0, 300.0, 0.4),
                CandidatePixel(110.0, 320.0, 0.8),
                CandidatePixel(150.0, 250.0, 0.7),
                CandidatePixel(500.0, 100.0, 0.9),
            ],
            calibration=_calibration(),
            plot_region=PlotRegion(left=90.0, top=200.0, width=100.0, height=150.0),
            settings=AssistedExtractionSettings(x_bin_size_px=20.0, min_confidence=0.2),
        )

        self.assertEqual(len(points), 2)
        self.assertEqual(points[0].point_id, "A01")
        self.assertEqual(points[0].method, ASSISTED_DRAFT_METHOD)
        self.assertEqual(points[0].review_status, ASSISTED_DRAFT_REVIEW_STATUS)
        self.assertAlmostEqual(points[0].source_pixel_x, 106.6666666667)
        self.assertAlmostEqual(points[0].source_pixel_y, 313.3333333333)
        self.assertAlmostEqual(points[0].confidence, 0.6)
        self.assertIn("Manual calibration", points[0].notes)

    def test_assisted_settings_must_remain_draft(self):
        with self.assertRaises(ValueError):
            AssistedExtractionSettings(method="final_curve_pick")

    def test_assisted_boundary_blocks_downstream_use(self):
        boundary = assisted_extraction_boundary()

        self.assertTrue(boundary["optional"])
        self.assertEqual(boundary["status"], "draft")
        self.assertEqual(
            boundary["downstream_use"],
            "blocked_until_manual_overlay_and_engineer_review",
        )

    def test_public_or_synthetic_image_import_reads_png_metadata(self):
        png_content = _png_bytes(width=16, height=9)
        image_format, width_px, height_px = inspect_image_bytes(png_content)

        self.assertEqual((image_format, width_px, height_px), ("png", 16, 9))

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "synthetic_plot.png"
            path.write_bytes(png_content)

            imported = load_public_or_synthetic_image(
                path,
                source_category="synthetic",
                notes="synthetic image for deterministic test",
            )

        self.assertEqual(imported.source_name, "synthetic_plot.png")
        self.assertEqual(imported.source_category, "synthetic")
        self.assertEqual(imported.width_px, 16)
        self.assertEqual(imported.height_px, 9)
        self.assertEqual(
            imported.review_status,
            "imported_requires_manual_plot_region_review",
        )

    def test_pdf_import_request_is_public_or_synthetic_only(self):
        request = PdfImportRequest(
            source_name="public_datasheet_example",
            source_category="public",
            page_index=0,
        )

        self.assertEqual(request.source_category, "public")

        with self.assertRaises(ValueError):
            PdfImportRequest(source_name="internal_example", source_category="internal")

    def test_pdf_byte_loader_requires_pdf_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            text_path = Path(temp_dir) / "source.txt"
            text_path.write_text("not a pdf", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_pdf_bytes(text_path)


def _calibration() -> CurveCalibration:
    return CurveCalibration(
        x_axis=AxisCalibration(80.0, 560.0, 2.5, 4.5),
        y_axis=AxisCalibration(420.0, 60.0, 0.0, 4000.0),
    )


def _png_bytes(*, width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + (13).to_bytes(4, "big")
        + b"IHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
    )


if __name__ == "__main__":
    unittest.main()
