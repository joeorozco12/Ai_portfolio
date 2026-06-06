# LED Datasheet Curve Studio - Project Brief

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

LED datasheet plots often encode forward voltage, current, temperature, luminous-flux, chromaticity, and derating behavior as images. Engineers need those curves in structured form for calculations and review packages, but manual point picking can be slow, inconsistent, and difficult to trace.

## Engineering Context

LED Datasheet Curve Studio is a supporting data-preparation tool under the AI-Assisted WCCA Prep Tool. It converts public or synthetic LED datasheet plots into calibrated, reviewable curve data packages for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, lighting-feasibility screening, and design-review preparation.

The tool is a data-preparation and review-support workflow, not a standalone AI demo. It does not approve LED design values, WCCA conclusions, thermal limits, optical predictions, feasibility conclusions, or release decisions.

## Workflow

1. Start a synthetic or public LED datasheet-plot project.
2. Store project metadata, source metadata, target curve definitions, assumptions, and review status in `.ledcurve.json`.
3. Use reusable synthetic seed projects or import a public/synthetic PDF or image source in the UI shell.
4. Select or record the plot region.
5. Calibrate x and y axes from known reference points.
6. Extract curve points manually first, with optional draft assisted candidates kept behind review controls.
7. Fit and validate a reviewable shape-preserving interpolation model from raw points.
8. Export CSV, JSON, Python lookup, MATLAB lookup, overlay image, and Markdown report artifacts.
9. Require qualified engineer review before downstream use.

## Inputs

- Public or synthetic LED datasheet PDF/image source
- Source page, source section, and plot-region metadata
- Curve name and intended downstream use
- X-axis and y-axis labels, units, scale type, and calibration points
- Manual or assisted curve-point picks
- Assumptions, engineering notes, review status, and reviewer comments

## Outputs

- `.ledcurve.json` project file for save/load workflow
- Digitized curve-points CSV
- Curve metadata JSON
- Python lookup function package
- MATLAB lookup function package
- Overlay verification image
- Markdown extraction report
- Reusable synthetic demo project files and point tables
- Structured demo export package under `exports/demo_export_package/`
- Planned optional reviewed adapter package for WCCA and lighting-feasibility inputs

## Screenshots Or Screenshot Placeholders

- `captures/streamlit_workflow_mock.md`
- `outputs/overlay_forward_voltage_vs_current.png`
- Future capture: project setup and metadata screen
- Future capture: calibration screen
- Future capture: curve-fit validation screen
- Future capture: export package screen

## Sanitized Sample Data

Current demo assets use synthetic labels such as `SYN-LED-170`, `SYN-LED-FVIF-001`, `Synthetic LED Supplier`, `synthetic_datasheet_style_plot`, and `synthetic_page_20`. Reusable demo projects under `data/demo_projects/` and point tables under `data/synthetic/` are synthetic seed data only. Future demo projects must stay synthetic or use clearly public LED datasheet examples with no proprietary customer, supplier, program, schematic, BOM, harness, cost, validation, internal requirement, ticket, part-number, file-path, repository, or internal-document details.

## Human Review Controls

- Axis calibration must be visible and reviewable before export.
- Raw points must remain available alongside fitted curves.
- Overlay review must be completed before downstream use.
- Export metadata must include source, calibration, extraction method, assumptions, fit model, and review status.
- Assisted extraction must be treated as draft until manual overlay review is complete.
- Downstream WCCA or feasibility adapters must require reviewed status before accepting data.
- The tool must state that AI-generated outputs are decision-support artifacts only.

## Codex Contribution

Codex helps scaffold the local tool, organize tasks, implement deterministic project and export logic, generate synthetic demo data, create tests, and draft public-safe documentation.

## Jose Contribution

Jose defines the automotive lighting workflow, WCCA and feasibility boundaries, relevant curve types, engineering review controls, publication safety rules, acceptance criteria, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured data extraction workflow design
- Metadata modeling for engineering traceability
- Deterministic transformation from pixels to engineering units
- Curve fitting and validation support
- Human-in-the-loop review gates
- Public-safe artifact generation

## Engineering Skills Demonstrated

- LED datasheet interpretation
- WCCA input preparation
- Thermal and optical curve-data preparation
- MATLAB/Python lookup generation
- Traceable engineering artifact packaging
- Design-review readiness support

## Risks And Mitigations

- Risk: Digitized plot data could be mistaken for guaranteed device limits. Mitigation: all artifacts mark plot data as reference-only and require qualified engineering review.
- Risk: Calibration mistakes could distort downstream calculations. Mitigation: preserve source pixels, calibration points, axis metadata, and overlay images.
- Risk: Curve fitting could hide bad extraction points. Mitigation: export raw points, fit model details, validation metrics, and reviewer status.
- Risk: Assisted extraction could create false confidence. Mitigation: keep assisted extraction draft-only until manual overlay review is complete.
- Risk: Public artifacts could expose controlled information. Mitigation: use synthetic or public examples only and keep publication classification explicit.

## Completed Work

- Deterministic `.ledcurve.json` project model, serialization, and save/load tests.
- Reusable synthetic LED curve seed projects for voltage/current, temperature/flux, current/flux, and thermal derating workflows.
- Synthetic point tables that preserve source pixels, engineering units, labels, publication classification, and review status.
- Calibration helpers for linear/log axes, reversed image-axis behavior, source-pixel traceability, and sanity metadata.
- Shape-preserving interpolation helpers, curve-fit validation helpers, and lookup export generation.
- Manual extraction conversion and draft assisted candidate grouping with explicit downstream-use gates.
- `run_demo.py` synthetic artifact generation for CSV, JSON, Python, MATLAB, overlay PNG, Markdown report outputs, and `exports/demo_export_package/`.
- Current screenshot placeholder and overlay artifact for portfolio review.

## Next Improvements

- Build a clearer Streamlit workflow UI.
- Integrate the full validation report into generated review packages and the Streamlit review screen.
- Add browser-verified screenshots after runtime dependencies are installed.
- Wire draft assisted extraction preview into the UI only after manual review controls are browser-verified.
- Add reviewed downstream adapters for WCCA and lighting-feasibility inputs.
- Replace mock captures with reviewed screenshots.

## Proof Gaps

- Current assets are synthetic and do not prove extraction quality on a real public datasheet.
- The project model is implemented in the deterministic core, but the Streamlit shell does not expose full project save/load yet.
- Full validation output exists in the deterministic core but is not fully wired into the generated review report or UI yet.
- Streamlit crop/click behavior is not browser-verified in this checkout.
- Assisted extraction is draft candidate grouping only; it is not a reviewed image-recognition workflow and has not been validated on real public datasheets.
- A qualified engineering review has not signed off on the tool, fit approach, screenshots, or public claims.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The framing and sample data are synthetic and public-safe, but the implementation, captures, and engineering claims require qualified review before publication.
