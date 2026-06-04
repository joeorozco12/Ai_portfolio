# LED Datasheet Curve Studio - Codex Tasks

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Operating Rules

- Work only inside `projects/wcca-prep-tool/datasheet-plot-digitizer` unless the user explicitly expands scope.
- Read `AGENTS.md`, `PROJECT_BRIEF.md`, and this file before each task.
- Implement one task at a time.
- Do not start the next task without explicit user direction.
- Keep deterministic engineering logic in `led_digitizer/` and Streamlit workflow code in `app.py`.
- Use only synthetic or public LED examples.
- Do not imply AI approves engineering decisions.
- Add or update tests for behavior changes.
- End each task with changed files, implementation summary, validation results, known limitations, and the next recommended task.

## Current Baseline

The rough-draft digitizer demo already includes:

- Streamlit shell in `app.py`
- Synthetic manual points in `data/synthetic_manual_points.csv`
- Deterministic calibration and PCHIP curve-fit helpers
- CSV, JSON, Python, MATLAB, overlay PNG, and Markdown report exports
- Basic tests for calibration, curve fitting, and exports

This task list formalizes the project as LED Datasheet Curve Studio and sequences future work.

## Task 1 - Project Model And Save/Load

Goal: Add a project file model that can persist metadata, sources, calibration, curves, points, assumptions, and review status.

Create or update:

- `led_digitizer/models.py`
- `led_digitizer/project_io.py`
- `tests/test_project_io.py`

Acceptance criteria:

- Project metadata can be created.
- Source metadata can be stored.
- Axis calibration can be stored.
- Curves can be added.
- Extracted points can be stored.
- Review status can be stored.
- Project can save to `.ledcurve.json`.
- Project can load from `.ledcurve.json`.
- Unit tests pass.

Validation:

```bash
python3 -m unittest tests/test_project_io.py
python3 -m py_compile led_digitizer/*.py
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 2 - Synthetic Demo Data

Goal: Create reusable synthetic demo projects that show common LED datasheet curve workflows without proprietary data.

Create or update:

- `led_digitizer/demo_data.py`
- `data/synthetic/`
- `data/demo_projects/`
- `tests/test_demo_data.py`
- `README.md` if demo instructions need alignment

Acceptance criteria:

- Synthetic forward-voltage/current demo exists.
- Synthetic relative luminous-flux/temperature demo exists.
- Synthetic thermal derating demo exists.
- Demo data includes source metadata, assumptions, and review status.
- Generated demo projects save as `.ledcurve.json`.
- No proprietary identifiers are introduced.

Validation:

```bash
python3 -m unittest tests/test_demo_data.py
python3 -m py_compile led_digitizer/*.py
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 3 - Calibration Engine

Goal: Expand axis and plot calibration into a reusable, tested core module.

Create or update:

- `led_digitizer/calibration.py`
- `tests/test_calibration.py`

Acceptance criteria:

- Linear x/y calibration is tested.
- Log x/y calibration is tested.
- Inverted image-axis behavior is tested.
- Invalid calibration inputs fail clearly.
- Calibration metadata can be serialized through the project model.
- Calibration residual or sanity-check outputs are available for reports.

Validation:

```bash
python3 -m unittest tests/test_calibration.py
python3 -m py_compile led_digitizer/*.py
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 4 - Curve Fitting And Validation Core

Goal: Build curve-fit validation logic that compares fitted outputs against raw reviewed points and reports fit quality.

Create or update:

- `led_digitizer/curve_fit.py`
- `led_digitizer/validation.py`
- `tests/test_curve_fit.py`
- `tests/test_validation.py`

Acceptance criteria:

- Shape-preserving interpolation remains available.
- Fit residuals are calculated.
- Monotonicity checks are available where applicable.
- Out-of-range lookup behavior is explicit.
- Validation output can be included in reports and exports.
- Tests cover normal and invalid inputs.

Validation:

```bash
python3 -m unittest tests/test_curve_fit.py tests/test_validation.py
python3 -m py_compile led_digitizer/*.py
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 5 - Export Package

Goal: Produce a structured export package for reviewable downstream use.

Create or update:

- `led_digitizer/exports.py`
- `led_digitizer/report.py`
- `exports/demo_export_package/`
- `tests/test_exports.py`
- `tests/test_report.py`

Acceptance criteria:

- Export package includes CSV, JSON, Python lookup, MATLAB lookup, overlay, and Markdown report.
- Export metadata includes source, calibration, assumptions, method, fit model, validation status, and review status.
- Export package states the synthetic label and human-review note.
- Downstream use warnings are visible.
- Tests cover package contents and safety labels.

Validation:

```bash
python3 -m unittest tests/test_exports.py tests/test_report.py
python3 -m py_compile led_digitizer/*.py
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 6 - Streamlit Workflow UI

Goal: Turn the Streamlit shell into a clearer project workflow without moving deterministic logic into UI code.

Create or update:

- `app.py`
- `captures/`
- `README.md` if run instructions change

Acceptance criteria:

- UI supports project setup, source import, calibration, point entry, fit validation, and export review.
- Export controls require engineer-review acknowledgment.
- UI remains local and public/synthetic-data only.
- Missing optional dependencies fail gracefully.
- Captures or capture placeholders are updated.

Validation:

```bash
python3 -m py_compile app.py led_digitizer/*.py
python3 -m unittest discover -s tests
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 7 - Assisted Extraction

Goal: Add optional assisted extraction while preserving manual review and deterministic validation boundaries.

Create or update:

- `led_digitizer/image_tools.py`
- `led_digitizer/pdf_import.py`
- `led_digitizer/extraction_manual.py`
- `led_digitizer/extraction_assisted.py`
- `tests/test_extraction_manual.py`
- `tests/test_extraction_assisted.py`
- `README.md` if workflow documentation changes

Acceptance criteria:

- Public/synthetic PDF or image import path is documented.
- Assisted extraction is optional and marked draft.
- Manual calibration and overlay review remain required.
- Assisted points preserve source pixels, method, confidence, and review status.
- Tests cover deterministic parts without requiring proprietary inputs.

Validation:

```bash
python3 -m unittest tests/test_extraction_manual.py tests/test_extraction_assisted.py
python3 -m py_compile led_digitizer/*.py
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Task 8 - Documentation And Portfolio Polish

Goal: Make the project portfolio-ready after implementation tasks are complete and validated.

Create or update:

- `README.md`
- `PROJECT_BRIEF.md`
- `CODEX_TASKS.md`
- `captures/`
- `outputs/` or `exports/` demo artifacts, if regenerated

Acceptance criteria:

- README matches implemented behavior.
- Screenshots or screenshot placeholders are current.
- Proof gaps separate completed work from planned work.
- Safe-to-publish status is explicit.
- Human-review controls remain visible.
- No proprietary content is present.

Validation:

```bash
python3 run_demo.py
python3 -m unittest discover -s tests
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. This task plan is synthetic and public-safe, but each generated implementation and public artifact requires qualified review before publication.
