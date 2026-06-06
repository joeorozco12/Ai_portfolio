"""Optional PDF import helpers for public or synthetic datasheet sources."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .image_tools import ImportedImage, inspect_image_bytes, validate_source_category


class OptionalDependencyUnavailable(RuntimeError):
    """Raised when an optional import path needs a package not installed here."""


@dataclass(frozen=True)
class PdfImportRequest:
    """Reviewable request to render one public/synthetic PDF page."""

    source_name: str
    source_category: str
    page_index: int = 0
    zoom: float = 1.5
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.source_name.strip():
            raise ValueError("source_name must be a non-empty string.")
        validate_source_category(self.source_category)
        if self.page_index < 0:
            raise ValueError("page_index must be zero or greater.")
        if self.zoom <= 0:
            raise ValueError("zoom must be positive.")


def render_pdf_page_to_image(
    pdf_content: bytes,
    request: PdfImportRequest,
) -> ImportedImage:
    """Render a PDF page to PNG when PyMuPDF is available.

    This helper is intentionally optional. The deterministic tests do not
    require PyMuPDF, and any rendered page still requires manual plot-region,
    calibration, and overlay review before use.
    """

    if not pdf_content:
        raise ValueError("PDF content must not be empty.")

    try:
        import fitz  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise OptionalDependencyUnavailable(
            "PDF rendering requires PyMuPDF. Install requirements.txt before "
            "rendering public or synthetic datasheet PDFs."
        ) from exc

    document = fitz.open(stream=pdf_content, filetype="pdf")
    if request.page_index >= len(document):
        raise ValueError("page_index is outside the PDF page range.")

    page = document[request.page_index]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(request.zoom, request.zoom))
    image_content = pixmap.tobytes("png")
    image_format, width_px, height_px = inspect_image_bytes(image_content)
    return ImportedImage(
        source_name=f"{request.source_name}:page_{request.page_index}",
        source_category=validate_source_category(request.source_category),
        image_format=image_format,
        width_px=width_px,
        height_px=height_px,
        content=image_content,
        source_type="datasheet_pdf_page_render",
        review_status="rendered_requires_manual_plot_region_review",
        notes=request.notes,
    )


def load_pdf_bytes(path: Path) -> bytes:
    """Load a local PDF after checking the extension is explicit."""

    path = Path(path)
    if path.suffix.lower() != ".pdf":
        raise ValueError("PDF import requires a .pdf file.")
    return path.read_bytes()
