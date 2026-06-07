# Interview And QR Console Readiness

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Interview Demo Target

Target date: Friday, June 12, 2026

This file is the source of truth for the interview-ready local demo plus the QR-accessible static console. The goal is to show deterministic engineering workflow tools, browser-only synthetic demos, generated proof assets, and explicit human-review controls. It does not promote any artifact to final engineering approval.

## Demo Order

| Order | Tool | Command | Main Evidence | Reveal Status |
|---|---|---|---|---|
| 1 | Requirements-to-Verification Tool | `python3 tools/requirements_to_verification.py --input "Synthetic Requirements Sample.csv" --output projects/requirements-to-verification/generated_outputs` | Trace matrix, ambiguity report, assumptions register, review checklist, capture previews | Ready for local demo after regeneration and review |
| 2 | LED Datasheet-to-Model Extractor | `cd projects/wcca-prep-tool/datasheet-plot-digitizer && python3 run_demo.py` | Digitized curve CSV, metadata JSON, Python/MATLAB lookup files, overlay PNG, extraction report | Deterministic extractor evidence ready; Streamlit UI remains unverified |
| 3 | Lighting Feasibility Mini-Simulator | `cd projects/lighting-feasibility-mini-simulator && python3 feasibility_engine.py` | Feasibility summary, plots, sensitivity sweeps, Project 6 reviewed-input boundary | Ready for local demo after equation review remains visibly pending |
| 4 | AI-Assisted WCCA Prep Tool | `cd projects/wcca-prep-tool && python3 -m wcca_prep.cli` | WCCA report, summary CSV, plot gallery, missing-data warnings, equation checklist | Ready for local demo after formulas remain clearly review-required |
| 5 | Design Review Readiness Assistant | `cd projects/design-review-readiness-assistant && python3 demo_project4.py` | Review packet, risk register, mode-to-test matrix, diagnostic table, generated screenshots | Ready for local demo |
| 6 | Codex Tool Development Case Study | Manual walkthrough of `projects/codex-tool-development-case-study/` | Prompt, scope, validation, and human-review capture artifacts | Ready after capture checklist review |

## Validation Commands

Run the full non-UX toolbench from the repo root:

```bash
python3 tools/validate_portfolio_toolbench.py
```

Run style and whitespace checks before the final walkthrough:

```bash
git diff --check
```

Project-specific checks:

```bash
cd projects/requirements-to-verification && python3 -m unittest discover -s tests
cd projects/wcca-prep-tool && python3 -m unittest discover -s tests
cd projects/wcca-prep-tool/datasheet-plot-digitizer && python3 -m unittest discover -s tests
cd projects/design-review-readiness-assistant && python3 scripts/validate_project4_outputs.py
cd projects/lighting-feasibility-mini-simulator && python3 -m unittest discover -s tests
```

Run the QR console checks from the repo root:

```bash
python3 tools/generate_ux_console_data.py --check
python3 -m unittest discover -s tests
python3 tools/validate_ux_console_review.py
```

## Public QR Console

Static site root: `ux-console/`

QR route after GitHub Pages deployment:

```text
https://<github-user>.github.io/<repo>/tools
```

Deep links:

- `/tools/requirements`
- `/tools/feasibility`
- `/tools/wcca`
- `/tools/design-review`
- `/tools/evidence`

The console provides live browser-only synthetic demos for Requirements-to-Verification and Lighting Feasibility, plus evidence dashboards for WCCA Prep, Design Review Readiness, and portfolio evidence. It requires no backend, login, API keys, uploads, or proprietary data.

## Current Proof Assets

| Tool | Inputs | Outputs | Captures / Screenshots | Human Review Gate |
|---|---|---|---|---|
| Project 1 Requirements-to-Verification | `Synthetic Requirements Sample.csv` | `projects/requirements-to-verification/generated_outputs/` | `projects/requirements-to-verification/captures/` | Requirement interpretation, verification mappings, ambiguity findings, assumptions |
| Project 6 LED Datasheet-to-Model Extractor | Synthetic curve points and demo projects | `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/` and `exports/demo_export_package/` | Overlay PNG plus Streamlit mock capture | Axis calibration, point picks, fit quality, downstream-use review gate |
| Project 5 Lighting Feasibility Mini-Simulator | `projects/lighting-feasibility-mini-simulator/data/synthetic_lighting_cases.csv` | `outputs/feasibility_summary.*`, plots, and sensitivity sweeps | `outputs/screenshots/portfolio_capture_summary.md` plus plot PNGs | Equation set, thresholds, sensitivity ranges, screening interpretation |
| Project 2 WCCA Prep Tool | `projects/wcca-prep-tool/data/` CSV files | WCCA report, summary CSV, missing-data warnings, plot gallery | `projects/wcca-prep-tool/captures/` plus plot PNGs | Formulas, units, tolerance assumptions, derating thresholds |
| Project 4 Design Review Readiness Assistant | `inputs/synthetic_lighting_review_notes.md` | Review packet, risk register, assumptions, validation gaps, matrices | `projects/design-review-readiness-assistant/screenshots/` | Risk labels, readiness language, reviewer disposition, validation gaps |
| Project 3 Codex Tool Development Case Study | Synthetic task and scope examples | Case-study Markdown and validation checklist | `projects/codex-tool-development-case-study/captures/` | Claim wording, scoped-work evidence, validation log, no proprietary detail |

## Talk Track Boundaries

- Say: these are deterministic local prototypes that structure engineering workflow evidence using synthetic data.
- Say: the QR console is a static browser-only interview surface once GitHub Pages deployment is verified.
- Say: Codex accelerates artifact creation, validation scaffolding, and review-package generation.
- Say: Jose owns engineering framing, review criteria, acceptance decisions, and final judgment.
- Do not say: AI is the decision owner for requirements, WCCA results, feasibility, diagnostics, design readiness, or release decisions.
- Do not say: the Streamlit digitizer path is browser-verified.
- Do not say: the public QR site is live until the GitHub Pages URL has deployed and loaded in a clean browser.

## Remaining Proof Gaps

- All projects remain `Needs review` until Jose completes a qualified engineering and publication review pass.
- Project 1 now has enough synthetic row coverage for the interview demo, but reviewer disposition fields remain placeholders.
- Project 2 formulas and WCCA assumptions still need checklist completion.
- Project 3 captures are synthetic Markdown captures, not live screenshots.
- Project 5 equations and thresholds are first-pass screening examples only.
- Project 6 is represented by the deterministic LED Datasheet Curve Studio / LED Datasheet-to-Model Extractor evidence. The old AI Studio Bridge demo should stay secondary or appendix-only.
- The GitHub Pages workflow still needs a configured GitHub remote and successful Actions deployment before final QR generation.

## Safe To Publish Status

Needs review. The demo package and static console use synthetic examples only, but final publication and QR use require a successful GitHub Pages deployment plus qualified review.
