# LED Datasheet Curve Studio

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

LED datasheet plots often contain voltage, current, temperature, luminous-flux, and chromaticity behavior that engineers need in structured form. Manual point picking is slow, inconsistent, and hard to trace into WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, and design-review artifacts.

## Engineering Context

LED Datasheet Curve Studio is a supporting data-preparation tool under the AI-Assisted WCCA Prep Tool. It converts public or synthetic LED datasheet-style plot images into calibrated, reviewable curve data packages for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, feasibility screening, and design-review preparation.

This project is not positioned as a standalone AI demo. It is a deterministic, review-controlled workflow component for turning datasheet-style curve inputs into traceable engineering artifacts.

The included sample uses only synthetic datasheet-style data and a synthetic LED identifier. Do not add proprietary datasheets, customer programs, supplier records, internal requirements, schematics, BOM data, harness data, cost data, validation results, internal file paths, ticket numbers, or controlled source details.

## Workflow

1. Create or load a `.ledcurve.json` Curve Studio project in the deterministic core.
2. Use synthetic seed projects or import a public/synthetic PDF/image source.
3. Render an optional public/synthetic PDF page or preview a PNG/JPEG image.
4. Record source, crop, axis, curve, assumption, and review metadata.
5. Calibrate x and y axes from known reference points.
6. Pick or enter curve points manually, with optional draft assisted candidates when enabled.
7. Build a shape-preserving interpolation model.
8. Review the overlay before CSV, JSON, Python, MATLAB, overlay, and Markdown artifacts are used downstream.
9. Require engineer review before downstream WCCA, simulation, derating, feasibility, or design-review use.

## Inputs

- Public or synthetic datasheet PDF/image
- Source category marked as `public` or `synthetic`
- Selected plot region
- X-axis and y-axis calibration points
- Axis units and scale type
- Manual curve-point picks
- Optional draft assisted candidate pixels from a public/synthetic source
- Curve metadata and review status
- `.ledcurve.json` project files
- Reusable synthetic demo point tables

## Outputs

Generated sample outputs are written under `outputs/`:

- `.ledcurve.json` project files saved or loaded through `led_digitizer.project_io`
- `digitized_curve_points.csv`
- `curve_metadata.json`
- `overlay_forward_voltage_vs_current.png`
- `python/lookup_forward_voltage_vs_forward_current.py`
- `matlab/lookup_forward_voltage_vs_forward_current.m`
- `extraction_report.md`

Reusable Task 2 demo assets are written under:

- `data/synthetic/` for synthetic point tables
- `data/demo_projects/` for loadable `.ledcurve.json` demo projects

`run_demo.py` also regenerates a structured review package under `exports/demo_export_package/`, including point data, metadata JSON, source/calibration metadata, lookup files, overlay image, and a Markdown report.

## Screenshots Or Screenshot Placeholders

- `outputs/overlay_forward_voltage_vs_current.png`
- `captures/streamlit_workflow_mock.md`

The current capture is a screenshot placeholder. The Streamlit shell exists, but runtime dependencies have not been installed or browser-verified in this checkout.

## Sanitized Sample Data

The sample data is stored in `data/synthetic_manual_points.csv`. It uses `SYN-LED-170`, `Synthetic LED Supplier`, and `synthetic_page_20` as demonstration labels. These are synthetic placeholders, not real device or supplier records.

Reusable synthetic demo projects are stored in `data/demo_projects/` and cover:

- Forward voltage vs forward current
- Junction temperature vs relative luminous flux
- Forward current vs relative luminous flux
- Thermal derating style curve

Each demo project includes source metadata, assumptions, pending engineering-review status, the synthetic-data label, and the human-review note. Matching point tables are stored in `data/synthetic/`.

## Human Review Controls

- Manual axis calibration is required before export.
- Manual point picks remain draft until reviewed.
- Assisted extraction is optional, draft-only, and never replaces manual calibration or overlay review.
- Assisted candidate rows preserve source pixels, method, confidence, notes, and review status.
- Overlay verification is required before downstream use.
- CSV rows include source pixels, source page, method, fit model, and review status.
- Export is blocked in the Streamlit shell until the engineer-review checkbox is selected.
- Digitized plot data is reference-only and must not be treated as guaranteed device limits.
- The tool does not approve LED design values.
- Exported data requires qualified engineer review before WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, feasibility screening, or design-review use.

## Codex Contribution

Codex scaffolded the local Streamlit shell, deterministic calibration math, dependency-free PCHIP curve-fit builder, export modules, synthetic sample data, overlay PNG generator, Markdown report generator, unit tests, and local task-control documentation.

## Jose Contribution

Jose defines the automotive LED engineering use case, WCCA/feasibility workflow placement, meaningful curve types, required export formats, review controls, publication boundary, and final engineering judgment.

## AI Fundamentals Demonstrated

- Structured extraction workflow design
- Deterministic data transformation
- Interpolation/model generation
- Metadata-rich artifact generation
- Test generation for engineering math
- Human-in-the-loop review gating

## Engineering Skills Demonstrated

- LED datasheet plot interpretation
- WCCA data preparation
- Forward-voltage/current lookup generation
- Traceable simulation input preparation
- Review-control design for engineering tools

## Risks And Mitigations

- Risk: Digitized curves could be mistaken for guaranteed manufacturer limits. Mitigation: every artifact marks plot data as reference-only and requires qualified engineering review.
- Risk: Pixel calibration errors could distort the exported curve. Mitigation: source pixels, calibration values, overlay image, and reviewer status are retained.
- Risk: Curve fitting could hide raw data quality issues. Mitigation: raw points are exported with the fitted lookup functions.
- Risk: Public output could expose controlled data. Mitigation: the included sample is synthetic, and the workflow is limited to public or sanitized sources.

## Run

Generate the current synthetic artifact package:

```bash
python3 run_demo.py
```

Generate reusable Task 2 synthetic demo projects and point tables:

```bash
python3 -m led_digitizer.demo_data
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

Run the project save/load tests:

```bash
python3 -m unittest tests/test_project_io.py
```

Run the synthetic demo-data tests:

```bash
python3 -m unittest tests/test_demo_data.py
```

Run the Task 7 extraction tests:

```bash
python3 -m unittest tests/test_extraction_manual.py tests/test_extraction_assisted.py
```

Optional Streamlit runtime:

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

## Current Dependency Boundary

The deterministic core and tested synthetic artifact path use only the Python standard library. PNG/JPEG metadata inspection, manual extraction conversion, draft assisted candidate grouping, and review-gate checks are tested without proprietary inputs or optional runtime packages. PyMuPDF is optional for rendering public/synthetic PDF pages. Streamlit, PyMuPDF, OpenCV, NumPy, Pandas, SciPy, and Matplotlib are declared in `requirements.txt` for the interactive app path, but they are not required for `python3 run_demo.py` or the current unit tests.

## Project Control Files

- `AGENTS.md` defines local safety, architecture, and task-boundary instructions.
- `PROJECT_BRIEF.md` defines the public-safe engineering framing.
- `CODEX_TASKS.md` sequences future implementation tasks so each Codex thread has one scoped goal.
- `docs/ux_plan.md` records a Task 6 UI plan. It is a planning artifact, not browser-verified implementation evidence.

## Completed Work

- Deterministic project model and `.ledcurve.json` save/load path are implemented and tested.
- Reusable synthetic demo projects and point tables are generated under `data/demo_projects/` and `data/synthetic/`.
- Axis calibration supports linear and log scales, reversed image axes, source-pixel preservation, and report-ready sanity metadata.
- Curve-fit validation helpers report residuals, monotonicity checks, review-status counts, and out-of-range behavior for review.
- The current curve-fit/export demo generates CSV, JSON, Python lookup, MATLAB lookup, overlay PNG, Markdown report artifacts, and a structured `exports/demo_export_package/` package from synthetic points.
- Optional draft assisted extraction helpers preserve source pixels, method, confidence, notes, and review status.
- Unit tests cover project I/O, synthetic demo data, calibration, curve fitting, validation, export safety labels, manual extraction, and draft assisted extraction boundaries.
- Human-review notes, synthetic-data labels, publication classifications, and downstream-use warnings are present in the checked-in demo artifacts.

## Next Improvements

- Build a clearer Streamlit project workflow UI around the deterministic core.
- Add browser-verified screenshots after optional runtime dependencies are installed.
- Integrate the full curve-fit validation report into the Streamlit review workflow and generated Markdown package.
- Wire the draft assisted extraction preview into the Streamlit UI after manual overlay controls are browser-verified.
- Add reviewed adapters that feed WCCA and lighting-feasibility inputs only after signoff.

## Proof Gaps

- The sample output is synthetic and does not validate extraction quality on a real public datasheet.
- Reusable demo projects are synthetic seed data only; they are not reviewed device limits.
- Assisted extraction currently groups provided candidate pixels only; it is not a reviewed image-recognition workflow and has not been validated on real public datasheets.
- Runtime dependencies are not installed in this checkout yet, so the Streamlit UI has not been browser-verified.
- Project save/load is implemented in the deterministic core, but the Streamlit shell does not expose it yet.
- Full validation output exists in the deterministic core but is not fully wired into the UI and generated export report yet.
- Crop and click behavior needs a Streamlit canvas/image-coordinate component before it becomes a full interactive digitizer.
- A qualified reviewer has not signed off on the workflow, fit model, or public screenshots.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The code and sample data are synthetic and sanitized, but the app workflow, screenshots, and engineering claims require qualified review before publication.
