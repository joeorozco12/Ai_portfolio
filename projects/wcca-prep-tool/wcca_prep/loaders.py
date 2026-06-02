"""CSV loaders for the synthetic WCCA preparation pipeline."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


REQUIRED_CASE_COLUMNS = {
    "Case_ID",
    "Topology",
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
}

REQUIRED_CONDITION_COLUMNS = {
    "Condition_ID",
    "Description",
    "VIN_V",
    "Ambient_Temp_C",
    "Load_Current_Factor",
}


@dataclass(frozen=True)
class CsvLoadResult:
    rows: List[Dict[str, str]]
    warnings: List[str]


def load_wcca_cases(path: Path) -> CsvLoadResult:
    return _load_csv(path, REQUIRED_CASE_COLUMNS, "case")


def load_operating_conditions(path: Path) -> CsvLoadResult:
    return _load_csv(path, REQUIRED_CONDITION_COLUMNS, "operating condition")


def _load_csv(path: Path, required_columns: set[str], label: str) -> CsvLoadResult:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label} CSV: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = sorted(required_columns - fieldnames)
        if missing_columns:
            joined = ", ".join(missing_columns)
            raise ValueError(f"{path.name} is missing required {label} columns: {joined}")

        rows = [_strip_row(row) for row in reader]

    warnings: List[str] = []
    for index, row in enumerate(rows, start=2):
        row_id = row.get("Case_ID") or row.get("Condition_ID") or f"row {index}"
        for column in sorted(required_columns):
            if row.get(column, "") == "":
                warnings.append(f"{row_id}: required field {column} is blank in {path.name}.")

    return CsvLoadResult(rows=rows, warnings=warnings)


def _strip_row(row: Dict[str, str]) -> Dict[str, str]:
    return {
        (key or "").strip(): (value or "").strip()
        for key, value in row.items()
        if key is not None
    }
