"""Deterministic feasibility engine for synthetic automotive lighting cases."""

from __future__ import annotations

import argparse
import csv
import struct
import zlib
from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts only. "
    "A qualified engineer owns final review and approval."
)

PASS_STATUS = "Pass"
MARGINAL_STATUS = "Marginal"
FAIL_STATUS = "Fail"

LIMIT_RATIO = 1.00
MARGINAL_RATIO = 0.85
MARGINAL_VOLTAGE_HEADROOM_V = 0.75
MARGINAL_TEMPERATURE_MARGIN_C = 10.0

PLOT_WIDTH = 960
PLOT_HEIGHT = 540
WHITE = (255, 255, 255)
INK = (31, 41, 55)
MUTED = (107, 114, 128)
GRID = (229, 231, 235)
PASS_COLOR = (37, 99, 235)
MARGINAL_COLOR = (217, 119, 6)
FAIL_COLOR = (220, 38, 38)
DRIVER_COLOR = (79, 70, 229)
LED_COLOR = (5, 150, 105)
CURRENT_COLOR = (8, 145, 178)


REQUIRED_COLUMNS = {
    "Case_ID",
    "Load_Name",
    "Driver_Topology",
    "LED_Count",
    "LED_Forward_Voltage_Nom_V",
    "LED_VF_Tol_pct",
    "LED_Current_Nom_A",
    "Current_Tol_pct",
    "Duty_Cycle",
    "VSupply_Min_V",
    "VSupply_Max_V",
    "Driver_Dropout_V",
    "Driver_Efficiency",
    "Efficiency_Tol_pct",
    "Max_Input_Current_A",
    "Max_Input_Voltage_V",
    "Max_Output_Power_W",
    "Board_Thermal_Resistance_C_per_W",
    "Max_Driver_Case_Temp_C",
    "LED_Thermal_Resistance_C_per_W",
    "Max_LED_Junction_Temp_C",
    "Ambient_Temp_C",
    "Max_Boost_Duty_Cycle",
}

AMBIENT_TEMPERATURE_SWEEP_C = [75.0, 85.0, 95.0, 105.0, 115.0]
LED_CURRENT_SWEEP_FACTORS = [0.80, 0.90, 1.00, 1.10, 1.20]
THERMAL_RESISTANCE_SWEEP_FACTORS = [0.80, 0.90, 1.00, 1.10, 1.20]
OPTICAL_EFFICIENCY_SWEEP_PCT = [70.0, 85.0, 100.0, 115.0, 130.0]

SENSITIVITY_FIELDNAMES = [
    "Synthetic_Label",
    "Human_Review_Note",
    "Publication_Classification",
    "Engineering_Review_Required",
    "Sweep_Name",
    "Variable_Name",
    "Sweep_Setting_Label",
    "Base_Value",
    "Sweep_Value",
    "Sweep_Unit",
    "Case_ID",
    "Load_Name",
    "Driver_Topology",
    "Applied_Ambient_Temp_C",
    "Applied_LED_Current_A",
    "Applied_Board_Thermal_Resistance_C_per_W",
    "Applied_LED_Thermal_Resistance_C_per_W",
    "Applied_Optical_Efficiency_pct",
    "Base_Status",
    "Sweep_Status",
    "Output_Power_W",
    "Input_Current_at_Min_V_A",
    "Voltage_Headroom_V",
    "Boost_Duty_Cycle",
    "Driver_Temp_Margin_C",
    "LED_Temp_Margin_C",
    "Max_Ratio",
    "Reason",
]


@dataclass(frozen=True)
class FeasibilityCase:
    case_id: str
    load_name: str
    driver_topology: str
    led_count: int
    led_forward_voltage_nom_v: float
    led_vf_tol_pct: float
    led_current_nom_a: float
    current_tol_pct: float
    duty_cycle: float
    supply_min_v: float
    supply_max_v: float
    driver_dropout_v: float
    driver_efficiency: float
    efficiency_tol_pct: float
    max_input_current_a: float
    max_input_voltage_v: float
    max_output_power_w: float
    board_thermal_resistance_c_per_w: float
    max_driver_case_temp_c: float
    led_thermal_resistance_c_per_w: float
    max_led_junction_temp_c: float
    ambient_temp_c: float
    max_boost_duty_cycle: float


@dataclass(frozen=True)
class FeasibilityResult:
    case_id: str
    load_name: str
    driver_topology: str
    led_string_vf_low_v: float
    led_string_vf_high_v: float
    led_current_high_a: float
    output_power_w: float
    input_power_w: float
    input_current_at_min_v: float
    driver_loss_w: float
    driver_case_temp_c: float
    led_junction_temp_c: float
    voltage_headroom_v: Optional[float]
    boost_duty_cycle: Optional[float]
    input_current_ratio: Optional[float]
    input_voltage_ratio: Optional[float]
    output_power_ratio: Optional[float]
    driver_temp_ratio: Optional[float]
    led_temp_ratio: Optional[float]
    max_ratio: Optional[float]
    driver_temp_margin_c: float
    led_temp_margin_c: float
    status: str
    reason: str
    recommended_next_step: str


@dataclass(frozen=True)
class FeasibilityBundle:
    cases: List[FeasibilityCase]
    results: List[FeasibilityResult]
    warnings: List[str]


@dataclass(frozen=True)
class SensitivityRow:
    sweep_name: str
    variable_name: str
    sweep_setting_label: str
    base_value: float
    sweep_value: float
    sweep_unit: str
    case_id: str
    load_name: str
    driver_topology: str
    applied_ambient_temp_c: float
    applied_led_current_a: float
    applied_board_thermal_resistance_c_per_w: float
    applied_led_thermal_resistance_c_per_w: float
    applied_optical_efficiency_pct: Optional[float]
    base_status: str
    sweep_status: str
    output_power_w: float
    input_current_at_min_v: float
    voltage_headroom_v: Optional[float]
    boost_duty_cycle: Optional[float]
    driver_temp_margin_c: float
    led_temp_margin_c: float
    max_ratio: Optional[float]
    reason: str


def run_from_csv(path: Path) -> FeasibilityBundle:
    cases, warnings = load_cases(path)
    results = [calculate_case(case) for case in cases]
    return FeasibilityBundle(cases=cases, results=results, warnings=warnings)


def load_cases(path: Path) -> Tuple[List[FeasibilityCase], List[str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing synthetic input CSV: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = sorted(REQUIRED_COLUMNS - fieldnames)
        if missing_columns:
            joined = ", ".join(missing_columns)
            raise ValueError(f"{path.name} is missing required columns: {joined}")
        rows = [_strip_row(row) for row in reader]

    warnings: List[str] = []
    cases: List[FeasibilityCase] = []
    for index, row in enumerate(rows, start=2):
        parsed = _parse_case(row, index, warnings)
        if parsed is not None:
            cases.append(parsed)
    return cases, warnings


def calculate_case(case: FeasibilityCase) -> FeasibilityResult:
    led_string_vf_nom_v = case.led_count * case.led_forward_voltage_nom_v
    led_string_vf_low_v = led_string_vf_nom_v * (1.0 - _pct(case.led_vf_tol_pct))
    led_string_vf_high_v = led_string_vf_nom_v * (1.0 + _pct(case.led_vf_tol_pct))
    led_current_high_a = case.led_current_nom_a * (1.0 + _pct(case.current_tol_pct))
    output_power_w = led_string_vf_high_v * led_current_high_a * case.duty_cycle
    efficiency_low = case.driver_efficiency * (1.0 - _pct(case.efficiency_tol_pct))

    if _is_linear(case.driver_topology):
        input_current_at_min_v = led_current_high_a * case.duty_cycle
        driver_loss_w = max(case.supply_max_v - led_string_vf_low_v, 0.0) * input_current_at_min_v
        input_power_w = output_power_w + driver_loss_w
    else:
        input_power_w = output_power_w / efficiency_low
        input_current_at_min_v = input_power_w / case.supply_min_v
        driver_loss_w = max(input_power_w - output_power_w, 0.0)

    driver_case_temp_c = case.ambient_temp_c + (
        driver_loss_w * case.board_thermal_resistance_c_per_w
    )
    led_junction_temp_c = case.ambient_temp_c + (
        output_power_w / case.led_count * case.led_thermal_resistance_c_per_w
    )

    voltage_headroom_v: Optional[float]
    boost_duty_cycle: Optional[float]
    if _is_boost(case.driver_topology):
        voltage_headroom_v = None
        boost_duty_cycle = max(0.0, 1.0 - (case.supply_min_v * efficiency_low / led_string_vf_high_v))
    else:
        voltage_headroom_v = case.supply_min_v - led_string_vf_high_v - case.driver_dropout_v
        boost_duty_cycle = None

    ratio_checks = {
        "input current": _safe_ratio(input_current_at_min_v, case.max_input_current_a),
        "input voltage": _safe_ratio(case.supply_max_v, case.max_input_voltage_v),
        "output power": _safe_ratio(output_power_w, case.max_output_power_w),
        "driver case temperature": _safe_ratio(driver_case_temp_c, case.max_driver_case_temp_c),
        "LED junction temperature": _safe_ratio(led_junction_temp_c, case.max_led_junction_temp_c),
    }
    max_ratio = _max_known_ratio(ratio_checks.values())
    driver_temp_margin_c = case.max_driver_case_temp_c - driver_case_temp_c
    led_temp_margin_c = case.max_led_junction_temp_c - led_junction_temp_c
    status, reason = _classify_result(
        case=case,
        ratio_checks=ratio_checks,
        voltage_headroom_v=voltage_headroom_v,
        boost_duty_cycle=boost_duty_cycle,
        driver_temp_margin_c=driver_temp_margin_c,
        led_temp_margin_c=led_temp_margin_c,
    )

    return FeasibilityResult(
        case_id=case.case_id,
        load_name=case.load_name,
        driver_topology=case.driver_topology,
        led_string_vf_low_v=led_string_vf_low_v,
        led_string_vf_high_v=led_string_vf_high_v,
        led_current_high_a=led_current_high_a,
        output_power_w=output_power_w,
        input_power_w=input_power_w,
        input_current_at_min_v=input_current_at_min_v,
        driver_loss_w=driver_loss_w,
        driver_case_temp_c=driver_case_temp_c,
        led_junction_temp_c=led_junction_temp_c,
        voltage_headroom_v=voltage_headroom_v,
        boost_duty_cycle=boost_duty_cycle,
        input_current_ratio=ratio_checks["input current"],
        input_voltage_ratio=ratio_checks["input voltage"],
        output_power_ratio=ratio_checks["output power"],
        driver_temp_ratio=ratio_checks["driver case temperature"],
        led_temp_ratio=ratio_checks["LED junction temperature"],
        max_ratio=max_ratio,
        driver_temp_margin_c=driver_temp_margin_c,
        led_temp_margin_c=led_temp_margin_c,
        status=status,
        reason=reason,
        recommended_next_step=_recommended_next_step(status),
    )


def write_markdown_summary(
    path: Path,
    results: Sequence[FeasibilityResult],
    warnings: Sequence[str],
    input_path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_build_markdown_summary(results, warnings, input_path), encoding="utf-8")


def write_csv_summary(path: Path, results: Sequence[FeasibilityResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "Synthetic_Label",
        "Human_Review_Note",
        "Publication_Classification",
        "Case_ID",
        "Load_Name",
        "Driver_Topology",
        "Output_Power_W",
        "Input_Current_at_Min_V_A",
        "Voltage_Headroom_V",
        "Boost_Duty_Cycle",
        "Driver_Case_Temp_C",
        "LED_Junction_Temp_C",
        "Max_Ratio",
        "Status",
        "Reason",
        "Recommended_Next_Step",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "Synthetic_Label": SYNTHETIC_LABEL,
                    "Human_Review_Note": HUMAN_REVIEW_NOTE,
                    "Publication_Classification": "Needs review",
                    "Case_ID": result.case_id,
                    "Load_Name": result.load_name,
                    "Driver_Topology": result.driver_topology,
                    "Output_Power_W": f"{result.output_power_w:.3f}",
                    "Input_Current_at_Min_V_A": f"{result.input_current_at_min_v:.3f}",
                    "Voltage_Headroom_V": _fmt_optional(result.voltage_headroom_v),
                    "Boost_Duty_Cycle": _fmt_optional(result.boost_duty_cycle),
                    "Driver_Case_Temp_C": f"{result.driver_case_temp_c:.1f}",
                    "LED_Junction_Temp_C": f"{result.led_junction_temp_c:.1f}",
                    "Max_Ratio": _fmt_optional(result.max_ratio),
                    "Status": result.status,
                    "Reason": result.reason,
                    "Recommended_Next_Step": result.recommended_next_step,
                }
            )


def write_plots(path: Path, results: Sequence[FeasibilityResult]) -> List[Path]:
    path.mkdir(parents=True, exist_ok=True)
    labels = [_case_short_label(result.case_id) for result in results]

    thermal_path = path / "thermal_margin_by_case.png"
    _write_bar_chart(
        thermal_path,
        title="THERMAL MARGIN BY CASE",
        labels=labels,
        series=[
            ("DRIVER C", [result.driver_temp_margin_c for result in results], DRIVER_COLOR),
            ("LED TJ C", [result.led_temp_margin_c for result in results], LED_COLOR),
        ],
        y_label="MARGIN C",
    )

    current_path = path / "current_margin_by_case.png"
    _write_bar_chart(
        current_path,
        title="CURRENT MARGIN BY CASE",
        labels=labels,
        series=[
            (
                "INPUT CURRENT PCT",
                [
                    (1.0 - (result.input_current_ratio or 0.0)) * 100.0
                    for result in results
                ],
                CURRENT_COLOR,
            ),
        ],
        y_label="MARGIN PCT",
    )

    status_counts = Counter(result.status for result in results)
    status_path = path / "feasibility_status_count.png"
    _write_bar_chart(
        status_path,
        title="FEASIBILITY STATUS COUNT",
        labels=[PASS_STATUS.upper(), MARGINAL_STATUS.upper(), FAIL_STATUS.upper()],
        series=[
            (
                "COUNT",
                [
                    float(status_counts.get(PASS_STATUS, 0)),
                    float(status_counts.get(MARGINAL_STATUS, 0)),
                    float(status_counts.get(FAIL_STATUS, 0)),
                ],
                PASS_COLOR,
            )
        ],
        y_label="COUNT",
        status_colors=[PASS_COLOR, MARGINAL_COLOR, FAIL_COLOR],
    )

    return [thermal_path, current_path, status_path]


def write_screenshot_capture_summary(
    path: Path,
    results: Sequence[FeasibilityResult],
    plot_paths: Sequence[Path],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts = Counter(result.status for result in results)
    lines = [
        "# Screenshot Capture Summary",
        "",
        SYNTHETIC_LABEL,
        "",
        f"> {HUMAN_REVIEW_NOTE}",
        "",
        "Publication classification: Needs review",
        "",
        "## Capture Intent",
        "",
        "This file is a screenshot-ready portfolio artifact for the deterministic lighting feasibility mini-simulator. It uses synthetic data only and represents feasibility screening, not design approval.",
        "",
        "## Portfolio Panels",
        "",
        "- Feasibility status count",
        "- Thermal margin by synthetic case",
        "- Current margin by synthetic case",
        "- Summary table with review reasons",
        "",
        "## Plot Assets",
        "",
    ]
    for plot_path in plot_paths:
        lines.append(f"- `{plot_path.as_posix()}`")

    lines.extend(
        [
            "",
            "## Status Counts",
            "",
            f"- {PASS_STATUS}: {status_counts.get(PASS_STATUS, 0)}",
            f"- {MARGINAL_STATUS}: {status_counts.get(MARGINAL_STATUS, 0)}",
            f"- {FAIL_STATUS}: {status_counts.get(FAIL_STATUS, 0)}",
            "",
            "## Summary Table",
            "",
            "| Case | Status | Review Reason |",
            "|---|---|---|",
        ]
    )
    for result in results:
        lines.append(f"| {result.case_id} | {result.status} | {result.reason} |")

    lines.extend(
        [
            "",
            "## Capture Notes",
            "",
            "- Capture this Markdown and the PNG plots only after confirming the synthetic-data disclaimer remains visible.",
            "- Do not crop out the human-review note in public portfolio screenshots.",
            "- Keep any future UI screenshots synthetic and free of proprietary identifiers.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_sensitivity_sweeps(cases: Sequence[FeasibilityCase]) -> List[SensitivityRow]:
    base_results = {case.case_id: calculate_case(case) for case in cases}
    rows: List[SensitivityRow] = []

    for case in cases:
        base_result = base_results[case.case_id]

        for ambient_c in AMBIENT_TEMPERATURE_SWEEP_C:
            variant = replace(case, ambient_temp_c=ambient_c)
            rows.append(
                _make_sensitivity_row(
                    case=case,
                    variant=variant,
                    base_result=base_result,
                    sweep_name="ambient_temperature_sweep",
                    variable_name="ambient_temperature_c",
                    sweep_setting_label=f"{ambient_c:.0f}C",
                    base_value=case.ambient_temp_c,
                    sweep_value=ambient_c,
                    sweep_unit="C",
                    optical_efficiency_pct=None,
                )
            )

        for factor in LED_CURRENT_SWEEP_FACTORS:
            current_a = case.led_current_nom_a * factor
            variant = replace(case, led_current_nom_a=current_a)
            rows.append(
                _make_sensitivity_row(
                    case=case,
                    variant=variant,
                    base_result=base_result,
                    sweep_name="led_current_sweep",
                    variable_name="led_current_a",
                    sweep_setting_label=f"{factor * 100:.0f}%",
                    base_value=case.led_current_nom_a,
                    sweep_value=current_a,
                    sweep_unit="A",
                    optical_efficiency_pct=None,
                )
            )

        for factor in THERMAL_RESISTANCE_SWEEP_FACTORS:
            board_r = case.board_thermal_resistance_c_per_w * factor
            led_r = case.led_thermal_resistance_c_per_w * factor
            variant = replace(
                case,
                board_thermal_resistance_c_per_w=board_r,
                led_thermal_resistance_c_per_w=led_r,
            )
            rows.append(
                _make_sensitivity_row(
                    case=case,
                    variant=variant,
                    base_result=base_result,
                    sweep_name="thermal_resistance_sweep",
                    variable_name="thermal_resistance_c_per_w",
                    sweep_setting_label=f"{factor * 100:.0f}%",
                    base_value=case.board_thermal_resistance_c_per_w,
                    sweep_value=board_r,
                    sweep_unit="C/W",
                    optical_efficiency_pct=None,
                )
            )

        for efficiency_pct in OPTICAL_EFFICIENCY_SWEEP_PCT:
            current_multiplier = 100.0 / efficiency_pct
            current_a = case.led_current_nom_a * current_multiplier
            variant = replace(case, led_current_nom_a=current_a)
            rows.append(
                _make_sensitivity_row(
                    case=case,
                    variant=variant,
                    base_result=base_result,
                    sweep_name="optical_efficiency_sweep",
                    variable_name="optical_efficiency_percent",
                    sweep_setting_label=f"{efficiency_pct:.0f}%",
                    base_value=100.0,
                    sweep_value=efficiency_pct,
                    sweep_unit="%",
                    optical_efficiency_pct=efficiency_pct,
                )
            )

    return rows


def write_sensitivity_outputs(path: Path, rows: Sequence[SensitivityRow]) -> List[Path]:
    path.mkdir(parents=True, exist_ok=True)
    outputs = [
        path / "sensitivity_summary.csv",
        path / "ambient_temperature_sweep.csv",
        path / "led_current_sweep.csv",
        path / "thermal_resistance_sweep.csv",
        path / "optical_efficiency_sweep.csv",
        path / "sensitivity_summary.md",
    ]

    write_sensitivity_csv(outputs[0], rows)
    for sweep_name, output_path in (
        ("ambient_temperature_sweep", outputs[1]),
        ("led_current_sweep", outputs[2]),
        ("thermal_resistance_sweep", outputs[3]),
        ("optical_efficiency_sweep", outputs[4]),
    ):
        write_sensitivity_csv(output_path, _filter_sweep(rows, sweep_name))

    outputs[5].write_text(_build_sensitivity_summary(rows), encoding="utf-8")
    outputs.extend(write_sensitivity_plots(path / "plots", rows))
    return outputs


def write_sensitivity_csv(path: Path, rows: Sequence[SensitivityRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SENSITIVITY_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(_sensitivity_row_to_csv(row))


def write_sensitivity_plots(path: Path, rows: Sequence[SensitivityRow]) -> List[Path]:
    path.mkdir(parents=True, exist_ok=True)
    plot_specs = [
        (
            "ambient_temperature_sweep",
            path / "ambient_temperature_sweep.png",
            "AMBIENT TEMP SWEEP",
        ),
        ("led_current_sweep", path / "led_current_sweep.png", "LED CURRENT SWEEP"),
        (
            "thermal_resistance_sweep",
            path / "thermal_resistance_sweep.png",
            "THERMAL RES SWEEP",
        ),
        (
            "optical_efficiency_sweep",
            path / "optical_efficiency_sweep.png",
            "OPTICAL EFF SWEEP",
        ),
    ]
    outputs: List[Path] = []
    for sweep_name, output_path, title in plot_specs:
        sweep_rows = _filter_sweep(rows, sweep_name)
        labels = _ordered_sweep_labels(sweep_rows)
        status_counts = _status_counts_by_label(sweep_rows, labels)
        _write_bar_chart(
            output_path,
            title=title,
            labels=labels,
            series=[
                ("PASS", [float(status_counts[label].get(PASS_STATUS, 0)) for label in labels], PASS_COLOR),
                (
                    "MARGINAL",
                    [float(status_counts[label].get(MARGINAL_STATUS, 0)) for label in labels],
                    MARGINAL_COLOR,
                ),
                ("FAIL", [float(status_counts[label].get(FAIL_STATUS, 0)) for label in labels], FAIL_COLOR),
            ],
            y_label="CASE COUNT",
        )
        outputs.append(output_path)
    return outputs


def _make_sensitivity_row(
    case: FeasibilityCase,
    variant: FeasibilityCase,
    base_result: FeasibilityResult,
    sweep_name: str,
    variable_name: str,
    sweep_setting_label: str,
    base_value: float,
    sweep_value: float,
    sweep_unit: str,
    optical_efficiency_pct: Optional[float],
) -> SensitivityRow:
    result = calculate_case(variant)
    return SensitivityRow(
        sweep_name=sweep_name,
        variable_name=variable_name,
        sweep_setting_label=sweep_setting_label,
        base_value=base_value,
        sweep_value=sweep_value,
        sweep_unit=sweep_unit,
        case_id=case.case_id,
        load_name=case.load_name,
        driver_topology=case.driver_topology,
        applied_ambient_temp_c=variant.ambient_temp_c,
        applied_led_current_a=variant.led_current_nom_a,
        applied_board_thermal_resistance_c_per_w=variant.board_thermal_resistance_c_per_w,
        applied_led_thermal_resistance_c_per_w=variant.led_thermal_resistance_c_per_w,
        applied_optical_efficiency_pct=optical_efficiency_pct,
        base_status=base_result.status,
        sweep_status=result.status,
        output_power_w=result.output_power_w,
        input_current_at_min_v=result.input_current_at_min_v,
        voltage_headroom_v=result.voltage_headroom_v,
        boost_duty_cycle=result.boost_duty_cycle,
        driver_temp_margin_c=result.driver_temp_margin_c,
        led_temp_margin_c=result.led_temp_margin_c,
        max_ratio=result.max_ratio,
        reason=result.reason,
    )


def _sensitivity_row_to_csv(row: SensitivityRow) -> Dict[str, str]:
    return {
        "Synthetic_Label": SYNTHETIC_LABEL,
        "Human_Review_Note": HUMAN_REVIEW_NOTE,
        "Publication_Classification": "Needs review",
        "Engineering_Review_Required": "Yes - synthetic thresholds require qualified engineering review.",
        "Sweep_Name": row.sweep_name,
        "Variable_Name": row.variable_name,
        "Sweep_Setting_Label": row.sweep_setting_label,
        "Base_Value": f"{row.base_value:.4f}",
        "Sweep_Value": f"{row.sweep_value:.4f}",
        "Sweep_Unit": row.sweep_unit,
        "Case_ID": row.case_id,
        "Load_Name": row.load_name,
        "Driver_Topology": row.driver_topology,
        "Applied_Ambient_Temp_C": f"{row.applied_ambient_temp_c:.2f}",
        "Applied_LED_Current_A": f"{row.applied_led_current_a:.4f}",
        "Applied_Board_Thermal_Resistance_C_per_W": (
            f"{row.applied_board_thermal_resistance_c_per_w:.4f}"
        ),
        "Applied_LED_Thermal_Resistance_C_per_W": (
            f"{row.applied_led_thermal_resistance_c_per_w:.4f}"
        ),
        "Applied_Optical_Efficiency_pct": _fmt_optional(row.applied_optical_efficiency_pct),
        "Base_Status": row.base_status,
        "Sweep_Status": row.sweep_status,
        "Output_Power_W": f"{row.output_power_w:.3f}",
        "Input_Current_at_Min_V_A": f"{row.input_current_at_min_v:.3f}",
        "Voltage_Headroom_V": _fmt_optional(row.voltage_headroom_v),
        "Boost_Duty_Cycle": _fmt_optional(row.boost_duty_cycle),
        "Driver_Temp_Margin_C": f"{row.driver_temp_margin_c:.2f}",
        "LED_Temp_Margin_C": f"{row.led_temp_margin_c:.2f}",
        "Max_Ratio": _fmt_optional(row.max_ratio),
        "Reason": row.reason,
    }


def _build_sensitivity_summary(rows: Sequence[SensitivityRow]) -> str:
    status_counts = Counter(row.sweep_status for row in rows)
    lines = [
        "# Sensitivity Sweep Summary",
        "",
        SYNTHETIC_LABEL,
        "",
        f"> {HUMAN_REVIEW_NOTE}",
        "",
        "## Purpose",
        "",
        "Task 5C adds deterministic sensitivity sweeps to show how synthetic feasibility status changes when selected engineering inputs move across review ranges.",
        "",
        "## Engineering Context",
        "",
        "The sweeps support investigation of lighting feasibility drivers such as ambient temperature, LED current, thermal resistance, and a synthetic relative optical-efficiency factor. They do not approve engineering decisions.",
        "",
        "## Variables Swept",
        "",
        "- `ambient_temperature_c`: ambient temperature values from 75 C to 115 C.",
        "- `led_current_a`: base LED current scaled from 80% to 120%; CSV rows show applied current in A.",
        "- `thermal_resistance_c_per_w`: board and LED thermal resistances scaled from 80% to 120%; CSV rows show applied C/W values.",
        "- `optical_efficiency_percent`: synthetic relative optical efficiency from 70% to 130%; lower values increase LED current for a fixed notional light target.",
        "",
        "## Synthetic Ranges Used",
        "",
        f"- Ambient temperature C: {_join_numbers(AMBIENT_TEMPERATURE_SWEEP_C)}",
        f"- LED current scale factors: {_join_percentages(LED_CURRENT_SWEEP_FACTORS)}",
        f"- Thermal resistance scale factors: {_join_percentages(THERMAL_RESISTANCE_SWEEP_FACTORS)}",
        f"- Optical efficiency percent: {_join_numbers(OPTICAL_EFFICIENCY_SWEEP_PCT)}",
        "",
        "## Outputs",
        "",
        "- `outputs/sensitivity/sensitivity_summary.csv`",
        "- `outputs/sensitivity/ambient_temperature_sweep.csv`",
        "- `outputs/sensitivity/led_current_sweep.csv`",
        "- `outputs/sensitivity/thermal_resistance_sweep.csv`",
        "- `outputs/sensitivity/optical_efficiency_sweep.csv`",
        "- `outputs/sensitivity/plots/ambient_temperature_sweep.png`",
        "- `outputs/sensitivity/plots/led_current_sweep.png`",
        "- `outputs/sensitivity/plots/thermal_resistance_sweep.png`",
        "- `outputs/sensitivity/plots/optical_efficiency_sweep.png`",
        "",
        "## Status Summary",
        "",
        f"- Total sweep rows: {len(rows)}",
        f"- {PASS_STATUS}: {status_counts.get(PASS_STATUS, 0)}",
        f"- {MARGINAL_STATUS}: {status_counts.get(MARGINAL_STATUS, 0)}",
        f"- {FAIL_STATUS}: {status_counts.get(FAIL_STATUS, 0)}",
        "",
        "## Sweep Details",
        "",
        "| Sweep | Rows | Pass | Marginal | Fail | What It Reveals |",
        "|---|---:|---:|---:|---:|---|",
    ]
    reveals = {
        "ambient_temperature_sweep": "Temperature sensitivity of driver and LED thermal margins.",
        "led_current_sweep": "Electrical and thermal sensitivity to current demand.",
        "thermal_resistance_sweep": "Thermal-path sensitivity using scaled C/W assumptions.",
        "optical_efficiency_sweep": "Current-demand sensitivity for a fixed synthetic light target.",
    }
    for sweep_name in (
        "ambient_temperature_sweep",
        "led_current_sweep",
        "thermal_resistance_sweep",
        "optical_efficiency_sweep",
    ):
        sweep_rows = _filter_sweep(rows, sweep_name)
        counts = Counter(row.sweep_status for row in sweep_rows)
        lines.append(
            "| "
            f"{sweep_name} | "
            f"{len(sweep_rows)} | "
            f"{counts.get(PASS_STATUS, 0)} | "
            f"{counts.get(MARGINAL_STATUS, 0)} | "
            f"{counts.get(FAIL_STATUS, 0)} | "
            f"{reveals[sweep_name]} |"
        )

    lines.extend(
        [
            "",
            "## Human Review Controls",
            "",
            "- Review all sweep ranges and thresholds before publication.",
            "- Treat status changes as investigation prompts only.",
            "- Confirm plots and CSV rows remain synthetic and sanitized.",
            "- Do not use sweep output as design approval or engineering signoff.",
            "",
            "## Limitations",
            "",
            "- Sweeps vary one synthetic input family at a time.",
            "- Optical efficiency is modeled as a relative current-demand factor because the base engine does not model optical output.",
            "- Thermal resistance scaling is lumped and does not replace detailed thermal analysis.",
            "- No correlations between variables are modeled.",
            "",
            "## Safe to Publish Status",
            "",
            "Needs review. The ranges and thresholds are synthetic and require qualified engineering review before publication.",
            "",
        ]
    )
    return "\n".join(lines)


def _filter_sweep(rows: Sequence[SensitivityRow], sweep_name: str) -> List[SensitivityRow]:
    return [row for row in rows if row.sweep_name == sweep_name]


def _ordered_sweep_labels(rows: Sequence[SensitivityRow]) -> List[str]:
    labels: List[str] = []
    for row in rows:
        if row.sweep_setting_label not in labels:
            labels.append(row.sweep_setting_label)
    return labels


def _status_counts_by_label(
    rows: Sequence[SensitivityRow], labels: Sequence[str]
) -> Dict[str, Counter]:
    counts = {label: Counter() for label in labels}
    for row in rows:
        counts[row.sweep_setting_label][row.sweep_status] += 1
    return counts


def _join_numbers(values: Sequence[float]) -> str:
    return ", ".join(f"{value:g}" for value in values)


def _join_percentages(values: Sequence[float]) -> str:
    return ", ".join(f"{value * 100:.0f}%" for value in values)


def _build_markdown_summary(
    results: Sequence[FeasibilityResult],
    warnings: Sequence[str],
    input_path: Path,
) -> str:
    status_counts = Counter(result.status for result in results)
    lines: List[str] = [
        "# Automotive Lighting Feasibility Mini-Simulator Summary",
        "",
        SYNTHETIC_LABEL,
        "",
        f"> {HUMAN_REVIEW_NOTE}",
        "",
        "## Problem",
        "",
        "Early lighting feasibility discussions need quick estimates for LED electrical load, driver stress, and thermal margin without presenting the result as design approval.",
        "",
        "## Engineering Context",
        "",
        "The engine screens synthetic automotive lighting load cases using first-pass LED string, driver input, voltage headroom, boost duty, and thermal equations.",
        "",
        "## Workflow",
        "",
        "- Load synthetic input parameters from CSV.",
        "- Calculate worst-case LED string voltage, current, power, driver loss, and temperature estimates.",
        "- Apply deterministic Pass, Marginal, or Fail logic.",
        "- Export markdown and CSV summaries for human review.",
        "",
        "## Inputs",
        "",
        f"- Input CSV: `{input_path.as_posix()}`",
        "- Parameters: LED count, LED forward voltage, current, supply range, topology, efficiency, ratings, thermal resistance, and ambient temperature.",
        "",
        "## Outputs",
        "",
        "- Feasibility status by synthetic case.",
        "- Electrical and thermal calculated values.",
        "- Review reason and recommended next step.",
        "- PNG plot assets under `outputs/plots/`.",
        "- Screenshot-ready capture notes under `outputs/screenshots/`.",
        "- Sensitivity sweep outputs under `outputs/sensitivity/`.",
        "",
        "## Screenshots or Screenshot Placeholders",
        "",
        "- `outputs/screenshots/portfolio_capture_summary.md`",
        "- `outputs/plots/thermal_margin_by_case.png`",
        "- `outputs/plots/current_margin_by_case.png`",
        "- `outputs/plots/feasibility_status_count.png`",
        "",
        "## Sanitized Sample Data",
        "",
        "All case IDs, load names, limits, ratings, and assumptions are synthetic demonstration values. No proprietary organization, program, part, drawing, BOM, harness, cost, validation, controlled source, or restricted design details are included.",
        "",
        "## Human Review Controls",
        "",
        "- Confirm all inputs are synthetic before public use.",
        "- Verify formulas, units, thresholds, and assumptions before using the output in any engineering discussion.",
        "- Treat Pass as a first-pass screen only, not an engineering approval.",
        "- Escalate Marginal and Fail rows to detailed analysis with reviewed assumptions.",
        "",
        "## Codex Contribution",
        "",
        "Codex scaffolded the deterministic Python engine, sample CSV, output writers, and basic tests.",
        "",
        "## Jose Contribution",
        "",
        "Jose defines acceptable first-pass screening equations, engineering interpretation, and final review criteria.",
        "",
        "## AI Fundamentals Demonstrated",
        "",
        "- Deterministic code generation",
        "- Structured data transformation",
        "- Rule-based classification",
        "- Test generation",
        "- Report generation",
        "",
        "## Engineering Skills Demonstrated",
        "",
        "- LED load estimation",
        "- Driver power and current screening",
        "- Voltage headroom review",
        "- Boost duty-cycle screening",
        "- Thermal margin estimation",
        "",
        "## Risks and Mitigations",
        "",
        "- Risk: The simulator could be mistaken for final approval. Mitigation: every output states human review is required.",
        "- Risk: Generic assumptions may not match a real design. Mitigation: use synthetic data only and keep formulas transparent.",
        "- Risk: Marginal cases may be overinterpreted. Mitigation: recommend detailed analysis before design decisions.",
        "",
        "## Next Improvements",
        "",
        "- Add cross-variable sensitivity sweeps after single-variable behavior is reviewed.",
        "- Add reviewed equation annotations from a qualified engineer.",
        "- Add an optional Streamlit shell after equation review.",
        "",
        "## Safe to Publish Status",
        "",
        "Needs review. The data is synthetic, but formulas, limits, thresholds, screenshots, and claims require qualified engineering review before publication.",
        "",
        "## Deterministic Feasibility Policy",
        "",
        "- Fail: any calculated ratio exceeds 1.00, voltage headroom is below 0 V, boost duty exceeds the synthetic maximum, or thermal margin is below 0 C.",
        "- Marginal: any calculated ratio is at least 0.85, voltage headroom is 0.75 V or less, boost duty is at least 85% of the synthetic maximum, or thermal margin is 10 C or less.",
        "- Pass: no fail or marginal triggers are present.",
        "",
        "## Status Summary",
        "",
    ]
    if status_counts:
        for status in (PASS_STATUS, MARGINAL_STATUS, FAIL_STATUS):
            lines.append(f"- {status}: {status_counts.get(status, 0)}")
    else:
        lines.append("- No calculation rows generated.")

    lines.extend(
        [
            "",
            "## Calculation Results",
            "",
            "| Case | Load | Topology | Pout W | Iin @ Min V A | Headroom V | Boost Duty | Driver C | LED Tj C | Max Ratio | Status |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for result in results:
        lines.append(
            "| "
            f"{result.case_id} | "
            f"{result.load_name} | "
            f"{result.driver_topology} | "
            f"{result.output_power_w:.2f} | "
            f"{result.input_current_at_min_v:.3f} | "
            f"{_fmt_optional(result.voltage_headroom_v)} | "
            f"{_fmt_optional(result.boost_duty_cycle)} | "
            f"{result.driver_case_temp_c:.1f} | "
            f"{result.led_junction_temp_c:.1f} | "
            f"{_fmt_optional(result.max_ratio)} | "
            f"{result.status} |"
        )

    lines.extend(
        [
            "",
            "## Review Reasons",
            "",
        ]
    )
    if results:
        for result in results:
            lines.append(f"- {result.case_id}: {result.reason}")
    else:
        lines.append("- No review reasons were generated.")

    lines.extend(
        [
            "",
            "## Warnings",
            "",
        ]
    )
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- No input warnings were generated.")

    lines.extend(
        [
            "",
            "## Proof Gaps",
            "",
            "- Equation set has not yet been independently reviewed.",
            "- PNG plots are generated from synthetic data but have not been design-reviewed.",
            "- Screenshot-ready Markdown is included, but no live UI screenshot exists yet.",
            "- No Streamlit UI is included yet.",
            "- No reviewed signoff record is included yet.",
            "",
        ]
    )
    return "\n".join(lines)


def _write_bar_chart(
    path: Path,
    title: str,
    labels: Sequence[str],
    series: Sequence[Tuple[str, Sequence[float], Tuple[int, int, int]]],
    y_label: str,
    status_colors: Optional[Sequence[Tuple[int, int, int]]] = None,
) -> None:
    canvas = _new_canvas(PLOT_WIDTH, PLOT_HEIGHT, WHITE)
    chart_left = 92
    chart_top = 92
    chart_right = PLOT_WIDTH - 42
    chart_bottom = PLOT_HEIGHT - 86
    plot_width = chart_right - chart_left
    plot_height = chart_bottom - chart_top

    values = [value for _, series_values, _ in series for value in series_values]
    raw_min = min(values) if values else 0.0
    raw_max = max(values) if values else 1.0
    y_min = 0.0 if raw_min >= 0 else min(0.0, raw_min)
    y_max = max(0.0, raw_max)
    if y_min == y_max:
        y_max = y_min + 1.0
    span = y_max - y_min
    if raw_min < 0:
        y_min -= span * 0.10
    y_max += span * 0.16

    def y_for(value: float) -> int:
        normalized = (value - y_min) / (y_max - y_min)
        return int(chart_bottom - normalized * plot_height)

    _draw_text(canvas, 32, 24, title, INK, scale=3)
    _draw_text(canvas, 32, 62, y_label, MUTED, scale=2)

    for index in range(6):
        tick_value = y_min + (y_max - y_min) * index / 5
        y = y_for(tick_value)
        _draw_line(canvas, chart_left, y, chart_right, y, GRID)
        _draw_text(canvas, 28, y - 6, _format_axis_tick(tick_value, y_max - y_min), MUTED, scale=1)

    zero_y = y_for(0.0)
    _draw_line(canvas, chart_left, chart_top, chart_left, chart_bottom, INK)
    _draw_line(canvas, chart_left, zero_y, chart_right, zero_y, INK)

    if not labels:
        _draw_text(canvas, chart_left + 24, chart_top + 120, "NO DATA", FAIL_COLOR, scale=3)
        _write_png(path, canvas)
        return

    group_width = plot_width / len(labels)
    series_count = max(len(series), 1)
    bar_width = max(16, min(54, int(group_width / (series_count + 1.6))))

    for label_index, label in enumerate(labels):
        group_start = int(chart_left + label_index * group_width)
        total_bar_width = bar_width * series_count
        x_start = group_start + int((group_width - total_bar_width) / 2)
        for series_index, (_, series_values, color) in enumerate(series):
            value = series_values[label_index] if label_index < len(series_values) else 0.0
            bar_color = color
            if status_colors is not None and label_index < len(status_colors):
                bar_color = status_colors[label_index]
            x0 = x_start + series_index * bar_width
            x1 = x0 + bar_width - 5
            y_value = y_for(value)
            y0 = min(y_value, zero_y)
            y1 = max(y_value, zero_y)
            _draw_rect(canvas, x0, y0, x1, y1, bar_color)
            label_y = y0 - 16 if value >= 0 else y1 + 6
            _draw_text(canvas, x0 - 2, label_y, f"{value:.1f}", INK, scale=1)
        _draw_text(canvas, group_start + 12, chart_bottom + 18, label, INK, scale=2)

    legend_x = chart_left
    legend_y = PLOT_HEIGHT - 38
    for legend_label, _, color in series:
        _draw_rect(canvas, legend_x, legend_y, legend_x + 18, legend_y + 18, color)
        _draw_text(canvas, legend_x + 26, legend_y + 2, legend_label, INK, scale=2)
        legend_x += 210

    _write_png(path, canvas)


def _new_canvas(width: int, height: int, color: Tuple[int, int, int]) -> List[List[Tuple[int, int, int]]]:
    return [[color for _ in range(width)] for _ in range(height)]


def _draw_rect(
    canvas: List[List[Tuple[int, int, int]]],
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: Tuple[int, int, int],
) -> None:
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


def _draw_line(
    canvas: List[List[Tuple[int, int, int]]],
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: Tuple[int, int, int],
) -> None:
    if y0 == y1:
        _draw_rect(canvas, x0, y0, x1, y1, color)
        return
    if x0 == x1:
        _draw_rect(canvas, x0, y0, x1, y1, color)
        return
    steps = max(abs(x1 - x0), abs(y1 - y0))
    for step in range(steps + 1):
        x = round(x0 + (x1 - x0) * step / steps)
        y = round(y0 + (y1 - y0) * step / steps)
        _draw_rect(canvas, x, y, x, y, color)


def _draw_text(
    canvas: List[List[Tuple[int, int, int]]],
    x: int,
    y: int,
    text: str,
    color: Tuple[int, int, int],
    scale: int = 1,
) -> None:
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


def _write_png(path: Path, canvas: List[List[Tuple[int, int, int]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    height = len(canvas)
    width = len(canvas[0])
    raw_rows = []
    for row in canvas:
        raw_rows.append(b"\x00" + b"".join(bytes(pixel) for pixel in row))
    compressed = zlib.compress(b"".join(raw_rows), level=9)

    def chunk(kind: bytes, data: bytes) -> bytes:
        checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)

    png = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
            chunk(b"IDAT", compressed),
            chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(png)


def _case_short_label(case_id: str) -> str:
    return case_id.replace("SYN-LGT-", "")


def _format_axis_tick(value: float, span: float) -> str:
    if abs(value) < 0.05:
        value = 0.0
    if span <= 5:
        return f"{value:.1f}"
    return f"{value:.0f}"


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


def _classify_result(
    case: FeasibilityCase,
    ratio_checks: Dict[str, Optional[float]],
    voltage_headroom_v: Optional[float],
    boost_duty_cycle: Optional[float],
    driver_temp_margin_c: float,
    led_temp_margin_c: float,
) -> Tuple[str, str]:
    fail_reasons: List[str] = []
    marginal_reasons: List[str] = []

    for label, ratio in ratio_checks.items():
        if ratio is None:
            fail_reasons.append(f"{label} ratio could not be calculated")
        elif ratio > LIMIT_RATIO:
            fail_reasons.append(f"{label} ratio {ratio:.2f} exceeds 1.00")
        elif ratio >= MARGINAL_RATIO:
            marginal_reasons.append(f"{label} ratio {ratio:.2f} is at or above 0.85")

    if voltage_headroom_v is not None:
        if voltage_headroom_v < 0:
            fail_reasons.append(f"voltage headroom {voltage_headroom_v:.2f} V is below 0 V")
        elif voltage_headroom_v <= MARGINAL_VOLTAGE_HEADROOM_V:
            marginal_reasons.append(f"voltage headroom {voltage_headroom_v:.2f} V is 0.75 V or less")

    if boost_duty_cycle is not None:
        if boost_duty_cycle > case.max_boost_duty_cycle:
            fail_reasons.append(
                f"boost duty {boost_duty_cycle:.2f} exceeds synthetic max {case.max_boost_duty_cycle:.2f}"
            )
        elif boost_duty_cycle >= case.max_boost_duty_cycle * MARGINAL_RATIO:
            marginal_reasons.append(
                f"boost duty {boost_duty_cycle:.2f} is near synthetic max {case.max_boost_duty_cycle:.2f}"
            )

    if driver_temp_margin_c < 0:
        fail_reasons.append(f"driver thermal margin {driver_temp_margin_c:.1f} C is below 0 C")
    elif driver_temp_margin_c <= MARGINAL_TEMPERATURE_MARGIN_C:
        marginal_reasons.append(
            f"driver thermal margin {driver_temp_margin_c:.1f} C is 10 C or less"
        )

    if led_temp_margin_c < 0:
        fail_reasons.append(f"LED junction margin {led_temp_margin_c:.1f} C is below 0 C")
    elif led_temp_margin_c <= MARGINAL_TEMPERATURE_MARGIN_C:
        marginal_reasons.append(f"LED junction margin {led_temp_margin_c:.1f} C is 10 C or less")

    if fail_reasons:
        return FAIL_STATUS, "; ".join(fail_reasons)
    if marginal_reasons:
        return MARGINAL_STATUS, "; ".join(marginal_reasons)
    return PASS_STATUS, "All deterministic synthetic feasibility checks are below marginal limits."


def _parse_case(row: Dict[str, str], row_number: int, warnings: List[str]) -> Optional[FeasibilityCase]:
    case_id = row.get("Case_ID", "").strip() or f"UNKNOWN-ROW-{row_number}"
    load_name = row.get("Load_Name", "").strip()
    driver_topology = row.get("Driver_Topology", "").strip()
    if not load_name:
        warnings.append(f"{case_id}: Load_Name is blank; row skipped.")
        return None
    if not driver_topology:
        warnings.append(f"{case_id}: Driver_Topology is blank; row skipped.")
        return None

    parsed = {
        field: _float(row.get(field), case_id, field, warnings)
        for field in sorted(REQUIRED_COLUMNS - {"Case_ID", "Load_Name", "Driver_Topology"})
    }
    if any(value is None for value in parsed.values()):
        warnings.append(f"{case_id}: required numeric input is missing or invalid; row skipped.")
        return None

    led_count_float = parsed["LED_Count"]
    assert led_count_float is not None
    led_count = int(led_count_float)
    if led_count_float != led_count or led_count <= 0:
        warnings.append(f"{case_id}: LED_Count must be a positive whole number; row skipped.")
        return None

    case = FeasibilityCase(
        case_id=case_id,
        load_name=load_name,
        driver_topology=driver_topology,
        led_count=led_count,
        led_forward_voltage_nom_v=_known(parsed["LED_Forward_Voltage_Nom_V"]),
        led_vf_tol_pct=_known(parsed["LED_VF_Tol_pct"]),
        led_current_nom_a=_known(parsed["LED_Current_Nom_A"]),
        current_tol_pct=_known(parsed["Current_Tol_pct"]),
        duty_cycle=_known(parsed["Duty_Cycle"]),
        supply_min_v=_known(parsed["VSupply_Min_V"]),
        supply_max_v=_known(parsed["VSupply_Max_V"]),
        driver_dropout_v=_known(parsed["Driver_Dropout_V"]),
        driver_efficiency=_known(parsed["Driver_Efficiency"]),
        efficiency_tol_pct=_known(parsed["Efficiency_Tol_pct"]),
        max_input_current_a=_known(parsed["Max_Input_Current_A"]),
        max_input_voltage_v=_known(parsed["Max_Input_Voltage_V"]),
        max_output_power_w=_known(parsed["Max_Output_Power_W"]),
        board_thermal_resistance_c_per_w=_known(parsed["Board_Thermal_Resistance_C_per_W"]),
        max_driver_case_temp_c=_known(parsed["Max_Driver_Case_Temp_C"]),
        led_thermal_resistance_c_per_w=_known(parsed["LED_Thermal_Resistance_C_per_W"]),
        max_led_junction_temp_c=_known(parsed["Max_LED_Junction_Temp_C"]),
        ambient_temp_c=_known(parsed["Ambient_Temp_C"]),
        max_boost_duty_cycle=_known(parsed["Max_Boost_Duty_Cycle"]),
    )

    validation_errors = _validate_case(case)
    if validation_errors:
        for error in validation_errors:
            warnings.append(f"{case.case_id}: {error}; row skipped.")
        return None
    return case


def _validate_case(case: FeasibilityCase) -> List[str]:
    errors: List[str] = []
    positive_fields = {
        "LED_Forward_Voltage_Nom_V": case.led_forward_voltage_nom_v,
        "LED_Current_Nom_A": case.led_current_nom_a,
        "VSupply_Min_V": case.supply_min_v,
        "VSupply_Max_V": case.supply_max_v,
        "Driver_Efficiency": case.driver_efficiency,
        "Max_Input_Current_A": case.max_input_current_a,
        "Max_Input_Voltage_V": case.max_input_voltage_v,
        "Max_Output_Power_W": case.max_output_power_w,
        "Board_Thermal_Resistance_C_per_W": case.board_thermal_resistance_c_per_w,
        "Max_Driver_Case_Temp_C": case.max_driver_case_temp_c,
        "LED_Thermal_Resistance_C_per_W": case.led_thermal_resistance_c_per_w,
        "Max_LED_Junction_Temp_C": case.max_led_junction_temp_c,
        "Max_Boost_Duty_Cycle": case.max_boost_duty_cycle,
    }
    for field, value in positive_fields.items():
        if value <= 0:
            errors.append(f"{field} must be greater than zero")
    if case.driver_dropout_v < 0:
        errors.append("Driver_Dropout_V must be zero or greater")
    if case.supply_max_v < case.supply_min_v:
        errors.append("VSupply_Max_V must be greater than or equal to VSupply_Min_V")
    if not 0 < case.duty_cycle <= 1:
        errors.append("Duty_Cycle must be greater than 0 and no more than 1")
    if not 0 < case.driver_efficiency <= 1:
        errors.append("Driver_Efficiency must be greater than 0 and no more than 1")
    if case.driver_efficiency * (1.0 - _pct(case.efficiency_tol_pct)) <= 0:
        errors.append("low-corner driver efficiency must be greater than zero")
    if not 0 < case.max_boost_duty_cycle < 1:
        errors.append("Max_Boost_Duty_Cycle must be greater than 0 and less than 1")
    return errors


def _recommended_next_step(status: str) -> str:
    if status == FAIL_STATUS:
        return "Revise topology, LED count, current, thermal path, or ratings before deeper analysis."
    if status == MARGINAL_STATUS:
        return "Run sensitivity sweep and review thermal/electrical margins."
    return "Keep as first-pass candidate and verify assumptions during detailed review."


def _strip_row(row: Dict[str, str]) -> Dict[str, str]:
    return {
        (key or "").strip(): (value or "").strip()
        for key, value in row.items()
        if key is not None
    }


def _float(value: Optional[str], row_id: str, field: str, warnings: List[str]) -> Optional[float]:
    if value is None or value == "":
        warnings.append(f"{row_id}: field {field} is blank.")
        return None
    try:
        return float(value)
    except ValueError:
        warnings.append(f"{row_id}: field {field} has invalid numeric value {value!r}.")
        return None


def _known(value: Optional[float]) -> float:
    if value is None:
        raise ValueError("Expected parsed numeric value.")
    return value


def _is_linear(topology: str) -> bool:
    return "linear" in topology.lower()


def _is_boost(topology: str) -> bool:
    return "boost" in topology.lower()


def _safe_ratio(value: float, rating: float) -> Optional[float]:
    if rating <= 0:
        return None
    return value / rating


def _max_known_ratio(ratios: Iterable[Optional[float]]) -> Optional[float]:
    known = [ratio for ratio in ratios if ratio is not None]
    if not known:
        return None
    return max(known)


def _pct(value: float) -> float:
    return value / 100.0


def _fmt_optional(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the synthetic automotive lighting feasibility mini-simulator."
    )
    parser.add_argument("--input", type=Path, default=Path("data/synthetic_lighting_cases.csv"))
    parser.add_argument("--markdown", type=Path, default=Path("outputs/feasibility_summary.md"))
    parser.add_argument("--csv", type=Path, default=Path("outputs/feasibility_summary.csv"))
    parser.add_argument("--plots-dir", type=Path, default=Path("outputs/plots"))
    parser.add_argument("--screenshots-dir", type=Path, default=Path("outputs/screenshots"))
    parser.add_argument("--sensitivity-dir", type=Path, default=Path("outputs/sensitivity"))
    parser.add_argument("--skip-sweeps", action="store_true")
    args = parser.parse_args()

    bundle = run_from_csv(args.input)
    write_markdown_summary(args.markdown, bundle.results, bundle.warnings, args.input)
    write_csv_summary(args.csv, bundle.results)
    plot_paths = write_plots(args.plots_dir, bundle.results)
    screenshot_path = args.screenshots_dir / "portfolio_capture_summary.md"
    write_screenshot_capture_summary(screenshot_path, bundle.results, plot_paths)
    sensitivity_rows: List[SensitivityRow] = []
    if not args.skip_sweeps:
        sensitivity_rows = run_sensitivity_sweeps(bundle.cases)
        write_sensitivity_outputs(args.sensitivity_dir, sensitivity_rows)

    print(f"Synthetic cases loaded: {len(bundle.cases)}")
    print(f"Feasibility rows generated: {len(bundle.results)}")
    print(f"Sensitivity rows generated: {len(sensitivity_rows)}")
    print(f"Warnings: {len(bundle.warnings)}")
    print(f"Markdown summary: {args.markdown}")
    print(f"CSV summary: {args.csv}")
    print(f"Plots: {args.plots_dir}")
    print(f"Screenshot capture summary: {screenshot_path}")
    if not args.skip_sweeps:
        print(f"Sensitivity outputs: {args.sensitivity_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
