# Sensitivity Sweep Summary

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

Task 5C adds deterministic sensitivity sweeps to show how synthetic feasibility status changes when selected engineering inputs move across review ranges.

## Engineering Context

The sweeps support investigation of lighting feasibility drivers such as ambient temperature, LED current, thermal resistance, and a synthetic relative optical-efficiency factor. They do not approve engineering decisions.

## Variables Swept

- `ambient_temperature_c`: ambient temperature values from 75 C to 115 C.
- `led_current_a`: base LED current scaled from 80% to 120%; CSV rows show applied current in A.
- `thermal_resistance_c_per_w`: board and LED thermal resistances scaled from 80% to 120%; CSV rows show applied C/W values.
- `optical_efficiency_percent`: synthetic relative optical efficiency from 70% to 130%; lower values increase LED current for a fixed notional light target.

## Synthetic Ranges Used

- Ambient temperature C: 75, 85, 95, 105, 115
- LED current scale factors: 80%, 90%, 100%, 110%, 120%
- Thermal resistance scale factors: 80%, 90%, 100%, 110%, 120%
- Optical efficiency percent: 70, 85, 100, 115, 130

## Outputs

- `outputs/sensitivity/sensitivity_summary.csv`
- `outputs/sensitivity/ambient_temperature_sweep.csv`
- `outputs/sensitivity/led_current_sweep.csv`
- `outputs/sensitivity/thermal_resistance_sweep.csv`
- `outputs/sensitivity/optical_efficiency_sweep.csv`
- `outputs/sensitivity/plots/ambient_temperature_sweep.png`
- `outputs/sensitivity/plots/led_current_sweep.png`
- `outputs/sensitivity/plots/thermal_resistance_sweep.png`
- `outputs/sensitivity/plots/optical_efficiency_sweep.png`

## Status Summary

- Total sweep rows: 100
- Pass: 18
- Marginal: 40
- Fail: 42

## Sweep Details

| Sweep | Rows | Pass | Marginal | Fail | What It Reveals |
|---|---:|---:|---:|---:|---|
| ambient_temperature_sweep | 25 | 4 | 9 | 12 | Temperature sensitivity of driver and LED thermal margins. |
| led_current_sweep | 25 | 5 | 10 | 10 | Electrical and thermal sensitivity to current demand. |
| thermal_resistance_sweep | 25 | 5 | 10 | 10 | Thermal-path sensitivity using scaled C/W assumptions. |
| optical_efficiency_sweep | 25 | 4 | 11 | 10 | Current-demand sensitivity for a fixed synthetic light target. |

## Human Review Controls

- Review all sweep ranges and thresholds before publication.
- Treat status changes as investigation prompts only.
- Confirm plots and CSV rows remain synthetic and sanitized.
- Do not use sweep output as design approval or engineering signoff.

## Limitations

- Sweeps vary one synthetic input family at a time.
- Optical efficiency is modeled as a relative current-demand factor because the base engine does not model optical output.
- Thermal resistance scaling is lumped and does not replace detailed thermal analysis.
- No correlations between variables are modeled.

## Safe to Publish Status

Needs review. The ranges and thresholds are synthetic and require qualified engineering review before publication.
