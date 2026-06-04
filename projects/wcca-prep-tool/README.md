# AI-Assisted WCCA Prep Tool

[SYNTHETIC -- FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Engineering Review Boundary

This tool prepares WCCA inputs and review artifacts. It is not a final WCCA approval tool.

- The tool prepares WCCA inputs and review artifacts.
- It does not approve engineering decisions.
- Engineers remain responsible for formulas, assumptions, thresholds, and final conclusions.
- All examples are synthetic and sanitized.

## Workflow Alignment

- Uses only synthetic or sanitized automotive lighting examples.
- Keeps AI/Codex work scoped to this project folder.
- Uses deterministic calculations before AI narrative.
- Generates review artifacts to support engineering review.
- Does not replace qualified engineering judgment.

## Scope

This Task 2 proof package is a deterministic WCCA preparation pipeline for synthetic automotive LED driver examples. It does not use proprietary circuit data, customer limits, internal derating rules, schematics, BOMs, harness data, cost data, validation data, or real program identifiers.

The proof package demonstrates:

- load synthetic WCCA case data from CSV
- load synthetic operating conditions from CSV
- run repeatable stress and derating calculations
- generate a Markdown WCCA prep report
- generate a CSV calculation summary
- generate a PNG plot gallery
- generate a missing-data warning report
- generate clearly labeled mock capture artifacts
- test the calculation engine

## Run

From this folder:

```bash
python3 -m unittest discover -s tests
python3 -m wcca_prep.cli
```

Default inputs:

- [data/synthetic_wcca_cases.csv](data/synthetic_wcca_cases.csv)
- [data/operating_conditions.csv](data/operating_conditions.csv)

Default outputs:

- [outputs/synthetic_wcca_report.md](outputs/synthetic_wcca_report.md)
- [outputs/synthetic_wcca_summary.csv](outputs/synthetic_wcca_summary.csv)
- [outputs/missing_data_warnings.md](outputs/missing_data_warnings.md)
- [outputs/plots/](outputs/plots/)
- [captures/](captures/)

## Portfolio Evidence

- Synthetic input CSV: [data/synthetic_wcca_cases.csv](data/synthetic_wcca_cases.csv)
- Operating conditions CSV: [data/operating_conditions.csv](data/operating_conditions.csv)
- Generated calculation rows: 60 rows from 15 synthetic cases and 4 synthetic operating conditions
- Generated report: [outputs/synthetic_wcca_report.md](outputs/synthetic_wcca_report.md)
- Generated CSV summary: [outputs/synthetic_wcca_summary.csv](outputs/synthetic_wcca_summary.csv)
- Missing-data warnings: [outputs/missing_data_warnings.md](outputs/missing_data_warnings.md)
- Plot gallery:
  - [outputs/plots/margin_by_case.png](outputs/plots/margin_by_case.png)
  - [outputs/plots/worst_case_result_by_condition.png](outputs/plots/worst_case_result_by_condition.png)
  - [outputs/plots/pass_fail_distribution.png](outputs/plots/pass_fail_distribution.png)
  - [outputs/plots/thermal_temperature_sensitivity.png](outputs/plots/thermal_temperature_sensitivity.png)
  - [outputs/plots/voltage_sensitivity.png](outputs/plots/voltage_sensitivity.png)
- Mock captures:
  - [captures/cli_run_mock.md](captures/cli_run_mock.md)
  - [captures/generated_summary_table_mock.md](captures/generated_summary_table_mock.md)
  - [captures/plot_gallery_preview_mock.md](captures/plot_gallery_preview_mock.md)
  - [captures/report_preview_mock.md](captures/report_preview_mock.md)
  - [captures/test_run_output_mock.md](captures/test_run_output_mock.md)
- Equation review checklist: [docs/equation_review_checklist.md](docs/equation_review_checklist.md)
- Unit tests: [tests/test_calculations.py](tests/test_calculations.py)
- Proof asset tests: [tests/test_proof_assets.py](tests/test_proof_assets.py)
- CLI execution result: `WCCA results: 60 rows`; `Warnings: 3`; `Capture files: 5`

## Codex Contribution

Codex contributed the isolated project scaffold, CSV loaders, deterministic calculation engine, Markdown output structure, missing-data warnings, and calculation tests for this synthetic prototype.

## Jose Contribution

Jose defines the engineering workflow intent, WCCA preparation boundary, review expectations, synthetic automotive lighting framing, and final engineering judgment.

## Human Review Controls

- Treat generated outputs as draft WCCA preparation artifacts.
- Verify formulas, units, assumptions, thresholds, input data, output tables, and warning labels.
- Complete the reviewer checklist before representing the output as reviewed.
- Confirm all public examples remain synthetic or sanitized.
- Do not use the tool output as engineering approval.

## Screenshot Placeholders

- CLI run: [captures/cli_run_mock.md](captures/cli_run_mock.md)
- Input CSV: [data/synthetic_wcca_cases.csv](data/synthetic_wcca_cases.csv)
- Generated report: [captures/report_preview_mock.md](captures/report_preview_mock.md)
- Missing-data warning output: [outputs/missing_data_warnings.md](outputs/missing_data_warnings.md)
- Calculation output table: [captures/generated_summary_table_mock.md](captures/generated_summary_table_mock.md)
- Plot gallery preview: [captures/plot_gallery_preview_mock.md](captures/plot_gallery_preview_mock.md)

## Deterministic Calculation Summary

The engine applies synthetic tolerance corners using these simplified preparation rules:

- LED high-current corner = nominal LED current multiplied by operating-condition load factor, current tolerance, and sense-resistor tolerance.
- LED high-VF corner = nominal LED string voltage multiplied by the optional VF tolerance.
- Output power = LED high-current corner multiplied by LED high-VF corner.
- Switching-driver input current = output power divided by condition input voltage and low-corner efficiency.
- Linear-channel loss = voltage headroom multiplied by LED high-current corner.
- Switching-driver loss = output power multiplied by the calculated efficiency loss ratio.
- Topology-specific current stress estimates are deterministic approximations for prep screening only.
- Derating ratios compare calculated stress to synthetic rating columns.

Synthetic status thresholds:

- Ratio greater than 1.00: `Over synthetic limit`
- Ratio from 0.80 to 1.00: `Review required`
- Ratio below 0.80 with complete derating inputs: `Within synthetic prep limit`
- Missing derating inputs: `Review required`

## Proof Gaps

- Formulas are simplified WCCA preparation examples and need qualified engineering review before any public demo claim.
- Real screenshots are not captured yet; current captures are clearly labeled mock captures.
- Monte Carlo workflow is not included.
- Reviewer checklist completion is still needed: [docs/equation_review_checklist.md](docs/equation_review_checklist.md)
- The generated report remains draft output until reviewed against the sanitization checklist.

## Safe to Publish Status

Needs review. The data and code are synthetic, but the formulas, output labels, screenshots, and public presentation still require qualified engineering review.

## Next Improvements

- Complete the equation review checklist with reviewer name, date, and comments.
- Replace mock captures with real screenshots after final layout review.
- Add a one-page plot gallery screenshot for the portfolio page.
- Add AI narrative only after deterministic outputs are accepted through human review.
