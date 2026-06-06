"""CSV summary helpers for synthetic WCCA proof assets."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from .calculations import WccaResult


SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_NOTE = (
    "Human Review Required: AI-generated outputs are decision-support artifacts only. "
    "A qualified engineer owns final review and approval."
)

SUMMARY_COLUMNS = [
    "Synthetic_Label",
    "Human_Review_Note",
    "Publication_Classification",
    "Case_ID",
    "Condition_ID",
    "Topology",
    "VIN_V",
    "Ambient_Temp_C",
    "LED_Current_High_A",
    "LED_VF_High_V",
    "Output_Power_W",
    "Input_Current_A",
    "Switch_Current_Stress_A",
    "Inductor_Current_Stress_A",
    "Thermal_Loss_W",
    "Junction_Temp_C",
    "Max_Ratio",
    "Margin_pct",
    "Pass_Fail_Status",
    "Review_Status",
    "Review_Reason",
]


def write_summary_csv(path: Path, results: Sequence[WccaResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for result in results:
            writer.writerow(result_to_summary_row(result))


def result_to_summary_row(result: WccaResult) -> Dict[str, str]:
    return {
        "Synthetic_Label": SYNTHETIC_LABEL,
        "Human_Review_Note": HUMAN_REVIEW_NOTE,
        "Publication_Classification": "Needs review",
        "Case_ID": result.case_id,
        "Condition_ID": result.condition_id,
        "Topology": result.topology,
        "VIN_V": f"{result.vin_v:.2f}",
        "Ambient_Temp_C": f"{result.ambient_temp_c:.1f}",
        "LED_Current_High_A": f"{result.led_current_high_a:.4f}",
        "LED_VF_High_V": f"{result.led_vf_high_v:.3f}",
        "Output_Power_W": f"{result.output_power_w:.3f}",
        "Input_Current_A": f"{result.input_current_a:.4f}",
        "Switch_Current_Stress_A": f"{result.switch_current_stress_a:.4f}",
        "Inductor_Current_Stress_A": _fmt_optional(result.inductor_current_stress_a, digits=4),
        "Thermal_Loss_W": f"{result.thermal_loss_w:.3f}",
        "Junction_Temp_C": _fmt_optional(result.junction_temp_c, digits=1),
        "Max_Ratio": _fmt_optional(result.max_ratio, digits=4),
        "Margin_pct": _fmt_optional(result_margin_pct(result), digits=2),
        "Pass_Fail_Status": pass_fail_status(result),
        "Review_Status": result.review_status,
        "Review_Reason": result.review_reason,
    }


def result_margin_pct(result: WccaResult) -> Optional[float]:
    if result.max_ratio is None:
        return None
    return (1.0 - result.max_ratio) * 100.0


def pass_fail_status(result: WccaResult) -> str:
    if result.review_status == "Over synthetic limit":
        return "Fail"
    if result.review_status == "Within synthetic prep limit":
        return "Pass"
    return "Review"


def worst_results_by_case(results: Sequence[WccaResult]) -> List[WccaResult]:
    by_case: Dict[str, WccaResult] = {}
    for result in results:
        current = by_case.get(result.case_id)
        if current is None or _ratio_value(result) > _ratio_value(current):
            by_case[result.case_id] = result
    return [by_case[case_id] for case_id in sorted(by_case)]


def _ratio_value(result: WccaResult) -> float:
    if result.max_ratio is None:
        return -1.0
    return result.max_ratio


def _fmt_optional(value: Optional[float], digits: int) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}"
