# AI-Assisted WCCA Prep Tool

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Synthetic LED-driver WCCA preparation workflow that organizes parameters, tolerances, plots, and review questions.

## Status

Priority proof spine

## Problem

Worst-case circuit analysis preparation is slow when assumptions, tolerances, derating limits, equations, CSV exports, and plots live in scattered notes and scripts.

## Engineering Context

Synthetic LED-driver case with generated voltage, current, tolerance, efficiency, and thermal parameters. It demonstrates workflow structure without exposing circuit details.

## Workflow

- Load synthetic WCCA parameter CSV.
- Validate units, missing tolerances, and assumption fields.
- Run deterministic example calculations and corner sweeps.
- Generate plots and pass/review notes.
- Export assumption register, calculation summary, and review memo.

## Inputs

- synthetic_wcca_sample.csv
- calculation_config.yaml
- plot_style_config.json
- review_limit_dictionary.json

## Outputs

- parameter table
- corner-case summary
- assumption register
- plots
- review memo
- open questions list

## Screenshot Placeholders

- parameter_audit_table.png
- wcca_corner_plot.png
- assumption_register.png

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

Codex helps scaffold MATLAB/Python functions, generate unit tests, refactor calculation modules, and draft markdown reports.

## Jose Contribution

Jose defines equations, validates assumptions, checks tolerances, reviews plots, and decides whether calculations are acceptable.

## AI Fundamentals Demonstrated

- Structured analysis planning
- Code generation for repeatable calculations
- Documentation automation
- Test generation
- Human-review checkpoint design

## Engineering Skills Demonstrated

- WCCA preparation
- Tolerance analysis
- Thermal/electrical assumption tracking
- MATLAB/Python plotting
- Design-review readiness

## Risks and Mitigations

- AI-generated equations can be wrong. Mitigation: deterministic calculation modules and engineer formula review.
- Tolerance omissions can hide risk. Mitigation: missing-data audit.
- Plots may imply pass/fail certainty. Mitigation: label as prep output pending review.

## Next Improvements

- Add Monte Carlo demo.
- Add MATLAB Live Script variant.
- Add plot gallery.
- Add equation review checklist.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
