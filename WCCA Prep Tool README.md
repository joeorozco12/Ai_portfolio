# AI-Assisted WCCA Prep Tool

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Synthetic LED-driver WCCA preparation workflow that organizes parameters, tolerances, plots, and review questions.

## Status

Priority proof spine

Working deterministic prototype is implemented under [projects/wcca-prep-tool](projects/wcca-prep-tool). The LED Datasheet-to-Model Extractor evidence is implemented under [projects/wcca-prep-tool/datasheet-plot-digitizer](projects/wcca-prep-tool/datasheet-plot-digitizer) and supports the WCCA prep story as a reviewed data-preparation path.

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

- [projects/wcca-prep-tool/data/synthetic_wcca_cases.csv](projects/wcca-prep-tool/data/synthetic_wcca_cases.csv)
- [projects/wcca-prep-tool/data/operating_conditions.csv](projects/wcca-prep-tool/data/operating_conditions.csv)
- Reviewed extractor outputs may become future inputs only after Project 6 adapter review.

## Outputs

- [projects/wcca-prep-tool/outputs/synthetic_wcca_report.md](projects/wcca-prep-tool/outputs/synthetic_wcca_report.md)
- [projects/wcca-prep-tool/outputs/synthetic_wcca_summary.csv](projects/wcca-prep-tool/outputs/synthetic_wcca_summary.csv)
- [projects/wcca-prep-tool/outputs/missing_data_warnings.md](projects/wcca-prep-tool/outputs/missing_data_warnings.md)
- [projects/wcca-prep-tool/outputs/plots](projects/wcca-prep-tool/outputs/plots)
- [projects/wcca-prep-tool/captures](projects/wcca-prep-tool/captures)

## Screenshots Or Capture Placeholders

- [projects/wcca-prep-tool/captures/cli_run_mock.md](projects/wcca-prep-tool/captures/cli_run_mock.md)
- [projects/wcca-prep-tool/captures/generated_summary_table_mock.md](projects/wcca-prep-tool/captures/generated_summary_table_mock.md)
- [projects/wcca-prep-tool/captures/plot_gallery_preview_mock.md](projects/wcca-prep-tool/captures/plot_gallery_preview_mock.md)
- [projects/wcca-prep-tool/outputs/plots/margin_by_case.png](projects/wcca-prep-tool/outputs/plots/margin_by_case.png)

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

- Complete the equation review checklist with reviewer notes.
- Add Monte Carlo demo only after the deterministic WCCA prep equations are reviewed.
- Add MATLAB Live Script variant only after current Python outputs are accepted.
- Replace Markdown mock captures with reviewed image screenshots only if needed.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
