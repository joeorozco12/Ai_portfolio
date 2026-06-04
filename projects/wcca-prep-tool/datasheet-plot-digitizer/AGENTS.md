# AGENTS.md - LED Datasheet Curve Studio

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Mission

This folder contains LED Datasheet Curve Studio, a local Streamlit engineering tool that converts public or synthetic LED datasheet plots into calibrated, reviewable curve data packages for WCCA, MATLAB/Python simulation, thermal derating, luminous-flux prediction, and design-review preparation.

## Scope

Work only inside `projects/wcca-prep-tool/datasheet-plot-digitizer` unless the user explicitly gives a broader scope.

Allowed project areas:

- `led_digitizer/` for deterministic project model, calibration, extraction, curve fitting, validation, export, and report logic.
- `app.py` for the Streamlit workflow shell only.
- `data/synthetic/` and `data/demo_projects/` for synthetic demo inputs.
- `exports/`, `outputs/`, and `captures/` for generated demo artifacts.
- `tests/` for focused unit tests.
- Local documentation files in this folder.

Do not edit the parent WCCA project, other portfolio projects, shared homepage files, or root portfolio materials unless the task explicitly says to do so.

## Safety Rules

Use only synthetic or public LED examples.

Never include proprietary automotive, customer, supplier, OEM, program, schematic, BOM, harness, cost, internal test, internal requirement, ticket, part-number, file-path, repository, or internal-document details.

If source material appears proprietary, do not quote it, reproduce it, or summarize specific details. Extract only the workflow pattern and create a synthetic substitute.

Never imply that AI approves engineering decisions. The tool prepares draft review artifacts only.

Every public or engineering artifact generated in this folder must include:

```text
[SYNTHETIC — FOR DEMONSTRATION ONLY]
```

Every engineering artifact generated in this folder must include:

```text
Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.
```

Use one publication classification in each artifact: `Safe to publish`, `Needs review`, `Internal only`, or `Do not publish`.

## Engineering Boundary

- Engineer review is required before exported data is used in WCCA, simulation, thermal derating, luminous-flux prediction, design-review preparation, or any design decision.
- Digitized curves are reference data extracted from plots. They are not guaranteed manufacturer limits.
- Preserve source pixels, calibration metadata, source page or section, extraction method, fit model, assumptions, and review status in exports.
- Treat assisted extraction as draft until manual overlay review and qualified engineering review are complete.
- Keep downstream adapters reviewed-only. Raw datasheet extraction must not flow directly into WCCA or feasibility tools without review metadata.

## Architecture Rules

- Keep deterministic engineering logic separate from Streamlit UI code.
- Put project models, serialization, calibration, extraction, curve fitting, validation, exports, reports, and demo-data builders in `led_digitizer/`.
- Keep `app.py` as a UI shell that calls deterministic core functions.
- Prefer standard-library logic for the deterministic demo path when practical.
- Optional dependencies such as Streamlit, PyMuPDF, OpenCV, NumPy, Pandas, SciPy, and Matplotlib may support the UI or assisted extraction path, but tests for the deterministic core should not require them unless the task explicitly says so.
- Add tests with each task that changes behavior.
- Avoid unrelated cleanup or renaming.

## Task Workflow

Before implementation, read:

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `CODEX_TASKS.md`
- Relevant source and tests for the assigned task

Implement one numbered task at a time from `CODEX_TASKS.md`. Do not start the next task unless the user explicitly asks for it.

Use validation commands listed in the task. At minimum, finish documentation-only work with:

```bash
git diff --check -- projects/wcca-prep-tool/datasheet-plot-digitizer
```

When complete, report:

- Changed files
- What was added or implemented
- Validation results
- Known limitations
- Next recommended task

## Done Means

A task is done only when scoped files are updated, required synthetic-data and human-review labels are present, generated or changed behavior has focused validation, publication risk is explicit, and no proprietary content has been introduced.

## Publication Classification

Needs review

## Safe To Publish Status

Needs review. These instructions are synthetic and public-safe, but the project still requires qualified review before portfolio publication.
