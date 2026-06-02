"""Deterministic stress and derating calculations for synthetic WCCA prep."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


REVIEW_RATIO = 0.80
LIMIT_RATIO = 1.00


@dataclass(frozen=True)
class WccaCase:
    case_id: str
    topology: str
    vin_min_v: float
    vin_nom_v: float
    vin_max_v: float
    led_string_vf_nom_v: float
    led_string_vf_tol_pct: float
    led_current_a: float
    ambient_temp_c: float
    efficiency_assumption: float
    efficiency_tol_pct: float
    current_tol_pct: float
    sense_res_tol_pct: float
    switch_current_rating_a: float
    input_voltage_rating_v: float
    inductor_current_rating_a: Optional[float]
    thermal_rise_c_per_w: Optional[float]
    max_junction_temp_c: Optional[float]


@dataclass(frozen=True)
class OperatingCondition:
    condition_id: str
    description: str
    vin_v: float
    ambient_temp_c: float
    load_current_factor: float


@dataclass(frozen=True)
class WccaResult:
    case_id: str
    condition_id: str
    topology: str
    vin_v: float
    ambient_temp_c: float
    led_current_high_a: float
    led_vf_high_v: float
    output_power_w: float
    input_current_a: float
    switch_current_stress_a: float
    inductor_current_stress_a: Optional[float]
    thermal_loss_w: float
    junction_temp_c: Optional[float]
    voltage_ratio: Optional[float]
    switch_current_ratio: Optional[float]
    inductor_current_ratio: Optional[float]
    thermal_ratio: Optional[float]
    max_ratio: Optional[float]
    review_status: str
    review_reason: str


@dataclass(frozen=True)
class CalculationBundle:
    results: List[WccaResult]
    warnings: List[str]


def calculate_wcca(
    case_rows: Sequence[Dict[str, str]],
    condition_rows: Sequence[Dict[str, str]],
) -> CalculationBundle:
    warnings: List[str] = []
    cases = [_parse_case(row, warnings) for row in case_rows]
    conditions = [_parse_condition(row, warnings) for row in condition_rows]

    valid_cases = [case for case in cases if case is not None]
    valid_conditions = [condition for condition in conditions if condition is not None]

    results: List[WccaResult] = []
    for case in valid_cases:
        for condition in valid_conditions:
            _warn_for_condition_outside_case_range(case, condition, warnings)
            results.append(calculate_case_condition(case, condition))

    return CalculationBundle(results=results, warnings=warnings)


def calculate_case_condition(case: WccaCase, condition: OperatingCondition) -> WccaResult:
    led_current_high_a = case.led_current_a * condition.load_current_factor
    led_current_high_a *= 1.0 + _pct(case.current_tol_pct) + _pct(case.sense_res_tol_pct)

    led_vf_high_v = case.led_string_vf_nom_v * (1.0 + _pct(case.led_string_vf_tol_pct))
    output_power_w = led_vf_high_v * led_current_high_a
    efficiency_low = case.efficiency_assumption * (1.0 - _pct(case.efficiency_tol_pct))

    input_current_a = output_power_w / (condition.vin_v * efficiency_low)
    switch_current_stress_a = _switch_current_stress(
        case.topology,
        led_current_high_a,
        input_current_a,
    )
    inductor_current_stress_a = _inductor_current_stress(case.topology, switch_current_stress_a)
    thermal_loss_w = _thermal_loss(
        case.topology,
        condition.vin_v,
        led_vf_high_v,
        led_current_high_a,
        output_power_w,
        efficiency_low,
    )

    junction_temp_c = None
    if case.thermal_rise_c_per_w is not None:
        junction_temp_c = condition.ambient_temp_c + thermal_loss_w * case.thermal_rise_c_per_w

    voltage_ratio = _safe_ratio(condition.vin_v, case.input_voltage_rating_v)
    switch_current_ratio = _safe_ratio(switch_current_stress_a, case.switch_current_rating_a)
    inductor_current_ratio = None
    if inductor_current_stress_a is not None and case.inductor_current_rating_a is not None:
        inductor_current_ratio = _safe_ratio(inductor_current_stress_a, case.inductor_current_rating_a)

    thermal_ratio = None
    if junction_temp_c is not None and case.max_junction_temp_c is not None:
        thermal_ratio = _safe_ratio(junction_temp_c, case.max_junction_temp_c)

    ratios = [
        ratio
        for ratio in (
            voltage_ratio,
            switch_current_ratio,
            inductor_current_ratio,
            thermal_ratio,
        )
        if ratio is not None
    ]
    max_ratio = max(ratios) if ratios else None
    review_status, review_reason = _review_status(
        case,
        max_ratio,
        voltage_ratio,
        switch_current_ratio,
        inductor_current_ratio,
        thermal_ratio,
    )

    return WccaResult(
        case_id=case.case_id,
        condition_id=condition.condition_id,
        topology=case.topology,
        vin_v=condition.vin_v,
        ambient_temp_c=condition.ambient_temp_c,
        led_current_high_a=led_current_high_a,
        led_vf_high_v=led_vf_high_v,
        output_power_w=output_power_w,
        input_current_a=input_current_a,
        switch_current_stress_a=switch_current_stress_a,
        inductor_current_stress_a=inductor_current_stress_a,
        thermal_loss_w=thermal_loss_w,
        junction_temp_c=junction_temp_c,
        voltage_ratio=voltage_ratio,
        switch_current_ratio=switch_current_ratio,
        inductor_current_ratio=inductor_current_ratio,
        thermal_ratio=thermal_ratio,
        max_ratio=max_ratio,
        review_status=review_status,
        review_reason=review_reason,
    )


def _parse_case(row: Dict[str, str], warnings: List[str]) -> Optional[WccaCase]:
    case_id = row.get("Case_ID", "").strip() or "UNKNOWN-CASE"
    topology = row.get("Topology", "").strip()

    required_fields = [
        "VIN_Min_V",
        "VIN_Nom_V",
        "VIN_Max_V",
        "LED_String_VF_Nom_V",
        "LED_Current_A",
        "Efficiency_Assumption",
        "Current_Tol_pct",
        "Sense_Res_Tol_pct",
        "Switch_Current_Rating_A",
        "Input_Voltage_Rating_V",
    ]
    parsed = {field: _float(row.get(field), case_id, field, warnings) for field in required_fields}
    if topology == "":
        warnings.append(f"{case_id}: required field Topology is blank; row skipped.")
        return None
    if any(value is None for value in parsed.values()):
        warnings.append(f"{case_id}: required numeric input is missing or invalid; row skipped.")
        return None

    led_vf_tol = _optional_float(row, "LED_String_VF_Tol_pct", case_id, 0.0, warnings)
    efficiency_tol = _optional_float(row, "Efficiency_Tol_pct", case_id, 0.0, warnings)
    inductor_rating = _optional_float(
        row, "Inductor_Current_Rating_A", case_id, None, warnings, warn_on_blank=False
    )
    thermal_rise = _optional_float(
        row, "Thermal_Rise_C_per_W", case_id, None, warnings, warn_on_blank=False
    )
    max_junction = _optional_float(
        row, "Max_Junction_Temp_C", case_id, None, warnings, warn_on_blank=False
    )

    _warn_for_nominal_power_mismatch(
        row,
        case_id,
        parsed["LED_String_VF_Nom_V"],
        parsed["LED_Current_A"],
        warnings,
    )
    _warn_for_missing_derating_inputs(topology, case_id, inductor_rating, thermal_rise, max_junction, warnings)
    if not _efficiency_is_valid(case_id, parsed["Efficiency_Assumption"], efficiency_tol, warnings):
        warnings.append(f"{case_id}: invalid efficiency input; row skipped.")
        return None
    ambient_temp_c = _optional_float(row, "Ambient_Temp_C", case_id, 25.0, warnings)

    return WccaCase(
        case_id=case_id,
        topology=topology,
        vin_min_v=parsed["VIN_Min_V"],
        vin_nom_v=parsed["VIN_Nom_V"],
        vin_max_v=parsed["VIN_Max_V"],
        led_string_vf_nom_v=parsed["LED_String_VF_Nom_V"],
        led_string_vf_tol_pct=led_vf_tol or 0.0,
        led_current_a=parsed["LED_Current_A"],
        ambient_temp_c=ambient_temp_c if ambient_temp_c is not None else 25.0,
        efficiency_assumption=parsed["Efficiency_Assumption"],
        efficiency_tol_pct=efficiency_tol or 0.0,
        current_tol_pct=parsed["Current_Tol_pct"],
        sense_res_tol_pct=parsed["Sense_Res_Tol_pct"],
        switch_current_rating_a=parsed["Switch_Current_Rating_A"],
        input_voltage_rating_v=parsed["Input_Voltage_Rating_V"],
        inductor_current_rating_a=inductor_rating,
        thermal_rise_c_per_w=thermal_rise,
        max_junction_temp_c=max_junction,
    )


def _parse_condition(row: Dict[str, str], warnings: List[str]) -> Optional[OperatingCondition]:
    condition_id = row.get("Condition_ID", "").strip() or "UNKNOWN-CONDITION"
    description = row.get("Description", "").strip()
    vin_v = _float(row.get("VIN_V"), condition_id, "VIN_V", warnings)
    ambient_temp_c = _float(row.get("Ambient_Temp_C"), condition_id, "Ambient_Temp_C", warnings)
    load_current_factor = _float(row.get("Load_Current_Factor"), condition_id, "Load_Current_Factor", warnings)

    if description == "":
        warnings.append(f"{condition_id}: required field Description is blank; row skipped.")
        return None
    if vin_v is None or ambient_temp_c is None or load_current_factor is None:
        warnings.append(f"{condition_id}: required numeric operating input is missing or invalid; row skipped.")
        return None
    if vin_v <= 0:
        warnings.append(f"{condition_id}: VIN_V must be greater than zero; row skipped.")
        return None
    if load_current_factor <= 0:
        warnings.append(f"{condition_id}: Load_Current_Factor must be greater than zero; row skipped.")
        return None

    return OperatingCondition(
        condition_id=condition_id,
        description=description,
        vin_v=vin_v,
        ambient_temp_c=ambient_temp_c,
        load_current_factor=load_current_factor,
    )


def _switch_current_stress(topology: str, led_current_high_a: float, input_current_a: float) -> float:
    normalized = topology.lower()
    if "boost" in normalized:
        return input_current_a * 1.15
    if "sepic" in normalized:
        return (input_current_a + led_current_high_a) * 1.10
    if "linear" in normalized:
        return led_current_high_a
    return led_current_high_a * 1.10


def _inductor_current_stress(topology: str, switch_current_stress_a: float) -> Optional[float]:
    if "linear" in topology.lower():
        return None
    return switch_current_stress_a


def _thermal_loss(
    topology: str,
    vin_v: float,
    led_vf_high_v: float,
    led_current_high_a: float,
    output_power_w: float,
    efficiency_low: float,
) -> float:
    if "linear" in topology.lower():
        return max(vin_v - led_vf_high_v, 0.0) * led_current_high_a
    return max(output_power_w * (1.0 / efficiency_low - 1.0), 0.0)


def _review_status(
    case: WccaCase,
    max_ratio: Optional[float],
    voltage_ratio: Optional[float],
    switch_current_ratio: Optional[float],
    inductor_current_ratio: Optional[float],
    thermal_ratio: Optional[float],
) -> Tuple[str, str]:
    if max_ratio is not None and max_ratio > LIMIT_RATIO:
        return "Over synthetic limit", "At least one stress ratio exceeds 1.00."

    missing_derating = voltage_ratio is None or switch_current_ratio is None or thermal_ratio is None
    if "linear" not in case.topology.lower() and inductor_current_ratio is None:
        missing_derating = True

    if missing_derating:
        return "Review required", "One or more derating ratios could not be calculated."
    if max_ratio is not None and max_ratio >= REVIEW_RATIO:
        return "Review required", "At least one stress ratio is at or above 0.80."
    return "Within synthetic prep limit", "All calculated stress ratios are below 0.80."


def _warn_for_condition_outside_case_range(
    case: WccaCase,
    condition: OperatingCondition,
    warnings: List[str],
) -> None:
    if condition.vin_v < case.vin_min_v or condition.vin_v > case.vin_max_v:
        warnings.append(
            f"{case.case_id}/{condition.condition_id}: condition VIN {condition.vin_v:.2f} V "
            f"is outside case range {case.vin_min_v:.2f} V to {case.vin_max_v:.2f} V."
        )


def _warn_for_nominal_power_mismatch(
    row: Dict[str, str],
    case_id: str,
    vf_nom_v: float,
    led_current_a: float,
    warnings: List[str],
) -> None:
    if row.get("Output_Power_W", "") == "":
        return
    provided = _float(row.get("Output_Power_W"), case_id, "Output_Power_W", warnings)
    if provided is None:
        return
    calculated = vf_nom_v * led_current_a
    if calculated == 0:
        return
    error_pct = abs(provided - calculated) / calculated * 100.0
    if error_pct > 2.0:
        warnings.append(
            f"{case_id}: Output_Power_W differs from nominal VF*current by {error_pct:.1f}%."
        )


def _warn_for_missing_derating_inputs(
    topology: str,
    case_id: str,
    inductor_rating: Optional[float],
    thermal_rise: Optional[float],
    max_junction: Optional[float],
    warnings: List[str],
) -> None:
    if "linear" not in topology.lower() and inductor_rating is None:
        warnings.append(f"{case_id}: Inductor_Current_Rating_A is missing; inductor derating is unavailable.")
    if thermal_rise is None:
        warnings.append(f"{case_id}: Thermal_Rise_C_per_W is missing; thermal rise is unavailable.")
    if max_junction is None:
        warnings.append(f"{case_id}: Max_Junction_Temp_C is missing; thermal derating is unavailable.")


def _efficiency_is_valid(
    case_id: str,
    efficiency_assumption: float,
    efficiency_tol_pct: float,
    warnings: List[str],
) -> bool:
    efficiency_low = efficiency_assumption * (1.0 - _pct(efficiency_tol_pct))
    is_valid = True
    if efficiency_assumption <= 0 or efficiency_assumption > 1:
        warnings.append(f"{case_id}: Efficiency_Assumption must be greater than 0 and no more than 1.")
        is_valid = False
    if efficiency_low <= 0:
        warnings.append(f"{case_id}: low-corner efficiency is not greater than zero.")
        is_valid = False
    return is_valid


def _optional_float(
    row: Dict[str, str],
    field: str,
    row_id: str,
    default: Optional[float],
    warnings: List[str],
    warn_on_blank: bool = True,
) -> Optional[float]:
    value = row.get(field, "")
    if value == "":
        if warn_on_blank and default is not None:
            warnings.append(f"{row_id}: optional field {field} is blank; default {default:g} used.")
        elif warn_on_blank:
            warnings.append(f"{row_id}: optional field {field} is blank.")
        return default
    return _float(value, row_id, field, warnings)


def _float(value: Optional[str], row_id: str, field: str, warnings: List[str]) -> Optional[float]:
    if value is None or value == "":
        warnings.append(f"{row_id}: field {field} is blank.")
        return None
    try:
        return float(value)
    except ValueError:
        warnings.append(f"{row_id}: field {field} has invalid numeric value {value!r}.")
        return None


def _safe_ratio(value: float, rating: float) -> Optional[float]:
    if rating <= 0:
        return None
    return value / rating


def _pct(value: float) -> float:
    return value / 100.0
