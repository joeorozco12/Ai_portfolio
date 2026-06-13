# Sensitivity Sweeps

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

Task 5C adds deterministic sensitivity sweeps to the Lighting Feasibility Mini-Simulator. The sweeps vary selected synthetic engineering inputs and show how `Pass`, `Marginal`, and `Fail` classifications change across simple review ranges.

The sweeps support engineering investigation only. They do not approve engineering decisions, release designs, or replace detailed electrical, thermal, optical, EMC, durability, or safety analysis.

## Review Disposition

| Field | Entry |
|---|---|
| Reviewer name | Jose Orozco |
| Review date | 2026-06-13 |
| Review status | Accepted for synthetic portfolio use |
| Review basis | Sweep variables, synthetic ranges, optical-efficiency proxy, limitations, output list, and publication wording reviewed for public-safe demonstration use. |
| Boundary | Sweeps remain one-variable-at-a-time investigation aids and do not represent final engineering judgment. |

## Variables Swept

| Sweep | Variable | Units | Engine Behavior |
|---|---|---:|---|
| Ambient temperature | `ambient_temperature_c` | C | Replaces the case ambient temperature before recalculating thermal margins |
| LED current | `led_current_a` | A | Scales base LED current from 80% to 120%; CSV rows show the applied current |
| Thermal resistance | `thermal_resistance_c_per_w` | C/W | Scales board and LED thermal resistance assumptions together |
| Optical efficiency | `optical_efficiency_percent` | % | Applies a synthetic relative optical factor; lower efficiency increases LED current demand for a fixed notional light target |

## Synthetic Ranges Used

| Sweep | Synthetic Range |
|---|---|
| `ambient_temperature_c` | 75 C, 85 C, 95 C, 105 C, 115 C |
| `led_current_a` | 80%, 90%, 100%, 110%, 120% of each base synthetic current |
| `thermal_resistance_c_per_w` | 80%, 90%, 100%, 110%, 120% of each base synthetic thermal resistance |
| `optical_efficiency_percent` | 70%, 85%, 100%, 115%, 130% relative optical efficiency |

## What Each Sweep Reveals

### Ambient Temperature

Shows how increased ambient temperature consumes driver and LED thermal margin. This is useful for identifying cases where thermal limits dominate the feasibility classification.

### LED Current

Shows how higher or lower current demand changes output power, input current, driver loss, and LED junction temperature. This sweep can reveal whether a case is current-limited, power-limited, or thermally sensitive.

### Thermal Resistance

Shows how synthetic thermal-path assumptions affect driver case and LED junction margin. The sweep scales board and LED thermal resistance together to keep the model simple and deterministic.

### Optical Efficiency

The base engine does not model optical output directly. This sweep uses a synthetic relative optical-efficiency factor as the closest optical proxy: lower relative optical efficiency requires more LED current for a fixed notional light target, while higher relative optical efficiency reduces current demand.

## Outputs

Generated files:

- `outputs/sensitivity/sensitivity_summary.md`
- `outputs/sensitivity/sensitivity_summary.csv`
- `outputs/sensitivity/ambient_temperature_sweep.csv`
- `outputs/sensitivity/led_current_sweep.csv`
- `outputs/sensitivity/thermal_resistance_sweep.csv`
- `outputs/sensitivity/optical_efficiency_sweep.csv`
- `outputs/sensitivity/plots/ambient_temperature_sweep.png`
- `outputs/sensitivity/plots/led_current_sweep.png`
- `outputs/sensitivity/plots/thermal_resistance_sweep.png`
- `outputs/sensitivity/plots/optical_efficiency_sweep.png`

## Limitations

- Sweeps vary one input family at a time and do not model coupled interactions.
- Ranges are synthetic demonstration values and are not program criteria.
- Optical efficiency is represented as a relative current-demand factor, not a photometric model.
- Thermal resistance scaling is lumped and does not replace detailed thermal analysis.
- The `Pass`, `Marginal`, and `Fail` thresholds remain synthetic and review-required.
- Plots are portfolio visualizations generated from synthetic rows.

## Human Review Requirements

- Sweep ranges have been reviewed for synthetic portfolio use.
- Thresholds and status rules have been reviewed as demonstration values only.
- Every row, plot, and summary must remain synthetic and sanitized.
- The optical-efficiency proxy must remain described as a simplified investigation input.
- No result may be described as engineering approval.

## Safe To Publish Status

Safe to publish for synthetic portfolio demonstration. The sweep outputs use synthetic data only, and the ranges, thresholds, and interpretation have been reviewed for demo use.
