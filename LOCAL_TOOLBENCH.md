# Local CLI Toolbench Runbook

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Purpose

This runbook is the local starting point for Jose's deterministic portfolio toolbench. It focuses on command-line workflows, generated Markdown/CSV/PNG outputs, review checklists, and proof drafts. It does not prioritize Streamlit, website publishing, or new AI/API dependencies.

All outputs in this sprint are draft decision-support artifacts. Keep every project at `Needs review` until Jose completes a qualified human review pass.

## Run All

From the repo root:

```bash
python3 tools/validate_portfolio_toolbench.py
```

The validator regenerates and checks the four primary local workflows:

- Project 1 Requirements-to-Verification
- Project 2 AI-Assisted WCCA Prep Tool
- Project 4 Design Review Readiness Assistant
- Project 5 Lighting Feasibility Mini-Simulator

It also runs LED Datasheet Curve Studio deterministic checks as a secondary, non-release-blocking review package. Curve Studio is not treated as a completed interactive app until the Streamlit workflow is browser-verified.

Run this style check before final review:

```bash
git diff --check
```

## Run One Project

| Project | Command | Main Inputs | Main Outputs |
|---|---|---|---|
| Project 1: Requirements-to-Verification | `python3 tools/requirements_to_verification.py --input "Synthetic Requirements Sample.csv" --output projects/requirements-to-verification/generated_outputs` | `Synthetic Requirements Sample.csv` | `projects/requirements-to-verification/generated_outputs/trace_matrix.*`, `ambiguity_report.*`, `assumptions_register.*`, `review_checklist.*`, `run_summary.md` |
| Project 2: WCCA Prep Tool | `cd projects/wcca-prep-tool && python3 -m wcca_prep.cli` | `data/synthetic_wcca_cases.csv`, `data/operating_conditions.csv` | `outputs/synthetic_wcca_report.md`, `outputs/synthetic_wcca_summary.csv`, `outputs/missing_data_warnings.md`, `outputs/plots/`, `captures/` |
| Project 4: Design Review Readiness Assistant | `cd projects/design-review-readiness-assistant && python3 demo_project4.py` | `inputs/synthetic_lighting_review_notes.md` | `outputs/design_review_packet.md`, `risk_register.csv`, `mode_to_test_matrix.*`, `diagnostic_response_table.*`, `screenshots/` |
| Project 5: Lighting Feasibility Mini-Simulator | `cd projects/lighting-feasibility-mini-simulator && python3 feasibility_engine.py` | `data/synthetic_lighting_cases.csv` | `outputs/feasibility_summary.*`, `outputs/plots/`, `outputs/screenshots/portfolio_capture_summary.md`, `outputs/sensitivity/` |

## Project Tests

```bash
cd projects/requirements-to-verification && python3 -m unittest discover -s tests
cd projects/wcca-prep-tool && python3 -m unittest discover -s tests
cd projects/design-review-readiness-assistant && python3 scripts/validate_project4_outputs.py
cd projects/lighting-feasibility-mini-simulator && python3 -m unittest discover -s tests
```

Secondary Curve Studio checks:

```bash
cd projects/wcca-prep-tool/datasheet-plot-digitizer
python3 run_demo.py
python3 -m unittest discover -s tests
```

## What Jose Should Review

- Formulas/rules: verify calculations, deterministic mappings, thresholds, status logic, and rule names before discussing outputs externally.
- Assumptions: inspect generated assumptions registers, warning files, equation review docs, sensitivity ranges, and placeholder reviewer fields.
- Synthetic data: confirm all inputs and outputs use only synthetic or sanitized automotive-lighting examples.
- Screenshots/captures: keep mock captures and generated screenshots labeled as draft proof until the visuals are reviewed.
- Publication wording: confirm every public-facing artifact includes the synthetic label, human-review note, proof gaps, and `Needs review` classification.

## What Not To Claim Yet

- Do not claim a live portfolio website or publishing workflow from this sprint.
- Do not claim Streamlit or interactive UI completion for any project.
- Do not claim Curve Studio is a completed browser-verified app.
- Do not imply AI approves requirements, WCCA results, design readiness, feasibility, diagnostics, or release decisions.
- Do not treat generated plots, CSVs, screenshots, or reports as reviewed engineering evidence until Jose completes the review pass.

## Review Output Map

- Project 1 review checklist: `projects/requirements-to-verification/generated_outputs/review_checklist.md`
- WCCA equation checklist: `projects/wcca-prep-tool/docs/equation_review_checklist.md`
- Project 4 review packet: `projects/design-review-readiness-assistant/outputs/design_review_packet.md`
- Project 5 equation review: `projects/lighting-feasibility-mini-simulator/docs/equation_review.md`
- Curve Studio secondary package: `projects/wcca-prep-tool/datasheet-plot-digitizer/exports/demo_export_package/`

## Known Limitations

- All workflows are deterministic local prototypes using synthetic data.
- No new AI/API dependency is introduced in this sprint.
- Mock captures are not final portfolio screenshots.
- Curve Studio deterministic exports are useful as a secondary review package, but the interactive workflow remains unverified.
- Everything remains `Needs review` until qualified human review is complete.
