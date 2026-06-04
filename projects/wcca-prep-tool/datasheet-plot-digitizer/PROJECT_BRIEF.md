# LED Datasheet Curve Studio - Project Brief

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

LED datasheet plots often encode forward voltage, current, temperature, luminous-flux, chromaticity, and derating behavior as images. Engineers need those curves in structured form for calculations and review packages, but manual point picking can be slow, inconsistent, and difficult to trace.

## Engineering Context

LED Datasheet Curve Studio is a local Streamlit engineering tool under the AI-Assisted WCCA Prep Tool. It converts public or synthetic LED datasheet plots into calibrated, reviewable curve data packages for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, and design-review preparation.

The tool is a data-preparation and review-support workflow. It does not approve LED design values, WCCA conclusions, thermal limits, optical predictions, or release decisions.

## Workflow

1. Start a synthetic or public LED datasheet-plot project.
2. Store project metadata, source metadata, target curve definitions, assumptions, and review status.
3. Import or preview a public/synthetic PDF or image source.
4. Select the plot region.
5. Calibrate x and y axes from known reference points.
6. Extract curve points manually first, then optionally use assisted extraction after review controls are in place.
7. Fit reviewable curve models and compare fit quality against raw points.
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
- Optional reviewed adapter package for WCCA and lighting-feasibility inputs

## Screenshots Or Screenshot Placeholders

- `captures/streamlit_workflow_mock.md`
- `outputs/overlay_forward_voltage_vs_current.png`
- Future capture: project setup and metadata screen
- Future capture: calibration screen
- Future capture: curve-fit validation screen
- Future capture: export package screen

## Sanitized Sample Data

Current demo assets use synthetic labels such as `SYN-LED-170`, `Synthetic LED Supplier`, `synthetic_datasheet_style_plot`, and `synthetic_page_20`. Future demo projects must stay synthetic or use clearly public LED datasheet examples with no proprietary customer, supplier, program, schematic, BOM, harness, cost, validation, internal requirement, ticket, part-number, file-path, repository, or internal-document details.

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

## Next Improvements

- Implement project model and `.ledcurve.json` save/load.
- Generate synthetic demo projects for common LED curve types.
- Harden calibration math and validation.
- Add curve-fit validation outputs.
- Package exports for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, and design-review preparation.
- Build a clearer Streamlit workflow UI.
- Add assisted extraction only after deterministic review controls are stable.
- Replace mock captures with reviewed screenshots.

## Proof Gaps

- Current assets are a minimum synthetic digitizer demo, not a complete project-managed Curve Studio workflow.
- `.ledcurve.json` save/load is not implemented yet.
- Calibration and curve-fit validation need expanded tests and report outputs.
- Streamlit crop/click behavior is not browser-verified in this checkout.
- Assisted extraction is not implemented as a reviewed workflow.
- A qualified engineering review has not signed off on the tool, fit approach, screenshots, or public claims.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The framing and sample data are synthetic and public-safe, but the implementation, captures, and engineering claims require qualified review before publication.
