# Automotive Lighting Feasibility Mini-Simulator

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

Early lighting feasibility discussions need quick, transparent estimates without implying that a simplified tool can replace detailed engineering analysis.

## Purpose

This project is a deterministic first-pass feasibility screen for synthetic automotive lighting load cases. It estimates LED string voltage, current, output power, driver input current, voltage headroom, boost duty cycle, and simple thermal margins so an engineer can quickly identify cases that need deeper review.

The simulator supports feasibility screening only. It does not approve engineering decisions, release designs, validate requirements, or replace detailed electrical, thermal, optical, EMC, durability, or safety analysis.

## Engineering Context

Automotive lighting modules often require early tradeoff checks before detailed design data is available. A first-pass screen can help compare synthetic cases such as short LED strings, long LED strings, buck drivers, boost drivers, and linear channels against generic supply, current, power, and temperature assumptions.

All data in this folder is synthetic or sanitized. Case IDs, load names, ratings, thresholds, and assumptions are demonstration values only. Do not add proprietary organization, program, drawing, BOM, harness, cost, validation, controlled source, ticket, file path, or part-number details.

## Workflow

1. Load synthetic lighting case parameters from CSV.
2. Calculate worst-case LED voltage, current, power, driver input current, driver loss, thermal estimates, voltage headroom, and boost duty.
3. Compare calculated values against synthetic limits and thresholds.
4. Classify each case as `Pass`, `Marginal`, or `Fail`.
5. Generate Markdown, CSV, PNG plots, and screenshot-ready portfolio notes for human review.

## Inputs

The default input file is `data/synthetic_lighting_cases.csv`.

Key input fields:

- `Case_ID`, `Load_Name`, `Driver_Topology`
- LED count, nominal forward voltage, voltage tolerance, current, current tolerance, and duty cycle
- Minimum and maximum supply voltage
- Driver dropout, efficiency, and efficiency tolerance
- Synthetic current, voltage, output-power, temperature, and duty-cycle limits
- Board and LED thermal resistance assumptions
- Ambient temperature

## Outputs

Running the engine regenerates:

- `outputs/feasibility_summary.md`
- `outputs/feasibility_summary.csv`
- `outputs/plots/thermal_margin_by_case.png`
- `outputs/plots/current_margin_by_case.png`
- `outputs/plots/feasibility_status_count.png`
- `outputs/screenshots/portfolio_capture_summary.md`
- `outputs/sensitivity/sensitivity_summary.md`
- `outputs/sensitivity/sensitivity_summary.csv`
- `outputs/sensitivity/*_sweep.csv`
- `outputs/sensitivity/plots/*_sweep.png`

The Markdown and CSV outputs include synthetic-data labeling, human-review notes, calculation results, status reasons, recommended next steps, proof gaps, and safe-to-publish status.

## Screenshots Or Screenshot Placeholders

- `outputs/screenshots/portfolio_capture_summary.md`
- `outputs/plots/thermal_margin_by_case.png`
- `outputs/plots/current_margin_by_case.png`
- `outputs/plots/feasibility_status_count.png`

## Sanitized Sample Data

The sample dataset uses synthetic automotive lighting examples only. It includes generic buck, boost, and linear-channel cases with demonstration values for LED count, current, supply range, efficiency, ratings, thermal resistance, and ambient temperature.

## Human Review Controls

- Confirm every input and output remains synthetic before public use.
- Verify formulas, units, assumptions, and thresholds.
- Treat `Pass` as a first-pass screening result only.
- Treat `Marginal` and `Fail` as prompts for deeper analysis.
- Keep the human-review note visible in screenshots and public artifacts.

## Jose Review Pass

- Formulas: review LED voltage/current, output power, driver loss, voltage headroom, boost duty, thermal margin, and status-threshold equations.
- Assumptions: inspect synthetic limits, thermal resistance values, efficiency tolerance, ambient temperature, and sensitivity sweep ranges.
- Synthetic data: confirm [data/synthetic_lighting_cases.csv](data/synthetic_lighting_cases.csv) and generated outputs contain only synthetic demo cases.
- Screenshots: inspect [outputs/screenshots/portfolio_capture_summary.md](outputs/screenshots/portfolio_capture_summary.md) and [outputs/plots](outputs/plots) before using them as portfolio proof.
- Publication wording: confirm `Pass`, `Marginal`, and `Fail` remain screening labels only and all artifacts stay `Needs review`.

## Equations

The core equations are documented in `docs/equation_review.md`.

High-level equation groups:

- LED string voltage low and high corners
- Worst-case LED current
- Output power
- Converter or linear input current and driver loss
- Driver case temperature estimate
- LED junction temperature estimate
- Non-boost voltage headroom
- Boost duty-cycle estimate
- Stress ratios against synthetic limits
- Thermal margins

## Sensitivity Sweeps

Task 5C adds deterministic sweeps for selected synthetic inputs:

- `ambient_temperature_c`
- `led_current_a`
- `thermal_resistance_c_per_w`
- `optical_efficiency_percent`

The optical-efficiency sweep uses a synthetic relative optical factor because the base engine does not model optical output directly. Lower relative optical efficiency increases LED current demand for a fixed notional light target. Sweep ranges, assumptions, limitations, and human-review controls are documented in `docs/sensitivity_sweeps.md`.

## Future Project 6 Integration

Project 6 is planned as an upstream LED datasheet-to-model extractor. Project 5 should only consume reviewed Project 6 LED model CSV or JSON outputs through a future optional adapter, not raw datasheet extraction. The intended interface, metadata requirements, and review gate are documented in `docs/project6_input_interface.md`.

## Thresholds

The deterministic status policy is intentionally simple:

- `Fail`: any calculated stress ratio is greater than `1.00`, voltage headroom is below `0 V`, boost duty exceeds the synthetic maximum, or thermal margin is below `0 C`.
- `Marginal`: any calculated stress ratio is at least `0.85`, voltage headroom is `0.75 V` or less, boost duty is at least `85%` of the synthetic maximum, or thermal margin is `10 C` or less.
- `Pass`: no fail or marginal triggers are present.

Engineering review is required for all equations, limits, and thresholds before using this project in any external portfolio discussion.

## Limitations

- Synthetic screening only; no final design approval.
- No optical output, photometry, EMC, diagnostics, dimming, transient, tolerance stack, layout, material, or reliability modeling.
- Thermal calculations are simple lumped estimates.
- Driver efficiency and thermal resistance values are generic synthetic assumptions.
- Plots are generated by a dependency-free internal PNG renderer for portfolio illustration, not by a validated plotting package.
- Streamlit UI is intentionally not included yet; the deterministic engine is the proof point.

## Codex Contribution

Codex scaffolded the deterministic engine, CSV parser, Markdown and CSV output writers, dependency-free PNG plot generator, screenshot-ready summary artifact, and unit tests.

## Jose Contribution

Jose defines the engineering framing, acceptable first-pass screening scope, review expectations, and final judgment for whether the equations and portfolio claims are appropriate.

## AI Fundamentals Demonstrated

- Deterministic code generation
- Structured data transformation
- Rule-based classification
- Automated output generation
- Test generation

## Engineering Skills Demonstrated

- LED load estimation
- Driver current and power screening
- Voltage headroom review
- Boost duty-cycle screening
- Thermal margin estimation

## Risks And Mitigations

- Risk: A `Pass` result could be misread as design approval. Mitigation: every artifact states that human review is required and the tool is screening-only.
- Risk: Synthetic thresholds could appear authoritative. Mitigation: thresholds are documented as demonstration values requiring engineering review.
- Risk: Simple thermal assumptions could hide real constraints. Mitigation: outputs list limitations and recommended next steps.

## Next Improvements

- Add cross-variable sweep combinations after single-variable behavior is reviewed.
- Add reviewed equation annotations from a qualified engineer.
- Add a Streamlit shell only after the deterministic engine and thresholds are reviewed.

## How To Run

From this folder:

```bash
python3 feasibility_engine.py
```

The default command regenerates base feasibility outputs and Task 5C sensitivity outputs.

Run tests:

```bash
python3 -m unittest discover -s tests
```

Optional custom paths:

```bash
python3 feasibility_engine.py \
  --input data/synthetic_lighting_cases.csv \
  --markdown outputs/feasibility_summary.md \
  --csv outputs/feasibility_summary.csv \
  --plots-dir outputs/plots \
  --screenshots-dir outputs/screenshots \
  --sensitivity-dir outputs/sensitivity
```

Skip sensitivity output generation when checking only the base engine:

```bash
python3 feasibility_engine.py --skip-sweeps
```

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The examples are synthetic, but the equation set, thresholds, visual outputs, and portfolio claims require qualified engineering review before publication.
