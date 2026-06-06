# LED Datasheet Curve Export Package

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

LED datasheet-style plots often contain useful voltage, current, temperature, and flux behavior in image form. Engineers need structured, traceable curve data for WCCA preparation, feasibility screening, simulation, and design-review discussion.

## Engineering Context

This package demonstrates a synthetic automotive-lighting data-prep workflow. It uses synthetic LED identifiers and synthetic plot points only. It does not include proprietary datasheets, customer programs, supplier records, internal requirements, schematics, BOM data, harness data, cost data, validation results, ticket numbers, repository names, file paths, or internal-document details.

## Workflow

1. Load a public or synthetic datasheet plot image.
2. Select the plot region and record source metadata.
3. Calibrate the x and y axes from known reference points.
4. Digitize curve points by manual picking first.
5. Fit a shape-preserving interpolation model for lookup generation.
6. Export raw points, metadata, lookup functions, overlay, and this report for review.
7. Require qualified engineering review before downstream use.

## Inputs

- Curve name: `forward_voltage_vs_forward_current`
- Source: `synthetic_datasheet_style_plot`
- Source page: `synthetic_page_20`
- Source section: `synthetic_forward_current_characteristics`
- X axis: `Forward Voltage` `V`
- Y axis: `Forward Current` `mA`
- Digitization method: `manual_calibration_plus_manual_curve_pick`
- Digitized points: `8`

## Outputs

- CSV points: `data/digitized_curve_points.csv`
- JSON metadata: `metadata/export_manifest.json`
- Python lookup function: `lookups/python/lookup_forward_voltage_vs_forward_current.py`
- MATLAB lookup function: `lookups/matlab/lookup_forward_voltage_vs_forward_current.m`
- Overlay verification image: `review/overlay_forward_voltage_vs_forward_current.png`
- Markdown extraction report: `this file`
- Source metadata JSON: `metadata/source_metadata.json`
- Calibration metadata JSON: `metadata/calibration_metadata.json`

## Screenshots Or Screenshot Placeholders

- Overlay verification image: `review/overlay_forward_voltage_vs_forward_current.png`
- Streamlit workflow placeholder: `captures/streamlit_workflow_mock.md`
- Future capture: export package review screen

## Sanitized Sample Data

The sample extraction uses `SYN-LED-170` from `Synthetic LED Supplier`. These are synthetic demonstration labels, not real device or supplier identifiers. The extracted x range is `2.800` to `3.850` V; the extracted y range is `50.0` to `3900.0` mA.

## Source Metadata

- Source category: `synthetic`
- Source type: `datasheet_plot_image`
- Source name: `synthetic_datasheet_style_plot`
- Source page: `synthetic_page_20`
- Source section: `synthetic_forward_current_characteristics`
- Crop region px: `{'left': 60, 'top': 40, 'width': 540, 'height': 410}`
- Source note: Synthetic or public source only. No proprietary source details are included in this package.

## Calibration Metadata

- X axis calibration: `{'label': 'Forward Voltage', 'unit': 'V', 'scale': 'linear', 'pixel_low': 80.0, 'pixel_high': 560.0, 'value_low': 2.5, 'value_high': 4.5}`
- Y axis calibration: `{'label': 'Forward Current', 'unit': 'mA', 'scale': 'linear', 'pixel_low': 420.0, 'pixel_high': 60.0, 'value_low': 0.0, 'value_high': 4000.0}`
- Calibration review status: `draft`
- Calibration note: Calibration values must be checked against the source plot before the exported curve is used downstream.

## Assumptions

- Source plot is synthetic or public and cleared for demonstration use.
- Manual axis calibration points were entered by the operator.
- Manual curve picks are treated as draft until overlay review is complete.
- Digitized plot data is reference-only and not a guaranteed device limit.

## Method

- Digitization method: `manual_calibration_plus_manual_curve_pick`
- Package generator: `LED Datasheet Curve Studio deterministic exporter`
- AI boundary: AI-assisted output is decision support only; the exporter does not approve engineering data.

## Fit Model

- Model name: `pchip_shape_preserving_interpolation`
- Model family: `shape_preserving_piecewise_cubic_interpolation`
- Segment count: `7`
- Fit domain: `{'x_min': 2.8, 'x_max': 3.85, 'x_unit': 'V'}`
- Out-of-range behavior: Endpoint clamping in generated lookup functions; not approved for engineering extrapolation.
- Raw points exported: `True`

## Validation Status

- Status: `draft_validation_pending_engineer_review`
- Summary: Deterministic export prechecks completed; manual overlay and qualified engineering review remain required.
- Checks: `[{'name': 'point_count_at_least_two', 'status': 'pass', 'detail': 'deterministic export precheck'}, {'name': 'unique_x_values', 'status': 'pass', 'detail': 'deterministic export precheck'}, {'name': 'strictly_increasing_x', 'status': 'pass', 'detail': 'deterministic export precheck'}, {'name': 'source_pixels_available', 'status': 'pass', 'detail': 'deterministic export precheck'}, {'name': 'manual_overlay_review', 'status': 'pending_engineer_review', 'detail': 'Overlay image must be reviewed against the source plot.'}]`

## Review Status

- Status: `draft_extraction`
- Reviewer: `not_assigned`
- Reviewed at UTC: `not_reviewed`
- Requires qualified engineer review: `True`

## Downstream Use Warnings

- Do not use this export for WCCA, feasibility simulation, thermal derating, luminous-flux prediction, design review, or design decisions until a qualified engineer reviews and accepts it.
- Lookup functions clamp outside the digitized x-range; they are not validated extrapolation models.
- Curve-fit coefficients must be checked against the raw points and overlay image before downstream use.
- Synthetic demo identifiers are not real device, supplier, customer, program, schematic, BOM, harness, cost, validation, ticket, repository, or internal-document references.

## Human Review Controls

- Manual axis calibration is required before export.
- Curve points remain draft until a qualified reviewer checks them.
- Overlay review is required before use in WCCA or feasibility inputs.
- Source page, crop region, calibration metadata, method, fit model, validation status, and review status are preserved.
- The reviewer must confirm that plot data is reference-only and not a guaranteed device limit.
- The tool does not approve LED design values.

## Codex Contribution

Codex scaffolded the deterministic export package, report builder, lookup artifacts, synthetic sample package, and focused tests.

## Jose Contribution

Jose defines the LED engineering data-prep use case, WCCA and feasibility workflow boundary, required review controls, acceptable public/synthetic source boundary, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured data extraction workflow
- Metadata modeling for engineering traceability
- Deterministic transformation from pixels to engineering units
- Curve-fit generation from reviewed samples
- Human-in-the-loop review gates
- Public-safe artifact generation

## Engineering Skills Demonstrated

- LED forward-voltage and current curve interpretation
- Datasheet plot traceability
- WCCA input preparation
- Simulation lookup-table preparation
- Engineering review governance
- Reviewable export-package design

## Risks And Mitigations

- Risk: Digitized plot points could be mistaken for guaranteed limits. Mitigation: every export states that plot data is reference-only and requires engineering review.
- Risk: Calibration errors could distort the curve. Mitigation: manual axis calibration, overlay review, source-pixel export, and reviewer status are required.
- Risk: A curve fit could oversmooth engineering behavior. Mitigation: raw points, fit metadata, validation status, and PCHIP coefficients are exported for review.
- Risk: Lookup functions could be used as unreviewed downstream inputs. Mitigation: report and JSON metadata warn that WCCA, feasibility, thermal, optical, and design-review use requires qualified engineering review.
- Risk: Public output could reveal controlled data. Mitigation: included samples are synthetic and public use requires sanitized/public source review.

## Completed Work

- Synthetic source metadata, crop metadata, calibration metadata, assumptions, method, fit model, validation status, and review status are exported.
- Raw source-pixel points are preserved alongside engineering-unit values.
- Python and MATLAB lookup artifacts are generated from draft PCHIP coefficients.
- Overlay image and Markdown report artifacts are generated for review.
- Downstream-use warnings and human-review controls are visible in the package.

## Next Improvements

- Add a reviewed-status gate for downstream WCCA and feasibility adapters.
- Add browser-based image click capture for calibration and curve picking.
- Add optional assisted extraction after manual-review controls are stable.
- Integrate the full curve-fit validation report into this generated package and the Streamlit review workflow.
- Add multi-curve export packaging from one source plot.
- Replace mock captures with reviewed screenshots.

## Proof Gaps

- The current generated sample is synthetic and does not prove extraction quality on a real public datasheet.
- Validation status is an export precheck in this generated report; qualified engineering review is still required.
- Streamlit image click/crop interaction still needs a browser component or custom canvas package.
- Optional PDF rendering and assisted extraction require runtime dependencies from `requirements.txt`.
- A qualified engineering review signoff has not been completed.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The code and sample data are synthetic and sanitized, but the tool behavior, screenshots, and public framing still require qualified engineering review before publication.
