# WCCA Equation Review Checklist

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Publication Classification

Needs review

## Engineering Review Boundary

This checklist supports review of deterministic WCCA preparation equations for synthetic automotive lighting examples. It does not approve engineering decisions. A qualified engineer remains responsible for formula correctness, units, assumptions, thresholds, boundary conditions, and final conclusions.

## Equation Checklist

| Equation Name | Purpose | Inputs | Units Check | Tolerance Handling | Temperature Handling | Boundary Condition Check | Known Limitation | Reviewer Notes | Reviewed By | Review Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Ohm's law current estimate | Estimate current from voltage and resistance when reviewing sense paths | Voltage V and resistance ohm | Confirm amps from V/ohm | Apply resistor min and max tolerance before margin review | None unless resistor temperature coefficient is added | Resistance must be greater than zero | Current-source behavior is simplified |  |  | Not reviewed |
| Resistor tolerance bounds | Bound current setpoint or sense threshold | Nominal resistor and tolerance pct | Confirm tolerance is percent of nominal value | Use high-current and low-current corners explicitly | Temperature coefficient not modeled | Tolerance cannot drive negative resistance | Does not replace component datasheet review |  |  | Not reviewed |
| LED string voltage margin | Compare input voltage against high-corner LED string voltage | LED VF nominal V and VF tolerance pct | Confirm volts in and volts out | Apply high VF corner for worst-case voltage stress | Ambient effects represented by synthetic VF tolerance only | Input voltage must remain positive | Does not model full LED binning or dynamic behavior |  |  | Not reviewed |
| Linear driver power dissipation | Estimate heat in a linear channel | VIN V LED VF V and LED current A | Confirm watts from V*A | Use high current and high VF for corner review | Ambient feeds junction estimate separately | Negative headroom is clamped for prep output | Simplified channel loss estimate |  |  | Not reviewed |
| Junction temperature estimate | Estimate synthetic junction temperature | Ambient C thermal rise C/W and loss W | Confirm C = C + W*C/W | Uses calculated worst-case loss | Ambient temperature comes from operating condition | Thermal resistance must be positive when provided | No transient or layout-specific model |  |  | Not reviewed |
| Harness voltage drop | Estimate low-line input stress after synthetic harness drop | Source voltage V drop V and load current A | Confirm voltage remains V | Apply worst-case low-line condition before margin review | Temperature effect not separately modeled | Resulting input voltage must be greater than zero | Harness model is a synthetic placeholder |  |  | Not reviewed |
| Percent margin calculation | Convert max stress ratio into review margin | Max stress ratio | Confirm percent is dimensionless ratio times 100 | Uses already-cornered stress ratios | Not directly temperature dependent | Missing ratio yields unavailable margin | Margin is prep status only not approval |  |  | Not reviewed |
| Pass/fail threshold comparison | Assign deterministic prep status | Max ratio and missing-data flags | Confirm ratio is unitless | Uses calculated worst-case stress ratios | Thermal ratio included when available | Missing required derating data triggers review | Thresholds are synthetic portfolio thresholds |  |  | Not reviewed |

## Reviewer Record

| Field | Entry |
|---|---|
| Reviewer name |  |
| Review date |  |
| Overall review status | Not reviewed |
| Comments |  |

## Proof Gaps

- Checklist has not been completed by a qualified reviewer.
- Formula, unit, threshold, assumption, boundary-condition, input, and output review status is still open.
- Synthetic thresholds are portfolio demonstration thresholds only.

## Safe to Publish Status

Needs review. This checklist is a synthetic review artifact and must be completed before the WCCA prep output is represented as reviewed.
