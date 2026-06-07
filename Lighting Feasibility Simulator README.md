# Lighting Feasibility Mini-Simulator

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Synthetic feasibility tool for first-pass LED-driver and thermal/electrical tradeoff exploration.

## Status

Secondary portfolio project

Working deterministic simulator is implemented under [projects/lighting-feasibility-mini-simulator](projects/lighting-feasibility-mini-simulator). Current proof includes feasibility summaries, plot PNGs, sensitivity sweeps, unit tests, and a reviewed-only Project 6 input-boundary document.

## Problem

Early feasibility discussions need quick, transparent estimates without pretending to replace detailed engineering analysis.

## Engineering Context

Synthetic automotive lighting loads, generated voltage/current limits, basic efficiency assumptions, and thermal review flags.

## Workflow

- Load candidate synthetic LED load cases.
- Calculate first-pass power, current, efficiency, and thermal indicators.
- Flag cases that need deeper analysis.
- Export feasibility table and plot gallery.

## Inputs

- [projects/lighting-feasibility-mini-simulator/data/synthetic_lighting_cases.csv](projects/lighting-feasibility-mini-simulator/data/synthetic_lighting_cases.csv)
- Future reviewed Project 6 LED model CSV/JSON outputs only through an adapter that is not implemented yet

## Outputs

- [projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.md](projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.md)
- [projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.csv](projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.csv)
- [projects/lighting-feasibility-mini-simulator/outputs/plots](projects/lighting-feasibility-mini-simulator/outputs/plots)
- [projects/lighting-feasibility-mini-simulator/outputs/sensitivity](projects/lighting-feasibility-mini-simulator/outputs/sensitivity)
- [projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md](projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md)

## Screenshots Or Capture Placeholders

- [projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md](projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md)
- [projects/lighting-feasibility-mini-simulator/outputs/plots/current_margin_by_case.png](projects/lighting-feasibility-mini-simulator/outputs/plots/current_margin_by_case.png)
- [projects/lighting-feasibility-mini-simulator/outputs/plots/thermal_margin_by_case.png](projects/lighting-feasibility-mini-simulator/outputs/plots/thermal_margin_by_case.png)
- [projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/ambient_temperature_sweep.png](projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/ambient_temperature_sweep.png)

## Sanitized Sample Data

Use the source-pack CSV files where applicable. Public examples must remain synthetic and should avoid internal naming, real customer requirements, proprietary schematics, internal limits, and program-specific values.

## Human Review Controls

Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Review checkpoints:

- Confirm all inputs are synthetic or sanitized.
- Confirm AI-proposed classifications are reviewed.
- Confirm calculations, formulas, limits, and pass/review labels are verified by an engineer.
- Confirm output is marked as draft until approved.

## Codex Contribution

Codex helps scaffold the simulator, generate input schemas, create plotting utilities, and write tests.

## Jose Contribution

Jose defines which calculations are acceptable for first-pass screening and clarifies that detailed design approval requires deeper review.

## AI Fundamentals Demonstrated

- Code generation
- Scenario generation
- Structured reporting
- Assumption documentation
- Visualization planning

## Engineering Skills Demonstrated

- Power electronics basics
- LED load estimation
- Thermal-risk screening
- Feasibility analysis
- MATLAB/Python plotting

## Risks and Mitigations

- Mini-simulator may be mistaken for final design tool. Mitigation: explicit feasibility-only labeling.
- Generic assumptions may not match real programs. Mitigation: synthetic-only disclaimer.

## Next Improvements

- Complete qualified review of equations, thresholds, and sensitivity ranges.
- Add reviewed Project 6 adapter only after the LED model schema is finalized.
- Add UI sliders only after deterministic engine evidence is accepted.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
