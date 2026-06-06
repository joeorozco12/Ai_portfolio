# Task 6 UX Implementation Plan - Streamlit Workflow UI

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

The current Streamlit shell exposes a useful demo path, but Task 6 should make the workflow clearer and more reviewable without moving calibration, fitting, save/load, or export logic into `app.py`.

## Engineering Context

LED Datasheet Curve Studio is a local data-preparation tool for public or synthetic LED datasheet-style plots. The UI must support traceable curve extraction for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, feasibility screening, and design-review preparation, while keeping downstream use blocked until qualified engineering review is acknowledged.

## Workflow

Use a left-to-right staged workflow with persistent Streamlit session state:

1. Project setup
2. Source import
3. Crop
4. Axis calibration
5. Manual point entry or picking
6. Fit validation
7. Review checklist
8. Export package

Each stage should show a compact status indicator: `Not started`, `In progress`, `Valid`, `Needs correction`, or `Blocked`.

## Inputs

- Project metadata: project name, synthetic/public source category, LED identifier, intended use, publication classification, assumptions, and reviewer notes.
- Source metadata: PDF/image upload, page index, source section, source URI or local label, and source category.
- Crop metadata: plot-region pixel bounds.
- Axis calibration: x/y pixel anchors, engineering values, units, labels, and linear/log scale.
- Curve points: manually entered rows first, then optional click/pick support when a browser coordinate component is added.
- Review checklist: source safety, calibration visibility, raw point review, fit review, overlay review, and downstream-use acknowledgment.

## Outputs

- Updated `.ledcurve.json` project payload.
- Reviewable curve points table in engineering units and source pixels.
- Fit preview and basic validation status.
- Export package containing CSV, metadata JSON, Python lookup, MATLAB lookup, overlay PNG, and Markdown report.
- Screenshot placeholders or captures under `captures/`.

## UI States

### Project Setup

- Empty: show synthetic sample defaults and a `New synthetic project` action.
- Loaded: show project summary, schema version, review status, and source category.
- Dirty: show unsaved changes after metadata, calibration, points, or review fields change.
- Saved: show `.ledcurve.json` path or download-ready project file.

Core calls:

- `ProjectMetadata(...)`
- `SourceMetadata(...)`
- `LedCurveProject(...)`
- `save_project(project, path)`
- `load_project(path)`

### Source Import

- No source: upload and source-category controls are enabled; downstream crop/calibration stages remain blocked.
- Image loaded: show preview and image dimensions.
- PDF loaded: call the existing PDF preview path; if `fitz` is missing, show install guidance and keep crop blocked.
- Unsupported file: reject file and keep downstream stages blocked.
- Source risk flagged: if source category is not `synthetic` or `public`, block export and show publication-safety warning.

Core calls:

- UI-local preview helper only for rendering.
- `SourceMetadata(...)` for normalized source fields.

### Crop

- No preview: crop controls disabled.
- Numeric crop mode: allow left/top/width/height entry with bounds checks.
- Future interactive crop mode: use browser coordinate/canvas component, but store only normalized crop metadata in the project model.
- Invalid crop: block calibration if width/height are less than 1 or crop exceeds known image bounds.

Core calls:

- `SourceMetadata(..., plot_region_px={...})`
- `LedCurveProject.to_dict()` for persisted crop metadata.

### Axis Calibration

- Missing crop/source: disabled.
- Editable: numeric anchor entry remains the deterministic fallback.
- Future pick mode: click anchors on preview, then populate the same numeric fields.
- Valid: construct `AxisCalibration` for x and y axes.
- Invalid: catch calibration exceptions and block point conversion, fit, and export.

Core calls:

- `AxisCalibration(...)`
- `CurveCalibration(x_axis=..., y_axis=...)`
- `axis_calibration_to_dict(calibration)`
- `curve_calibration_from_dict(payload)`

### Manual Point Entry/Picking

- No valid calibration: table and picking controls disabled.
- Manual table: keep `st.data_editor` as the MVP path for source pixel x/y, point id, review status, and notes.
- Sample seed: allow loading `load_sample_points(SAMPLE_POINTS_PATH)` only for synthetic demo mode.
- Future pick mode: image click component appends pixel points to the same table.
- Invalid row: show row-level warning and omit conversion until corrected.

Core calls:

- `CurveCalibration.pixel_to_engineering(...)`
- `EngineeringPoint(...)`
- `ExtractedPoint.from_engineering_point(point)`
- `CurveData.add_point(...)`
- `load_sample_points(SAMPLE_POINTS_PATH)`

### Fit Validation

- Fewer than two valid points: disabled and export blocked.
- Duplicate x-values: show deterministic error from the curve-fit core.
- Valid points: build shape-preserving interpolation and show sorted raw points, interpolation range, and endpoint clamp behavior.
- Pending validation core: if a future `led_digitizer.validation` module exists, call it here instead of adding validation math to `app.py`.

Core calls:

- `sort_unique_points(points)`
- `build_pchip_segments(points)`
- `evaluate_pchip(segments, x_value)`
- `linear_interpolate(points, x_value)` for a simple comparison preview if useful.

### Review Checklist

- Disabled until source, crop, calibration, points, and fit stages are valid.
- Required checks:
  - Source is public or synthetic.
  - Synthetic-data label is visible.
  - Human-review note is visible.
  - Axis calibration was reviewed.
  - Raw points were reviewed against source pixels.
  - Overlay or preview was reviewed.
  - Fit behavior and out-of-range behavior were reviewed.
  - Data is reference-only and not a guaranteed manufacturer limit.
- Reviewer note should be required before changing review status beyond `draft_extraction`.

Core calls:

- `CurveData(...)` with `review_status`, `reviewer_notes`, `engineering_notes`, and `assumptions`.
- `LedCurveProject(...)` with project-level `review_status` and assumptions.

### Export Package

- Export disabled until every gate is true:
  - project metadata valid
  - source category is `synthetic` or `public`
  - crop valid
  - axis calibration valid
  - at least two converted points
  - fit validation has no blocking error
  - required review checklist complete
  - engineer-review acknowledgment checked
- Export should generate files from deterministic helpers only.
- Download buttons should appear only after successful package generation.
- If export fails, show the deterministic exception message and keep prior project state intact.

Core calls:

- `safe_name(metadata["curve_name"])`
- `write_points_csv(...)`
- `write_metadata_json(...)`
- `write_overlay_png(...)`
- `write_python_lookup(...)`
- `write_matlab_lookup(...)`
- `write_markdown_report(...)`

## Error States

- Missing optional dependency: show install guidance; do not crash.
- Invalid `.ledcurve.json`: show schema/path error from `load_project(...)`.
- Unsupported project-file extension: show `PROJECT_FILE_EXTENSION` rule.
- Invalid calibration: show the deterministic `AxisCalibration` error.
- Invalid point row: show row-level warning and block fit/export.
- Duplicate x-value or too few points: show deterministic curve-fit error.
- Unsafe source category or publication classification: block export.
- Review checklist incomplete: keep export button disabled with the missing gates listed.
- Export helper failure: show file-specific failure and do not mark package complete.

## Disabled And Export Gating Behavior

Downstream sections should remain visible but disabled, with a short reason. This keeps the workflow teachable without implying the tool is ready for engineering use before source, calibration, points, fit, and review gates are satisfied.

Recommended gate object in `app.py`:

- `project_ready`
- `source_ready`
- `crop_ready`
- `calibration_ready`
- `points_ready`
- `fit_ready`
- `review_ready`
- `export_ready`

`export_ready` should be the only condition that enables `Generate export package`.

## Screenshots Or Screenshot Placeholders

- Keep `captures/streamlit_workflow_mock.md` until the UI is implemented and browser-verified.
- Add future captures for project setup, source import/crop, calibration, fit validation, review checklist, and export package.

## Sanitized Sample Data

Use the existing synthetic sample path and labels only: `data/synthetic_manual_points.csv`, `SYN-LED-170`, `Synthetic LED Supplier`, and `synthetic_page_20`.

## Human Review Controls

The UI should keep the human-review warning visible on every stage and should never describe export as approval. Export means "ready for review package download", not validated engineering signoff.

## Codex Contribution

Codex should implement the Streamlit workflow shell, stage gating, state handling, error messaging, and calls into deterministic core functions.

## Jose Contribution

Jose owns final workflow acceptance, review-control wording, engineering source eligibility, and any decision to use exported curve data downstream.

## AI Fundamentals Demonstrated

- Human-in-the-loop workflow gating
- Structured project-state modeling
- Deterministic transformation orchestration
- Traceable export packaging

## Engineering Skills Demonstrated

- LED datasheet plot interpretation workflow
- Calibration and source-pixel traceability
- WCCA and simulation input preparation boundaries
- Engineering review-control design

## Risks And Mitigations

- Risk: UI flow could imply engineering approval. Mitigation: keep review language visible and gate export on acknowledgment only.
- Risk: Users could bypass source safety. Mitigation: require `synthetic` or `public` source category before export.
- Risk: UI code could duplicate math. Mitigation: `app.py` should call deterministic core modules and only manage presentation/state.
- Risk: Fit preview could hide bad raw points. Mitigation: always show raw points and export source pixels.

## Next Improvements

- Implement Task 6 UI stages in `app.py` using the gate object above.
- Add capture placeholders or browser-verified captures after the UI is running.
- Add interactive image click/pick support only after the numeric fallback path is stable.
- Defer assisted extraction to Task 7.

## Proof Gaps

- This is a UX implementation plan only; no Task 6 code changes were made.
- Streamlit runtime dependencies are not verified by this plan.
- Interactive crop and point-picking require a browser coordinate component or custom canvas package.
- Fit validation is limited to current deterministic curve-fit helpers unless a validation module is added.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. This plan uses synthetic/public-safe framing, but the implemented UI and any screenshots require qualified engineering review before publication.
