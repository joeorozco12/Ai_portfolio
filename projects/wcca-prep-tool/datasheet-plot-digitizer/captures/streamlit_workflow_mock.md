# LED Datasheet Curve Studio - Streamlit Workflow Placeholder

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Capture Type

Screenshot placeholder for the current LED Datasheet Curve Studio Streamlit workflow shell. This is not browser-verified UI evidence.

## Problem

The interactive digitizer still needs a browser-verified screenshot-ready view that demonstrates import, calibration, point-entry, review, and export controls without exposing controlled source material.

## Engineering Context

This placeholder belongs to the AI-Assisted WCCA Prep Tool as a supporting LED data-prep view. It should show only public or synthetic datasheet-style inputs and should not imply that digitized data is approved for engineering use.

## Workflow

1. After runtime dependencies are installed, open the local Streamlit shell for browser verification.
2. Use the `Project Setup` tab to enter synthetic project metadata, intended use, and review status.
3. Use the `Source Import` tab to enter synthetic/public source metadata and preview a PDF or image source.
4. Use the `Crop & Calibration` tab to set numeric crop-region coordinates and x/y axis references.
5. Use the `Point Entry` tab to review or edit synthetic seed source-pixel rows and converted engineering values.
6. Use the `Fit Validation` tab to review PCHIP interpolation health for the current point table.
7. Use the `Review Checklist` tab to confirm source safety, crop/calibration review, point review, fit review, and reference-only export marking.
8. Use the `Export Review` tab to confirm engineer-review acknowledgment before export controls become available.
9. Export CSV, JSON, Python, MATLAB, overlay, and report artifacts for local review.

## Inputs

- Synthetic datasheet-style image or public datasheet image
- Crop-region pixel coordinates
- Axis calibration pixel/value pairs
- Manual curve-point pixels
- Curve metadata and review status

## Outputs

- Screenshot placeholder
- Overlay preview reference
- Export-button state reference
- Human-review gate reference

## Documented Shell State Pending Browser Verification

- The intended shell tabs are `Project Setup`, `Source Import`, `Crop & Calibration`, `Point Entry`, `Fit Validation`, `Review Checklist`, and `Export Review`.
- The synthetic-data label and human-review warning are visible near the page header.
- Metadata fields use synthetic defaults such as `SYN-LED-170`, `Synthetic LED Supplier`, and `synthetic_page_20`.
- Source import is labeled for synthetic/public PDF or image preview only.
- Numeric crop fields are visible for left, top, width, and height.
- Axis calibration fields show labels, units, scale type, and two pixel/value references per axis.
- Manual point table shows source-pixel coordinates and converted engineering values.
- Assisted extraction remains visibly deferred to a later task and shows install guidance if OpenCV is not installed.
- Fit validation shows point count, PCHIP segment count, x-domain, and raw-point residual status.
- Review checklist items are visible before export review.
- Engineer-review acknowledgment is visible before export.
- Export generation is disabled until points exist, calibration is valid, fit validation passes, checklist items are complete, and the acknowledgment is checked.

## Screenshots Or Screenshot Placeholders

This file is the screenshot placeholder. A real screenshot should replace or supplement it only after runtime dependencies are installed and the browser layout is reviewed.

The current overlay artifact is `outputs/overlay_forward_voltage_vs_current.png`.

## Sanitized Sample Data

The visible sample should use `SYN-LED-170`, `synthetic_datasheet_style_plot`, and `synthetic_page_20`. No real manufacturer part number, customer program, internal file path, internal requirement, schematic, BOM, harness, cost, validation result, or controlled source detail should appear.

## Human Review Controls

- The human-review note must remain visible in the screenshot.
- Export should be gated by review-checklist completion and an engineer-review acknowledgment checkbox.
- The screenshot must not show real proprietary or controlled source material.
- Fit validation must be framed as interpolation health only, not engineering approval.
- The tool must be framed as decision support only.
- Any downstream WCCA or lighting-feasibility use must remain blocked until reviewed status is confirmed outside the demo shell.

## Codex Contribution

Codex created the Streamlit workflow shell, refreshed the Task 6 workflow structure, updated the screenshot placeholder, and implemented export-gate logic intended for later browser verification.

## Jose Contribution

Jose defines the engineering workflow placement, acceptable screenshot framing, public/synthetic source boundary, and final review judgment.

## AI Fundamentals Demonstrated

- UI scaffolding for structured extraction
- Human-review gating
- Metadata-driven workflow control
- Testable deterministic backend integration

## Engineering Skills Demonstrated

- LED datasheet plot preparation
- WCCA input governance
- Traceability controls
- Review-ready engineering artifact packaging

## Risks And Mitigations

- Risk: A screenshot could imply the extraction is approved. Mitigation: keep the human-review note and disabled export state visible unless reviewed.
- Risk: A real source image could expose controlled data. Mitigation: use only synthetic or public-safe source imagery.
- Risk: Pixel picks could be misread as authoritative. Mitigation: show draft review status and require overlay review.

## Completed Work

- Placeholder documents the current seven-step tabbed Streamlit shell target pending browser verification.
- Export review gate is documented.
- Fit validation and review checklist states are documented.
- Synthetic labels and human-review controls are specified for the eventual screenshot.
- Overlay artifact path is current.

## Next Improvements

- Capture a real Streamlit screenshot after dependencies are installed.
- Add a click-based image coordinate component for the crop and curve-pick workflow.
- Add an assisted extraction preview only after manual controls are reviewed.
- Add project-file save/load controls to the Streamlit shell after deterministic project I/O is accepted.

## Proof Gaps

- Real browser screenshot still needs to be captured after Streamlit runtime dependencies are installed and the UI layout is reviewed.
- The current shell does not expose full project save/load workflow controls.
- Interactive image click/crop behavior is not implemented.
- Assisted extraction remains optional/planned and is not reviewed implementation evidence.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. This is a screenshot placeholder only; it is safe from proprietary content but still needs visual QA and engineering framing review before publication.
