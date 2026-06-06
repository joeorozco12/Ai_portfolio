"""Export helpers for digitized LED curve artifacts."""

from __future__ import annotations

import csv
import json
import re
import struct
import zlib
from pathlib import Path
from typing import Any, Sequence

from . import report as report_builder
from .calibration import EngineeringPoint
from .curve_fit import PchipSegment, build_pchip_segments
from .report import (
    DOWNSTREAM_USE_WARNINGS,
    HUMAN_REVIEW_NOTE,
    SYNTHETIC_LABEL,
    build_report_context,
    write_markdown_report,
)

EXPORT_PACKAGE_SCHEMA_VERSION = "led_curve_export_package_1.0"


def safe_name(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "curve_lookup"


def write_points_csv(
    path: Path,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    x_axis = metadata["x_axis"]
    y_axis = metadata["y_axis"]
    fieldnames = [
        "part_number",
        "curve_name",
        "x_name",
        "x_unit",
        "y_name",
        "y_unit",
        "x",
        "y",
        "source_pixel_x",
        "source_pixel_y",
        "source_page",
        "digitization_method",
        "fit_model",
        "review_status",
        "engineering_note",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for point in sorted(points, key=lambda item: item.x):
            writer.writerow(
                {
                    "part_number": metadata["part_number"],
                    "curve_name": metadata["curve_name"],
                    "x_name": x_axis["label"],
                    "x_unit": x_axis["unit"],
                    "y_name": y_axis["label"],
                    "y_unit": y_axis["unit"],
                    "x": f"{point.x:.6g}",
                    "y": f"{point.y:.6g}",
                    "source_pixel_x": f"{point.source_pixel_x:.3f}",
                    "source_pixel_y": f"{point.source_pixel_y:.3f}",
                    "source_page": metadata["source_page"],
                    "digitization_method": metadata["digitization_method"],
                    "fit_model": metadata["fit_model"],
                    "review_status": point.review_status,
                    "engineering_note": metadata["engineering_note"],
                }
            )


def write_metadata_json(path: Path, metadata: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "synthetic_label": SYNTHETIC_LABEL,
        "human_review_required": HUMAN_REVIEW_NOTE,
        "source_metadata": report_builder.build_source_metadata(metadata),
        "calibration_metadata": report_builder.build_calibration_metadata(metadata),
        "assumptions": report_builder.build_assumptions(metadata),
        "method": report_builder.build_method_metadata(metadata),
        "review_metadata": report_builder.build_review_status(metadata),
        "downstream_use_warnings": list(DOWNSTREAM_USE_WARNINGS),
        **metadata,
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_python_lookup(
    path: Path,
    function_name: str,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    segments = build_pchip_segments(points)
    segment_rows = [
        [segment.x0, segment.x1, segment.a, segment.b, segment.c, segment.d]
        for segment in segments
    ]
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    segments_json = json.dumps(segment_rows, indent=4)
    warnings_json = json.dumps(list(DOWNSTREAM_USE_WARNINGS), indent=4)
    content = f'''"""Synthetic LED curve lookup generated from digitized plot points."""

SYNTHETIC_LABEL = "{SYNTHETIC_LABEL}"
HUMAN_REVIEW_REQUIRED = "{HUMAN_REVIEW_NOTE}"
CURVE_METADATA = {metadata_json}
DOWNSTREAM_USE_WARNINGS = {warnings_json}
PCHIP_SEGMENTS = {segments_json}


def {function_name}(x_value):
    """Return interpolated y-value using draft PCHIP coefficients.

    Endpoint clamping is used outside the digitized range. This lookup is a
    review artifact and must not be used for engineering decisions until a
    qualified engineer accepts the export package.
    """

    segments = PCHIP_SEGMENTS
    if x_value <= segments[0][0]:
        return segments[0][2]
    last = segments[-1]
    if x_value >= last[1]:
        t = last[1] - last[0]
        return last[2] + last[3] * t + last[4] * t * t + last[5] * t * t * t

    for x0, x1, a, b, c, d in segments:
        if x0 <= x_value <= x1:
            t = x_value - x0
            return a + b * t + c * t * t + d * t * t * t
    raise ValueError("Input value is outside interpolation intervals.")
'''
    path.write_text(content, encoding="utf-8")


def write_matlab_lookup(
    path: Path,
    function_name: str,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    segments = build_pchip_segments(points)
    rows = "\n".join(
        "    "
        + " ".join(
            f"{value:.12g}"
            for value in [segment.x0, segment.x1, segment.a, segment.b, segment.c, segment.d]
        )
        for segment in segments
    )
    content = f"""function y = {function_name}(x)
% {SYNTHETIC_LABEL}
% {HUMAN_REVIEW_NOTE}
% Curve: {metadata["curve_name"]}
% Source: {metadata["datasheet_source"]}, page {metadata["source_page"]}
% Note: {metadata["engineering_note"]}
% Warning: Do not use for WCCA, feasibility, thermal, optical, design-review, or design-decision workflows until qualified engineering review is complete.
% Warning: This lookup clamps outside the digitized x-range and is not an approved extrapolation model.

segments = [
{rows}
];

y = zeros(size(x));
for idx = 1:numel(x)
    x_value = x(idx);
    if x_value <= segments(1, 1)
        y(idx) = segments(1, 3);
    elseif x_value >= segments(end, 2)
        t = segments(end, 2) - segments(end, 1);
        y(idx) = segments(end, 3) + segments(end, 4) * t + segments(end, 5) * t^2 + segments(end, 6) * t^3;
    else
        for seg_idx = 1:size(segments, 1)
            if x_value >= segments(seg_idx, 1) && x_value <= segments(seg_idx, 2)
                t = x_value - segments(seg_idx, 1);
                y(idx) = segments(seg_idx, 3) + segments(seg_idx, 4) * t + segments(seg_idx, 5) * t^2 + segments(seg_idx, 6) * t^3;
                break;
            end
        end
    end
end
end
"""
    path.write_text(content, encoding="utf-8")


def write_overlay_png(
    path: Path,
    points: Sequence[EngineeringPoint],
    width: int = 640,
    height: int = 480,
) -> None:
    """Write a lightweight synthetic overlay PNG using only stdlib code."""

    path.parent.mkdir(parents=True, exist_ok=True)
    pixels = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]

    for x in range(80, 561, 80):
        _draw_line(pixels, x, 60, x, 420, (225, 225, 225))
    for y in range(60, 421, 60):
        _draw_line(pixels, 80, y, 560, y, (225, 225, 225))

    _draw_line(pixels, 80, 420, 560, 420, (30, 30, 30))
    _draw_line(pixels, 80, 420, 80, 60, (30, 30, 30))

    sorted_points = sorted(points, key=lambda point: point.source_pixel_x)
    for left, right in zip(sorted_points, sorted_points[1:]):
        _draw_line(
            pixels,
            round(left.source_pixel_x),
            round(left.source_pixel_y),
            round(right.source_pixel_x),
            round(right.source_pixel_y),
            (90, 90, 90),
        )
    for point in sorted_points:
        _draw_circle(
            pixels,
            round(point.source_pixel_x),
            round(point.source_pixel_y),
            radius=5,
            color=(210, 35, 35),
        )

    _write_png(path, pixels)


def write_export_package(
    output_dir: Path,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> dict[str, Path]:
    """Write a structured export package for reviewable downstream use."""

    output_dir.mkdir(parents=True, exist_ok=True)
    curve_slug = safe_name(metadata["curve_name"])
    function_name = f"lookup_{curve_slug}"
    artifact_rel_paths = {
        "csv_points": "data/digitized_curve_points.csv",
        "json_metadata": "metadata/export_manifest.json",
        "source_metadata_json": "metadata/source_metadata.json",
        "calibration_metadata_json": "metadata/calibration_metadata.json",
        "python_lookup": f"lookups/python/{function_name}.py",
        "matlab_lookup": f"lookups/matlab/{function_name}.m",
        "overlay_png": f"review/overlay_{curve_slug}.png",
        "markdown_report": "review/extraction_report.md",
    }
    paths = {
        name: output_dir / relative_path
        for name, relative_path in artifact_rel_paths.items()
    }

    write_points_csv(paths["csv_points"], metadata, points)
    write_python_lookup(paths["python_lookup"], function_name, metadata, points)
    write_matlab_lookup(paths["matlab_lookup"], function_name, metadata, points)
    write_overlay_png(paths["overlay_png"], points)

    context = build_report_context(metadata, points, artifact_rel_paths)
    manifest = {
        "package_name": output_dir.name,
        "package_status": "draft_requires_qualified_engineer_review",
        **context,
    }
    _write_json(paths["json_metadata"], manifest)
    _write_json(
        paths["source_metadata_json"],
        {
            "synthetic_label": SYNTHETIC_LABEL,
            "human_review_required": HUMAN_REVIEW_NOTE,
            "publication_classification": context["publication_classification"],
            "source_metadata": context["source_metadata"],
            "downstream_use_warnings": context["downstream_use_warnings"],
        },
    )
    _write_json(
        paths["calibration_metadata_json"],
        {
            "synthetic_label": SYNTHETIC_LABEL,
            "human_review_required": HUMAN_REVIEW_NOTE,
            "publication_classification": context["publication_classification"],
            "calibration_metadata": context["calibration_metadata"],
            "assumptions": context["assumptions"],
            "validation_status": context["validation_status"],
            "review_status": context["review_status"],
            "downstream_use_warnings": context["downstream_use_warnings"],
        },
    )
    write_markdown_report(
        paths["markdown_report"],
        metadata,
        points,
        overlay_path=artifact_rel_paths["overlay_png"],
        csv_path=artifact_rel_paths["csv_points"],
        json_path=artifact_rel_paths["json_metadata"],
        python_path=artifact_rel_paths["python_lookup"],
        matlab_path=artifact_rel_paths["matlab_lookup"],
        source_metadata_path=artifact_rel_paths["source_metadata_json"],
        calibration_metadata_path=artifact_rel_paths["calibration_metadata_json"],
    )

    return paths


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_png(path: Path, pixels: list[list[tuple[int, int, int]]]) -> None:
    height = len(pixels)
    width = len(pixels[0])
    raw_rows = []
    for row in pixels:
        raw_rows.append(b"\x00" + b"".join(bytes(pixel) for pixel in row))
    raw = b"".join(raw_rows)

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        checksum = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", checksum)

    payload = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


def _draw_line(
    pixels: list[list[tuple[int, int, int]]],
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: tuple[int, int, int],
) -> None:
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    error = dx + dy
    x = x0
    y = y0
    while True:
        _set_pixel(pixels, x, y, color)
        if x == x1 and y == y1:
            break
        doubled = 2 * error
        if doubled >= dy:
            error += dy
            x += sx
        if doubled <= dx:
            error += dx
            y += sy


def _draw_circle(
    pixels: list[list[tuple[int, int, int]]],
    center_x: int,
    center_y: int,
    radius: int,
    color: tuple[int, int, int],
) -> None:
    for y in range(center_y - radius, center_y + radius + 1):
        for x in range(center_x - radius, center_x + radius + 1):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius * radius:
                _set_pixel(pixels, x, y, color)


def _set_pixel(
    pixels: list[list[tuple[int, int, int]]],
    x: int,
    y: int,
    color: tuple[int, int, int],
) -> None:
    if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
        pixels[y][x] = color
