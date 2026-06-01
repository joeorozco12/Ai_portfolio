# Lighting Feasibility Mini-Simulator

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Synthetic feasibility tool for first-pass LED-driver and thermal/electrical tradeoff exploration.

## Status

Secondary portfolio project

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

- synthetic_led_load_cases.csv
- demo_limits.yaml
- thermal_assumptions.json

## Outputs

- feasibility table
- power/temperature plots
- risk flags
- assumption notes
- next-analysis recommendations

## Screenshot Placeholders

- simulator_input_form.png
- feasibility_plot.png
- risk_flag_summary.png

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

- Add sensitivity sweep.
- Add UI sliders.
- Add exportable feasibility memo.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
