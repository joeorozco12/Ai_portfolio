# Engineering Workflow Portfolio Console

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This static local console implements the unified UX shell for Projects 1, 2, 4, and 5:

- Requirements-to-Verification Tool
- AI-Assisted WCCA Prep Tool
- Design Review Readiness Assistant
- Lighting Feasibility Mini-Simulator

The console is a portfolio/workflow review surface. It does not run engineering calculations, approve outputs, or replace the deterministic project scripts. It reads normalized data generated from each project artifact package.

The QR-ready public entry route is:

```text
tools/index.html
```

When `ux-console/` is published as the static site root, interviewers can open `/tools` to use the browser demos and evidence dashboards.

## Run

Regenerate the console data from the repo root:

```bash
python3 tools/generate_ux_console_data.py
```

Then open:

```text
ux-console/index.html
```

The app is dependency-free and can be opened directly in a browser. The data bundle is written as JavaScript instead of fetched JSON so local `file://` usage works without a development server.

## UX Boundary

- Generated outputs and reviewer decisions stay separate.
- Browser demos run locally in the visitor's browser.
- Every project remains `Needs review` until qualified review evidence exists.
- `Export ready` is package-readiness only, not engineering approval.
- `Safe to publish` requires synthetic-data, human-review, restricted-detail, and AI-approval wording checks.

## Validation

Run the console tests from the repo root:

```bash
python3 -m unittest discover -s tests
```

The tests verify that the normalized console data preserves required synthetic labels, human-review language, hash routes, indexed artifacts, surfaced review items, and `Needs review` publication state.

Validate reviewer dispositions:

```bash
python3 tools/validate_ux_console_review.py
```

The default review log is [review/review_log.csv](review/review_log.csv). It is a template until Jose records review decisions.

## Publish

Use the repository GitHub Pages workflow:

```text
.github/workflows/deploy-ux-console.yml
```

The workflow uploads only `ux-console/` as the static Pages artifact. The QR code should point to the hosted `/tools` route after the GitHub Pages URL and phone verification pass.

## Screenshot Evidence

Console screenshots are stored in [screenshots](screenshots). They are portfolio evidence only and remain `Needs review` until publication review is complete.

## Publication Classification

Needs review.
