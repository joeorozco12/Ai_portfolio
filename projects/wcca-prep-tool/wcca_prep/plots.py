"""Stdlib-only PNG plots for synthetic WCCA proof assets."""

from __future__ import annotations

import struct
import zlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .calculations import WccaResult
from .summary import pass_fail_status, result_margin_pct, worst_results_by_case


Color = Tuple[int, int, int]
WHITE: Color = (255, 255, 255)
INK: Color = (31, 41, 55)
MUTED: Color = (100, 116, 139)
GRID: Color = (226, 232, 240)
PASS_COLOR: Color = (34, 139, 94)
REVIEW_COLOR: Color = (202, 138, 4)
FAIL_COLOR: Color = (190, 72, 72)
BLUE: Color = (37, 99, 235)
PURPLE: Color = (124, 58, 237)
TEAL: Color = (13, 148, 136)
PLOT_WIDTH = 1200
PLOT_HEIGHT = 680


def write_plot_gallery(path: Path, results: Sequence[WccaResult]) -> List[Path]:
    path.mkdir(parents=True, exist_ok=True)
    worst_cases = worst_results_by_case(results)
    paths: List[Path] = []

    paths.append(path / "margin_by_case.png")
    _write_bar_chart(
        paths[-1],
        "MARGIN BY CASE",
        [_case_label(result.case_id) for result in worst_cases],
        [result_margin_pct(result) or 0.0 for result in worst_cases],
        "MARGIN PCT",
        [_status_color(pass_fail_status(result)) for result in worst_cases],
    )

    condition_ratios = _max_by_condition(results, value=lambda result: (result.max_ratio or 0.0) * 100.0)
    paths.append(path / "worst_case_result_by_condition.png")
    _write_bar_chart(
        paths[-1],
        "WORST CASE RESULT BY CONDITION",
        list(condition_ratios.keys()),
        list(condition_ratios.values()),
        "MAX RATIO PCT",
        [BLUE for _ in condition_ratios],
    )

    status_counts = Counter(pass_fail_status(result) for result in results)
    status_labels = ["PASS", "REVIEW", "FAIL"]
    paths.append(path / "pass_fail_distribution.png")
    _write_bar_chart(
        paths[-1],
        "PASS FAIL DISTRIBUTION",
        status_labels,
        [float(status_counts.get(label.title(), 0)) for label in status_labels],
        "COUNT",
        [PASS_COLOR, REVIEW_COLOR, FAIL_COLOR],
    )

    thermal_values = _max_by_condition(
        results,
        value=lambda result: result.junction_temp_c if result.junction_temp_c is not None else 0.0,
    )
    paths.append(path / "thermal_temperature_sensitivity.png")
    _write_bar_chart(
        paths[-1],
        "THERMAL TEMPERATURE SENSITIVITY",
        list(thermal_values.keys()),
        list(thermal_values.values()),
        "MAX TJ C",
        [PURPLE for _ in thermal_values],
    )

    voltage_values = _max_by_vin(results, value=lambda result: result.input_current_a)
    paths.append(path / "voltage_sensitivity.png")
    _write_bar_chart(
        paths[-1],
        "VOLTAGE SENSITIVITY",
        list(voltage_values.keys()),
        list(voltage_values.values()),
        "MAX INPUT CURRENT A",
        [TEAL for _ in voltage_values],
    )

    return paths


def _max_by_condition(results: Sequence[WccaResult], value) -> Dict[str, float]:
    grouped: Dict[str, float] = {}
    for result in results:
        label = _condition_label(result.condition_id)
        grouped[label] = max(grouped.get(label, float("-inf")), value(result))
    return {label: grouped[label] for label in sorted(grouped)}


def _max_by_vin(results: Sequence[WccaResult], value) -> Dict[str, float]:
    grouped: Dict[str, float] = defaultdict(lambda: float("-inf"))
    for result in results:
        grouped[f"{result.vin_v:.1f}V"] = max(grouped[f"{result.vin_v:.1f}V"], value(result))
    return {label: grouped[label] for label in sorted(grouped, key=lambda item: float(item.rstrip("V")))}


def _status_color(status: str) -> Color:
    if status == "Pass":
        return PASS_COLOR
    if status == "Fail":
        return FAIL_COLOR
    return REVIEW_COLOR


def _case_label(case_id: str) -> str:
    return case_id.replace("SYN-WCCA-", "W")


def _condition_label(condition_id: str) -> str:
    label = condition_id.replace("SYN-OC-", "")
    return label.replace("LOWLINE", "LOW").replace("HIGHLINE", "HIGH").replace("HIGHLOAD", "LOAD")


def _write_bar_chart(
    path: Path,
    title: str,
    labels: Sequence[str],
    values: Sequence[float],
    y_label: str,
    colors: Sequence[Color],
) -> None:
    canvas = _new_canvas(PLOT_WIDTH, PLOT_HEIGHT, WHITE)
    left = 94
    top = 92
    right = PLOT_WIDTH - 46
    bottom = PLOT_HEIGHT - 92
    plot_width = right - left
    plot_height = bottom - top
    raw_min = min(values) if values else 0.0
    raw_max = max(values) if values else 1.0
    y_min = min(0.0, raw_min)
    y_max = max(0.0, raw_max)
    if y_min == y_max:
        y_max = y_min + 1.0
    span = y_max - y_min
    y_min -= span * 0.10
    y_max += span * 0.16

    def y_for(value: float) -> int:
        normalized = (value - y_min) / (y_max - y_min)
        return int(bottom - normalized * plot_height)

    _draw_text(canvas, 32, 24, title, INK, scale=3)
    _draw_text(canvas, 32, 62, y_label, MUTED, scale=2)
    for index in range(6):
        tick_value = y_min + (y_max - y_min) * index / 5
        y = y_for(tick_value)
        _draw_line(canvas, left, y, right, y, GRID)
        _draw_text(canvas, 24, y - 6, _format_tick(tick_value, y_max - y_min), MUTED, scale=1)

    zero_y = y_for(0.0)
    _draw_line(canvas, left, top, left, bottom, INK)
    _draw_line(canvas, left, zero_y, right, zero_y, INK)
    if not labels:
        _draw_text(canvas, left + 24, top + 120, "NO DATA", FAIL_COLOR, scale=3)
        _write_png(path, canvas)
        return

    group_width = plot_width / len(labels)
    bar_width = max(12, min(50, int(group_width * 0.58)))
    for index, (label, value) in enumerate(zip(labels, values)):
        group_start = int(left + index * group_width)
        x0 = group_start + int((group_width - bar_width) / 2)
        x1 = x0 + bar_width
        y_value = y_for(value)
        y0 = min(y_value, zero_y)
        y1 = max(y_value, zero_y)
        color = colors[index] if index < len(colors) else BLUE
        _draw_rect(canvas, x0, y0, x1, y1, color)
        text_y = y0 - 16 if value >= 0 else y1 + 6
        _draw_text(canvas, x0 - 2, text_y, _format_value(value), INK, scale=1)
        _draw_text(canvas, group_start + 6, bottom + 18, label, INK, scale=1)

    _write_png(path, canvas)


def _new_canvas(width: int, height: int, color: Color) -> List[List[Color]]:
    return [[color for _ in range(width)] for _ in range(height)]


def _draw_rect(canvas: List[List[Color]], x0: int, y0: int, x1: int, y1: int, color: Color) -> None:
    height = len(canvas)
    width = len(canvas[0])
    left = max(0, min(x0, x1))
    right = min(width - 1, max(x0, x1))
    top = max(0, min(y0, y1))
    bottom = min(height - 1, max(y0, y1))
    for y in range(top, bottom + 1):
        row = canvas[y]
        for x in range(left, right + 1):
            row[x] = color


def _draw_line(canvas: List[List[Color]], x0: int, y0: int, x1: int, y1: int, color: Color) -> None:
    if y0 == y1 or x0 == x1:
        _draw_rect(canvas, x0, y0, x1, y1, color)
        return
    steps = max(abs(x1 - x0), abs(y1 - y0))
    for step in range(steps + 1):
        x = round(x0 + (x1 - x0) * step / steps)
        y = round(y0 + (y1 - y0) * step / steps)
        _draw_rect(canvas, x, y, x, y, color)


def _draw_text(canvas: List[List[Color]], x: int, y: int, text: str, color: Color, scale: int = 1) -> None:
    cursor = x
    for char in text.upper():
        pattern = _FONT_5X7.get(char, _FONT_5X7[" "])
        for row_index, row in enumerate(pattern):
            for col_index, pixel in enumerate(row):
                if pixel == "1":
                    _draw_rect(
                        canvas,
                        cursor + col_index * scale,
                        y + row_index * scale,
                        cursor + (col_index + 1) * scale - 1,
                        y + (row_index + 1) * scale - 1,
                        color,
                    )
        cursor += 6 * scale


def _write_png(path: Path, canvas: List[List[Color]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    height = len(canvas)
    width = len(canvas[0])
    raw_rows = [b"\x00" + b"".join(bytes(pixel) for pixel in row) for row in canvas]
    compressed = zlib.compress(b"".join(raw_rows), level=9)

    def chunk(kind: bytes, data: bytes) -> bytes:
        checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)

    path.write_bytes(
        b"".join(
            [
                b"\x89PNG\r\n\x1a\n",
                chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
                chunk(b"IDAT", compressed),
                chunk(b"IEND", b""),
            ]
        )
    )


def _format_tick(value: float, span: float) -> str:
    if abs(value) < 0.05:
        value = 0.0
    if span <= 8:
        return f"{value:.1f}"
    return f"{value:.0f}"


def _format_value(value: float) -> str:
    if abs(value) >= 100:
        return f"{value:.0f}"
    if abs(value) >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}"


_FONT_5X7 = {
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "%": ["11001", "11010", "00100", "01000", "10110", "00110", "00000"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "11100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
}
