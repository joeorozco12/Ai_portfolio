# LED Datasheet Curve Studio

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

LED datasheet plots often contain voltage, current, temperature, luminous-flux, and chromaticity behavior that engineers need in structured form. Manual point picking is slow, inconsistent, and hard to trace into WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, and design-review artifacts.

## Engineering Context

LED Datasheet Curve Studio is a local Streamlit engineering tool under the AI-Assisted WCCA Prep Tool. It converts public or synthetic LED datasheet-style plot images into calibrated, reviewable curve data packages for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, and design-review preparation.

The included sample uses only synthetic datasheet-style data and a synthetic LED identifier. Do not add proprietary datasheets, customer programs, supplier records, internal requirements, schematics, BOM data, harness data, cost data, validation results, internal file paths, ticket numbers, or controlled source details.

## Workflow

1. Create or load a Curve Studio project.
2. Upload a public or synthetic PDF/image source.
3. Render or preview the target page.
4. Select the plot region.
5. Calibrate x and y axes from known reference points.
6. Pick curve points manually for the MVP.
7. Build a shape-preserving interpolation model.
8. Export CSV, JSON, Python, MATLAB, overlay, and Markdown review artifacts.
9. Require engineer review before downstream WCCA, simulation, derating, feasibility, or design-review use.

## Inputs

- Public or synthetic datasheet PDF/image
- Selected plot region
- X-axis and y-axis calibration points
- Axis units and scale type
- Manual curve-point picks
- Curve metadata and review status
- Future `.ledcurve.json` project files

## Outputs

Generated sample outputs are written under `outputs/`:

- `digitized_curve_points.csv`
- `curve_metadata.json`
- `overlay_forward_voltage_vs_current.png`
- `python/lookup_forward_voltage_vs_forward_current.py`
- `matlab/lookup_forward_voltage_vs_forward_current.m`
- `extraction_report.md`

Future formal export packages should also support reviewed `.ledcurve.json` project files and packaged demo exports under `exports/`.

## Screenshots Or Screenshot Placeholders

- `outputs/overlay_forward_voltage_vs_current.png`
- `captures/streamlit_workflow_mock.md`

## Sanitized Sample Data

The sample data is stored in `data/synthetic_manual_points.csv`. It uses `SYN-LED-170`, `Synthetic LED Supplier`, and `synthetic_page_20` as demonstration labels. These are synthetic placeholders, not real device or supplier records.

## Human Review Controls

- Manual axis calibration is required before export.
- Manual point picks remain draft until reviewed.
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

Run tests:

```bash
python3 -m unittest discover -s tests
```

Optional Streamlit runtime:

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

## Current Dependency Boundary

The deterministic core uses only the Python standard library. Streamlit, PyMuPDF, OpenCV, NumPy, Pandas, SciPy, and Matplotlib are declared in `requirements.txt` for the interactive app path, but they are not required for the tested synthetic export demo.

## Project Control Files

- `AGENTS.md` defines local safety, architecture, and task-boundary instructions.
- `PROJECT_BRIEF.md` defines the public-safe engineering framing.
- `CODEX_TASKS.md` sequences future implementation tasks so each Codex thread has one scoped goal.

## Next Improvements

- Add project model and `.ledcurve.json` save/load.
- Add reusable synthetic demo projects.
- Harden calibration, curve-fit validation, and report outputs.
- Build a clearer Streamlit workflow UI.
- Add optional assisted extraction after deterministic review controls are accepted.
- Add reviewed adapters that feed WCCA and lighting-feasibility inputs only after signoff.

## Proof Gaps

- The sample output is synthetic and does not validate extraction quality on a real public datasheet.
- Project save/load is not implemented yet.
- Runtime dependencies are not installed in this checkout yet, so the Streamlit UI has not been browser-verified.
- Crop and click behavior needs a Streamlit canvas/image-coordinate component before it becomes a full interactive digitizer.
- A qualified reviewer has not signed off on the workflow, fit model, or public screenshots.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. The code and sample data are synthetic and sanitized, but the app workflow, screenshots, and engineering claims require qualified review before publication.
