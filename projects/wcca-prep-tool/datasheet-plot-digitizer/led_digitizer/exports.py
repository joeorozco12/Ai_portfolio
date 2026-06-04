"""Export helpers for digitized LED curve artifacts."""

from __future__ import annotations

import csv
import json
import re
import struct
import zlib
from pathlib import Path
from typing import Any, Sequence

from .calibration import EngineeringPoint
from .curve_fit import PchipSegment, build_pchip_segments

SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts "
    "only. A qualified engineer owns final review and approval."
)


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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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
        **metadata,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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
    content = f'''"""Synthetic LED curve lookup generated from digitized plot points."""

SYNTHETIC_LABEL = "{SYNTHETIC_LABEL}"
HUMAN_REVIEW_REQUIRED = "{HUMAN_REVIEW_NOTE}"
CURVE_METADATA = {metadata_json}
PCHIP_SEGMENTS = {segments_json}


def {function_name}(x_value):
    """Return interpolated y-value using reviewed PCHIP coefficients."""

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


def write_markdown_report(
    path: Path,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
    overlay_path: str,
    csv_path: str,
    json_path: str,
    python_path: str,
    matlab_path: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_points = sorted(points, key=lambda point: point.x)
    first = sorted_points[0]
    last = sorted_points[-1]
    content = f"""# LED Datasheet Plot Digitizer & Curve-Fit Builder

{SYNTHETIC_LABEL}

> {HUMAN_REVIEW_NOTE}

## Problem

LED datasheet-style plots often contain useful voltage, current, temperature, and flux behavior in image form. Engineers need structured, traceable curve data for WCCA preparation, feasibility screening, simulation, and design-review discussion.

## Engineering Context

This artifact demonstrates a synthetic automotive-lighting data-prep workflow. It uses a synthetic LED identifier and synthetic plot points only. It does not include proprietary datasheets, customer programs, supplier records, internal requirements, schematics, BOM data, harness data, cost data, or validation results.

## Workflow

1. Load a public or synthetic datasheet plot image.
2. Select the plot region.
3. Calibrate the x and y axes from known reference points.
4. Digitize curve points by manual picking first.
5. Fit a shape-preserving interpolation model.
6. Export reviewed CSV, JSON, Python, MATLAB, overlay, and report artifacts.

## Inputs

- Curve name: `{metadata["curve_name"]}`
- Source: `{metadata["datasheet_source"]}`
- Source page: `{metadata["source_page"]}`
- X axis: `{metadata["x_axis"]["label"]}` `{metadata["x_axis"]["unit"]}`
- Y axis: `{metadata["y_axis"]["label"]}` `{metadata["y_axis"]["unit"]}`
- Digitization method: `{metadata["digitization_method"]}`
- Digitized points: `{len(sorted_points)}`

## Outputs

- CSV points: `{csv_path}`
- JSON metadata: `{json_path}`
- Python lookup function: `{python_path}`
- MATLAB lookup function: `{matlab_path}`
- Overlay verification image: `{overlay_path}`
- Markdown extraction report: this file

## Screenshots Or Screenshot Placeholders

- Overlay verification image: `{overlay_path}`
- Streamlit workflow placeholder: `captures/streamlit_workflow_mock.md`

## Sanitized Sample Data

The sample extraction uses `{metadata["part_number"]}` from `{metadata["manufacturer"]}`. These are synthetic demonstration labels, not real device identifiers. The extracted x range is `{first.x:.3f}` to `{last.x:.3f}` {metadata["x_axis"]["unit"]}; the extracted y range is `{first.y:.1f}` to `{last.y:.1f}` {metadata["y_axis"]["unit"]}.

## Human Review Controls

- Manual axis calibration is required before export.
- Curve points remain `draft_extraction` until a qualified reviewer checks them.
- Overlay review is required before use in WCCA or feasibility inputs.
- Source page and digitization method are exported with every row.
- The reviewer must confirm that plot data is reference-only and not a guaranteed device limit.
- The tool does not approve LED design values.

## Codex Contribution

Codex scaffolded the Streamlit app shell, deterministic calibration math, PCHIP curve-fit builder, export modules, synthetic sample data, overlay generator, and unit tests.

## Jose Contribution

Jose defines the LED engineering data-prep use case, WCCA and feasibility workflow boundary, required review controls, acceptable public/synthetic source boundary, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured data extraction workflow
- Deterministic transformation from pixels to engineering units
- Curve-fit generation from reviewed samples
- Metadata-rich export generation
- Testable human-in-the-loop automation

## Engineering Skills Demonstrated

- LED forward-voltage and current curve interpretation
- Datasheet plot traceability
- WCCA input preparation
- Simulation lookup-table preparation
- Engineering review governance

## Risks And Mitigations

- Risk: Digitized plot points could be mistaken for guaranteed limits. Mitigation: every export states that plot data is reference-only and requires engineering review.
- Risk: Calibration errors could distort the curve. Mitigation: manual axis calibration, overlay review, source-pixel export, and reviewer status are required.
- Risk: A curve fit could oversmooth engineering behavior. Mitigation: the MVP uses shape-preserving PCHIP coefficients and exports raw points alongside the fitted model.
- Risk: Public output could reveal controlled data. Mitigation: included samples are synthetic and public use requires sanitized/public source review.

## Next Improvements

- Add browser-based image click capture for calibration and curve picking.
- Add optional OpenCV-assisted extraction after manual picks are accepted.
- Add log-axis support to the Streamlit workflow.
- Add multi-curve extraction from a single plot image.
- Add a reviewed adapter that feeds WCCA and Project 5 feasibility inputs only after approval.

## Proof Gaps

- The current generated sample is synthetic and does not prove extraction quality on a real public datasheet.
- Streamlit image click/crop interaction still needs a browser component or custom canvas package.
- Optional PDF rendering and OpenCV extraction require installing runtime dependencies from `requirements.txt`.
- A qualified engineering review signoff has not been completed.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The code and sample data are synthetic and sanitized, but the tool behavior, screenshots, and public framing still require qualified engineering review before publication.
"""
    path.write_text(content, encoding="utf-8")


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
