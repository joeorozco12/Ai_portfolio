"""Image import helpers for public or synthetic plot sources."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SOURCE_CATEGORIES = {"public", "synthetic"}
SUPPORTED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}


@dataclass(frozen=True)
class PlotRegion:
    """Pixel-space plot region selected for calibration and extraction."""

    left: float
    top: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.left < 0 or self.top < 0:
            raise ValueError("Plot region left/top must be non-negative.")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Plot region width/height must be positive.")

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    def contains(self, source_pixel_x: float, source_pixel_y: float) -> bool:
        return (
            self.left <= source_pixel_x <= self.right
            and self.top <= source_pixel_y <= self.bottom
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True)
class ImportedImage:
    """Imported raster source that remains tied to public/synthetic provenance."""

    source_name: str
    source_category: str
    image_format: str
    width_px: int
    height_px: int
    content: bytes
    source_type: str = "datasheet_plot_image"
    review_status: str = "imported_requires_manual_plot_region_review"
    notes: str = ""

    def __post_init__(self) -> None:
        _require_text(self.source_name, "source_name")
        validate_source_category(self.source_category)
        _require_text(self.image_format, "image_format")
        _require_text(self.source_type, "source_type")
        _require_text(self.review_status, "review_status")
        if self.width_px <= 0 or self.height_px <= 0:
            raise ValueError("Imported image dimensions must be positive.")
        if not self.content:
            raise ValueError("Imported image content must not be empty.")

    def to_metadata(self) -> dict[str, str | int]:
        return {
            "source_name": self.source_name,
            "source_category": self.source_category,
            "source_type": self.source_type,
            "image_format": self.image_format,
            "width_px": self.width_px,
            "height_px": self.height_px,
            "review_status": self.review_status,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class CandidatePixel:
    """Pixel candidate from a draft assisted extractor."""

    source_pixel_x: float
    source_pixel_y: float
    signal_strength: float = 1.0

    def __post_init__(self) -> None:
        if self.source_pixel_x < 0 or self.source_pixel_y < 0:
            raise ValueError("Source pixel coordinates must be non-negative.")
        if not 0.0 <= self.signal_strength <= 1.0:
            raise ValueError("Signal strength must be between 0.0 and 1.0.")


def validate_source_category(source_category: str) -> str:
    """Return a normalized source category or reject unsafe source classes."""

    normalized = str(source_category).strip().lower()
    if normalized not in SOURCE_CATEGORIES:
        raise ValueError("Source category must be 'public' or 'synthetic'.")
    return normalized


def load_public_or_synthetic_image(
    path: Path,
    *,
    source_category: str,
    source_name: str | None = None,
    notes: str = "",
) -> ImportedImage:
    """Load PNG/JPEG bytes and preserve source metadata for review."""

    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_IMAGE_SUFFIXES:
        raise ValueError("Image import supports PNG, JPG, or JPEG files.")

    content = path.read_bytes()
    image_format, width_px, height_px = inspect_image_bytes(content)
    return ImportedImage(
        source_name=source_name or path.name,
        source_category=validate_source_category(source_category),
        image_format=image_format,
        width_px=width_px,
        height_px=height_px,
        content=content,
        notes=notes,
    )


def inspect_image_bytes(content: bytes) -> tuple[str, int, int]:
    """Return image format and dimensions for PNG/JPEG bytes using stdlib only."""

    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        if len(content) < 24:
            raise ValueError("PNG content is too short to contain dimensions.")
        width_px = int.from_bytes(content[16:20], "big")
        height_px = int.from_bytes(content[20:24], "big")
        return "png", width_px, height_px

    if content.startswith(b"\xff\xd8"):
        return _inspect_jpeg_dimensions(content)

    raise ValueError("Unsupported image content. Expected PNG or JPEG bytes.")


def validate_plot_region(
    region: PlotRegion,
    *,
    image_width_px: int,
    image_height_px: int,
) -> PlotRegion:
    """Reject crop regions that extend outside the imported source image."""

    if region.right > image_width_px or region.bottom > image_height_px:
        raise ValueError("Plot region extends beyond imported image dimensions.")
    return region


def _inspect_jpeg_dimensions(content: bytes) -> tuple[str, int, int]:
    index = 2
    while index < len(content):
        if content[index] != 0xFF:
            index += 1
            continue
        while index < len(content) and content[index] == 0xFF:
            index += 1
        if index >= len(content):
            break
        marker = content[index]
        index += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if index + 2 > len(content):
            break
        segment_length = int.from_bytes(content[index : index + 2], "big")
        if segment_length < 2:
            raise ValueError("JPEG segment length is invalid.")
        segment_start = index + 2
        segment_end = index + segment_length
        if marker in {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }:
            if segment_start + 5 > len(content):
                break
            height_px = int.from_bytes(content[segment_start + 1 : segment_start + 3], "big")
            width_px = int.from_bytes(content[segment_start + 3 : segment_start + 5], "big")
            return "jpeg", width_px, height_px
        index = segment_end

    raise ValueError("JPEG dimensions could not be read.")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
