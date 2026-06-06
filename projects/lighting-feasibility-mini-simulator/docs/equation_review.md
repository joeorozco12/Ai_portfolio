# Equation Review Notes

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Scope

This document describes the deterministic equations used by `feasibility_engine.py` for synthetic automotive lighting feasibility screening. These equations are intentionally simple and must be reviewed by a qualified engineer before use in any public portfolio artifact or engineering discussion.

## Variables

| Symbol | CSV or Result Field | Units | Meaning |
|---|---|---:|---|
| `N_LED` | `LED_Count` | count | Number of LEDs in the synthetic string |
| `Vf_nom` | `LED_Forward_Voltage_Nom_V` | V | Nominal forward voltage per LED |
| `Vf_tol` | `LED_VF_Tol_pct` | % | Forward-voltage tolerance percentage |
| `I_led_nom` | `LED_Current_Nom_A` | A | Nominal LED current |
| `I_tol` | `Current_Tol_pct` | % | Current tolerance percentage |
| `D` | `Duty_Cycle` | ratio | Lighting duty cycle from 0 to 1 |
| `Vsup_min` | `VSupply_Min_V` | V | Minimum synthetic supply voltage |
| `Vsup_max` | `VSupply_Max_V` | V | Maximum synthetic supply voltage |
| `Vdrop` | `Driver_Dropout_V` | V | Synthetic dropout or headroom allowance |
| `eta_nom` | `Driver_Efficiency` | ratio | Nominal driver efficiency |
| `eta_tol` | `Efficiency_Tol_pct` | % | Efficiency tolerance percentage |
| `Iin_max` | `Max_Input_Current_A` | A | Synthetic input-current limit |
| `Vin_rating` | `Max_Input_Voltage_V` | V | Synthetic input-voltage rating |
| `Pout_max` | `Max_Output_Power_W` | W | Synthetic output-power limit |
| `Rtheta_drv` | `Board_Thermal_Resistance_C_per_W` | C/W | Synthetic driver board thermal resistance |
| `Tcase_max` | `Max_Driver_Case_Temp_C` | C | Synthetic driver case temperature limit |
| `Rtheta_led` | `LED_Thermal_Resistance_C_per_W` | C/W | Synthetic LED thermal resistance |
| `Tj_max` | `Max_LED_Junction_Temp_C` | C | Synthetic LED junction temperature limit |
| `Tamb` | `Ambient_Temp_C` | C | Synthetic ambient temperature |
| `Dboost_max` | `Max_Boost_Duty_Cycle` | ratio | Synthetic maximum boost duty cycle |

## Equations

### LED String Voltage

Nominal string voltage:

```text
Vstring_nom = N_LED * Vf_nom
```

Low-corner string voltage:

```text
Vstring_low = Vstring_nom * (1 - Vf_tol / 100)
```

High-corner string voltage:

```text
Vstring_high = Vstring_nom * (1 + Vf_tol / 100)
```

Units: volts. The high-corner value is used for output-power and headroom screening. The low-corner value is used for linear driver loss screening at maximum supply.

### Worst-Case LED Current

```text
Iled_high = I_led_nom * (1 + I_tol / 100)
```

Units: amperes. This is a synthetic high-current corner for first-pass screening.

### Output Power

```text
Pout = Vstring_high * Iled_high * D
```

Units: watts. This is an electrical output-power estimate, not optical output.

### Low-Corner Driver Efficiency

```text
eta_low = eta_nom * (1 - eta_tol / 100)
```

Units: ratio. This is used for switching driver input-power and input-current estimates.

### Switching Driver Input Power And Current

For non-linear drivers:

```text
Pin = Pout / eta_low
Iin_min_supply = Pin / Vsup_min
Ploss_driver = max(Pin - Pout, 0)
```

Units: watts for `Pin` and `Ploss_driver`; amperes for `Iin_min_supply`.

### Linear Driver Input Current And Loss

For linear LED channels:

```text
Iin_min_supply = Iled_high * D
Ploss_driver = max(Vsup_max - Vstring_low, 0) * Iin_min_supply
Pin = Pout + Ploss_driver
```

Units: amperes for input current; watts for driver loss and input power. The loss equation uses high supply and low LED voltage because that is a conservative linear-driver heat corner.

### Driver Case Temperature

```text
Tcase = Tamb + Ploss_driver * Rtheta_drv
```

Units: degrees C. This is a lumped first-pass estimate only.

### LED Junction Temperature

```text
Tj_led = Tamb + (Pout / N_LED) * Rtheta_led
```

Units: degrees C. This assumes equal power sharing across LEDs and does not model layout, optics, solder interface, or detailed thermal paths.

### Voltage Headroom

For non-boost drivers:

```text
Vheadroom = Vsup_min - Vstring_high - Vdrop
```

Units: volts. Negative headroom is treated as a fail trigger.

### Boost Duty Cycle

For boost drivers:

```text
Dboost = max(0, 1 - (Vsup_min * eta_low / Vstring_high))
```

Units: ratio. This is a simplified first-pass estimate and is not a substitute for converter design analysis.

### Stress Ratios

Each stress ratio compares a calculated value to a synthetic limit:

```text
input_current_ratio = Iin_min_supply / Iin_max
input_voltage_ratio = Vsup_max / Vin_rating
output_power_ratio = Pout / Pout_max
driver_temp_ratio = Tcase / Tcase_max
led_temp_ratio = Tj_led / Tj_max
max_ratio = maximum known stress ratio
```

Units: ratios. A ratio over `1.00` means the calculated stress exceeds the synthetic limit.

### Thermal Margins

```text
driver_temp_margin = Tcase_max - Tcase
led_temp_margin = Tj_max - Tj_led
```

Units: degrees C. Negative margin is treated as a fail trigger.

## Pass, Marginal, Fail Thresholds

Engineering review required: all thresholds below are synthetic demonstration thresholds and must be reviewed before publication or reuse.

| Status | Deterministic Trigger |
|---|---|
| `Fail` | Any stress ratio is greater than `1.00`; voltage headroom is below `0 V`; boost duty exceeds `Dboost_max`; driver or LED thermal margin is below `0 C` |
| `Marginal` | Any stress ratio is at least `0.85`; voltage headroom is `0.75 V` or less; boost duty is at least `85%` of `Dboost_max`; driver or LED thermal margin is `10 C` or less |
| `Pass` | No fail or marginal triggers are present |

## Review Items

- Confirm whether each equation is acceptable for a synthetic portfolio demonstration.
- Confirm whether the thermal model should remain this simple or be replaced with a more explicit assumptions table.
- Confirm whether voltage headroom and boost duty thresholds are appropriate as demonstration values.
- Confirm whether ratio thresholds should be adjusted or labeled as examples only.
- Confirm that no result is described as design approval.

## Safe To Publish Status

Needs review. This document contains synthetic equations and thresholds, but qualified engineering review is required before publication.
