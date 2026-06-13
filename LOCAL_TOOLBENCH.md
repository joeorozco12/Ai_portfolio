# Local CLI Toolbench Runbook

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Safe to publish

## Purpose

This runbook is the local starting point for Jose's deterministic portfolio toolbench. It focuses on command-line workflows, generated Markdown/CSV/PNG outputs, review checklists, and proof drafts. It does not prioritize Streamlit, website publishing, or new AI/API dependencies.

The June 12, 2026 target for this runbook is the interview-ready local toolbench. The public QR console is tracked separately under [ux-console](ux-console) and [UNVEIL_READINESS.md](UNVEIL_READINESS.md). Jose completed the qualified synthetic portfolio review pass on 2026-06-13. Generated deterministic outputs may still carry `Needs review` labels by design because they are decision-support artifacts; source review docs now record the accepted synthetic-publication disposition.

## Interview Demo Path

Use [UNVEIL_READINESS.md](UNVEIL_READINESS.md) as the demo checklist.

Recommended non-UX walkthrough order:

1. Project 1 Requirements-to-Verification Tool
2. Project 6 LED Datasheet-to-Model Extractor deterministic evidence, implemented as LED Datasheet Curve Studio under Project 2
3. Project 5 Lighting Feasibility Mini-Simulator
4. Project 2 AI-Assisted WCCA Prep Tool
5. Project 4 Design Review Readiness Assistant
6. Project 3 Codex Tool Development Case Study

The old `AI Studio Engineering Bridge Demo` framing is appendix-only for this reveal. The active Project 6 framing is `LED Datasheet-to-Model Extractor`, with reviewed extractor outputs intended to feed Project 5 only through a future reviewed adapter.

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

Project 3 is documentation/case-study evidence rather than a generated engineering calculation workflow. Inspect its synthetic captures manually under `projects/codex-tool-development-case-study/captures/`.

Run this style check before final review:

```bash
git diff --check
```

## Run One Project

| Project | Command | Main Inputs | Main Outputs |
|---|---|---|---|
| Project 1: Requirements-to-Verification | `python3 tools/requirements_to_verification.py --input "Synthetic Requirements Sample.csv" --output projects/requirements-to-verification/generated_outputs` | `Synthetic Requirements Sample.csv` | `projects/requirements-to-verification/generated_outputs/trace_matrix.*`, `ambiguity_report.*`, `assumptions_register.*`, `review_checklist.*`, `run_summary.md` |
| Project 6: LED Datasheet-to-Model Extractor evidence | `cd projects/wcca-prep-tool/datasheet-plot-digitizer && python3 run_demo.py` | synthetic curve points and `.ledcurve.json` demo projects | `outputs/`, `exports/demo_export_package/`, overlay PNG, Python/MATLAB lookup files |
| Project 2: WCCA Prep Tool | `cd projects/wcca-prep-tool && python3 -m wcca_prep.cli` | `data/synthetic_wcca_cases.csv`, `data/operating_conditions.csv` | `outputs/synthetic_wcca_report.md`, `outputs/synthetic_wcca_summary.csv`, `outputs/missing_data_warnings.md`, `outputs/plots/`, `captures/` |
| Project 4: Design Review Readiness Assistant | `cd projects/design-review-readiness-assistant && python3 demo_project4.py` | `inputs/synthetic_lighting_review_notes.md` | `outputs/design_review_packet.md`, `risk_register.csv`, `mode_to_test_matrix.*`, `diagnostic_response_table.*`, `screenshots/` |
| Project 5: Lighting Feasibility Mini-Simulator | `cd projects/lighting-feasibility-mini-simulator && python3 feasibility_engine.py` | `data/synthetic_lighting_cases.csv` | `outputs/feasibility_summary.*`, `outputs/plots/`, `outputs/screenshots/portfolio_capture_summary.md`, `outputs/sensitivity/` |
| Project 3: Codex Tool Development Case Study | Manual review | `projects/codex-tool-development-case-study/examples/` | `captures/`, `codex_workflow_case_study.md`, `validation_checklist.md` |

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

## Review Baseline

- Formulas/rules: calculations, deterministic mappings, thresholds, status logic, and rule names were reviewed for synthetic portfolio demonstration use.
- Assumptions: generated assumptions registers, warning files, equation review docs, and sensitivity ranges were reviewed for public-safe synthetic use.
- Synthetic data: all inputs and outputs must remain synthetic or sanitized automotive-lighting examples.
- Screenshots/captures: mock captures and generated screenshots remain portfolio proof assets, not final engineering evidence.
- Publication wording: public-facing artifacts must keep the synthetic label, human-review note, proof gaps, and decision-support boundary visible. Generated outputs can retain `Needs review` where that label is part of the workflow gate.

## What Not To Claim Yet

- Do not claim a live portfolio website until the GitHub Pages workflow is deployed and verified in a clean browser.
- Do not claim Streamlit or interactive UI completion for any project.
- Do not claim Curve Studio is a completed browser-verified app.
- Do not claim AI Studio Bridge is the active Project 6 proof item; keep it as appendix-only context.
- Do not imply AI is the decision owner for requirements, WCCA results, design readiness, feasibility, diagnostics, or release decisions.
- Do not treat generated plots, CSVs, screenshots, or reports as engineering approval. The review pass is for synthetic portfolio publication only.

## Review Output Map

- Project 1 review checklist: `projects/requirements-to-verification/generated_outputs/review_checklist.md`
- Project 6 extractor package: `projects/wcca-prep-tool/datasheet-plot-digitizer/exports/demo_export_package/`
- WCCA equation checklist: `projects/wcca-prep-tool/docs/equation_review_checklist.md`
- Project 3 validation checklist: `projects/codex-tool-development-case-study/validation_checklist.md`
- Project 4 review packet: `projects/design-review-readiness-assistant/outputs/design_review_packet.md`
- Project 5 equation review: `projects/lighting-feasibility-mini-simulator/docs/equation_review.md`

## Known Limitations

- All workflows are deterministic local prototypes using synthetic data.
- No new AI/API dependency is introduced in this sprint.
- Mock captures are not final portfolio screenshots.
- Curve Studio deterministic exports are useful as Project 6 extractor evidence, but the interactive workflow remains unverified.
- Project 3 captures are synthetic Markdown captures, not live IDE or terminal screenshots.
- Future formula, threshold, input-schema, adapter, UI, or publication-route changes require a new review pass. Generated outputs may continue to show `Needs review` to preserve the human-review boundary.
