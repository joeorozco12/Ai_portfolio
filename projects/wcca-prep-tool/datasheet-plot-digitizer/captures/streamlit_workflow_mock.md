# Streamlit Workflow Mock Capture

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Capture Type

Screenshot placeholder for the LED Datasheet Plot Digitizer Streamlit workflow.

## Problem

The interactive digitizer needs a screenshot-ready view that proves the workflow has import, calibration, point-picking, review, and export controls without exposing controlled source material.

## Engineering Context

This placeholder belongs to the AI-Assisted WCCA Prep Tool as a supporting LED data-prep view. It should show only public or synthetic datasheet-style inputs and should not imply that digitized data is approved for engineering use.

## Workflow

1. Import a public or synthetic datasheet page image.
2. Set a plot crop region.
3. Enter axis calibration references.
4. Review manually picked curve points.
5. Confirm engineer review before export.
6. Export reviewed CSV, JSON, Python, MATLAB, overlay, and report artifacts.

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

## Intended Screen State

- Uploaded public or synthetic datasheet plot image is visible.
- Axis calibration fields show two x-axis references and two y-axis references.
- Manual curve-point table shows source-pixel coordinates and converted engineering values.
- Engineer review checkbox is visible before export.
- Export buttons are disabled until review is confirmed.

## Screenshots Or Screenshot Placeholders

This file is the screenshot placeholder. A real screenshot should replace or supplement it only after runtime dependencies are installed and the browser layout is reviewed.

## Sanitized Sample Data

The visible sample should use `SYN-LED-170`, `synthetic_datasheet_style_plot`, and `synthetic_page_20`. No real manufacturer part number, customer program, internal file path, internal requirement, schematic, BOM, harness, cost, validation result, or controlled source detail should appear.

## Human Review Controls

- The human-review note must remain visible in the screenshot.
- Export should be gated by an engineer-review checkbox.
- The screenshot must not show real proprietary or controlled source material.
- The tool must be framed as decision support only.

## Codex Contribution

Codex created the Streamlit workflow shell, the screenshot placeholder, and the export-gate behavior intended for the UI capture.

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

## Next Improvements

- Capture a real Streamlit screenshot after dependencies are installed.
- Add a click-based image coordinate component for the crop and curve-pick workflow.
- Add an assisted extraction preview only after manual controls are reviewed.

## Proof Gap

Real browser screenshot still needs to be captured after Streamlit runtime dependencies are installed and the UI layout is reviewed.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. This is a screenshot placeholder only; it is safe from proprietary content but still needs visual QA and engineering framing review before publication.
