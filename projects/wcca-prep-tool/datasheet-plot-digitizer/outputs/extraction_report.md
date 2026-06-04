# LED Datasheet Plot Digitizer & Curve-Fit Builder

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

LED datasheet-style plots often contain useful voltage, current, temperature, and flux behavior in image form. Engineers need structured, traceable curve data for WCCA preparation, feasibility screening, simulation, and design-review discussion.

## Engineering Context

This artifact demonstrates a synthetic automotive-lighting data-prep workflow. It uses a synthetic LED identifier and synthetic plot points only. It does not include proprietary datasheets, customer programs, supplier records, internal requirements, schematics, BOM data, harness data, cost data, or validation results.

## Workflow

1. Load a public or synthetic datasheet plot image.
2. Select the plot region.
3. Calibrate the x and y axes from known reference points.
4. Digitize curve points by manual picking first.
5. Fit a shape-preserving interpolation model.
6. Export reviewed CSV, JSON, Python, MATLAB, overlay, and report artifacts.

## Inputs

- Curve name: `forward_voltage_vs_forward_current`
- Source: `synthetic_datasheet_style_plot`
- Source page: `synthetic_page_20`
- X axis: `Forward Voltage` `V`
- Y axis: `Forward Current` `mA`
- Digitization method: `manual_calibration_plus_manual_curve_pick`
- Digitized points: `8`

## Outputs

- CSV points: `outputs/digitized_curve_points.csv`
- JSON metadata: `outputs/curve_metadata.json`
- Python lookup function: `outputs/python/lookup_forward_voltage_vs_forward_current.py`
- MATLAB lookup function: `outputs/matlab/lookup_forward_voltage_vs_forward_current.m`
- Overlay verification image: `outputs/overlay_forward_voltage_vs_current.png`
- Markdown extraction report: this file

## Screenshots Or Screenshot Placeholders

- Overlay verification image: `outputs/overlay_forward_voltage_vs_current.png`
- Streamlit workflow placeholder: `captures/streamlit_workflow_mock.md`

## Sanitized Sample Data

The sample extraction uses `SYN-LED-170` from `Synthetic LED Supplier`. These are synthetic demonstration labels, not real device identifiers. The extracted x range is `2.800` to `3.850` V; the extracted y range is `50.0` to `3900.0` mA.

## Human Review Controls

- Manual axis calibration is required before export.
- Curve points remain `draft_extraction` until a qualified reviewer checks them.
- Overlay review is required before use in WCCA or feasibility inputs.
- Source page and digitization method are exported with every row.
- The reviewer must confirm that plot data is reference-only and not a guaranteed device limit.
- The tool does not approve LED design values.

## Codex Contribution

Codex scaffolded the Streamlit app shell, deterministic calibration math, PCHIP curve-fit builder, export modules, synthetic sample data, overlay generator, and unit tests.

## Jose Contribution

Jose defines the LED engineering data-prep use case, WCCA and feasibility workflow boundary, required review controls, acceptable public/synthetic source boundary, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured data extraction workflow
- Deterministic transformation from pixels to engineering units
- Curve-fit generation from reviewed samples
- Metadata-rich export generation
- Testable human-in-the-loop automation

## Engineering Skills Demonstrated

- LED forward-voltage and current curve interpretation
- Datasheet plot traceability
- WCCA input preparation
- Simulation lookup-table preparation
- Engineering review governance

## Risks And Mitigations

- Risk: Digitized plot points could be mistaken for guaranteed limits. Mitigation: every export states that plot data is reference-only and requires engineering review.
- Risk: Calibration errors could distort the curve. Mitigation: manual axis calibration, overlay review, source-pixel export, and reviewer status are required.
- Risk: A curve fit could oversmooth engineering behavior. Mitigation: the MVP uses shape-preserving PCHIP coefficients and exports raw points alongside the fitted model.
- Risk: Public output could reveal controlled data. Mitigation: included samples are synthetic and public use requires sanitized/public source review.

## Next Improvements

- Add browser-based image click capture for calibration and curve picking.
- Add optional OpenCV-assisted extraction after manual picks are accepted.
- Add log-axis support to the Streamlit workflow.
- Add multi-curve extraction from a single plot image.
- Add a reviewed adapter that feeds WCCA and Project 5 feasibility inputs only after approval.

## Proof Gaps

- The current generated sample is synthetic and does not prove extraction quality on a real public datasheet.
- Streamlit image click/crop interaction still needs a browser component or custom canvas package.
- Optional PDF rendering and OpenCV extraction require installing runtime dependencies from `requirements.txt`.
- A qualified engineering review signoff has not been completed.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The code and sample data are synthetic and sanitized, but the tool behavior, screenshots, and public framing still require qualified engineering review before publication.
