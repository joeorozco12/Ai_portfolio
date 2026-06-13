# LED Datasheet-to-Model Extractor

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Project Role

This is the active Project 6 framing for the June 12, 2026 interview package and QR console evidence. The deterministic evidence lives in [projects/wcca-prep-tool/datasheet-plot-digitizer](projects/wcca-prep-tool/datasheet-plot-digitizer) as LED Datasheet Curve Studio.

The old `AI Studio Engineering Bridge Demo` is appendix-only context. It should not be presented as the main Project 6 proof item.

## Problem

LED datasheet plots often need to become structured model inputs before they can support WCCA prep, feasibility screening, thermal derating, MATLAB/Python lookup functions, or design-review packets. Raw extraction is not enough; the values need source metadata, calibration metadata, fit validation, downstream-use warnings, and qualified human review.

## Engineering Context

This project uses synthetic LED datasheet-style curves only. It demonstrates the workflow pattern for converting review-controlled curve points into traceable model artifacts. It does not use proprietary datasheets, supplier part numbers, customer data, internal requirements, schematics, BOMs, validation results, cost data, file paths, ticket numbers, or program identifiers.

Deterministic evidence is ready for synthetic portfolio discussion. The interactive Streamlit/browser path is pending verification and should not be described as complete, deployed, or browser-verified.

## Workflow

1. Load synthetic curve points or a synthetic `.ledcurve.json` project.
2. Preserve source, crop, axis, calibration, point, and assumption metadata.
3. Generate a shape-preserving lookup model.
4. Export CSV, metadata JSON, Python lookup, MATLAB lookup, overlay PNG, and a Markdown report.
5. Require manual calibration, overlay review, and qualified engineer review before downstream use.

## Inputs

- Synthetic point tables under `projects/wcca-prep-tool/datasheet-plot-digitizer/data/synthetic/`
- Synthetic demo projects under `projects/wcca-prep-tool/datasheet-plot-digitizer/data/demo_projects/`
- Synthetic manual point seed data under `projects/wcca-prep-tool/datasheet-plot-digitizer/data/synthetic_manual_points.csv`

## Outputs

- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/digitized_curve_points.csv`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/curve_metadata.json`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/overlay_forward_voltage_vs_current.png`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/python/lookup_forward_voltage_vs_forward_current.py`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/matlab/lookup_forward_voltage_vs_forward_current.m`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/extraction_report.md`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/exports/demo_export_package/`

## Screenshots Or Capture Placeholders

- `projects/wcca-prep-tool/datasheet-plot-digitizer/outputs/overlay_forward_voltage_vs_current.png`
- `projects/wcca-prep-tool/datasheet-plot-digitizer/captures/streamlit_workflow_mock.md`

The Streamlit capture is a placeholder only. It is not browser-verified screenshot evidence.

## Human Review Controls

- Manual calibration and overlay review remain required before export use.
- Assisted extraction is draft-only and cannot replace engineer review.
- Exported curves are reference data only, not guaranteed device limits.
- Project 5 must consume only reviewed Project 6 model records through a future adapter.
- AI does not approve LED model values or downstream engineering decisions.

## Codex Contribution

Codex contributed the deterministic project model, calibration helpers, curve-fit/export modules, report generator, lookup-file generation, synthetic data packages, and tests.

## Jose Contribution

Jose defines the LED datasheet-to-model workflow, downstream WCCA/feasibility use case, review boundary, accepted export formats, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured extraction workflow design
- Metadata-rich artifact generation
- Deterministic model generation
- Test generation
- Human-in-the-loop review gating

## Engineering Skills Demonstrated

- LED datasheet curve interpretation
- Traceable simulation input preparation
- WCCA and feasibility input control
- Review-gated model handoff

## Risks And Mitigations

- Risk: Extracted curves may be mistaken for validated device limits. Mitigation: every output is synthetic, reference-only, and review-required.
- Risk: Calibration or point-pick error could distort the model. Mitigation: preserve source pixels, calibration metadata, overlay images, and review status.
- Risk: Downstream tools could consume unreviewed data. Mitigation: Project 5 integration remains reviewed-only and adapter-based.

## Next Improvements

- Add reviewed Project 6 CSV/JSON schemas for downstream adapter work.
- Add browser-verified Streamlit screenshots after optional runtime dependencies are installed.
- Add public-datasheet validation only after Jose approves a public/sanitized source.

## Safe To Publish Status

Needs review. The deterministic evidence is synthetic and ready for local interview discussion as decision-support only. The interactive Streamlit path, downstream adapters, and any engineering use still require verification and qualified engineer review.
