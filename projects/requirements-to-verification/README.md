# Requirements-to-Verification Prototype

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

Requirements-to-verification work often starts with mixed inputs: requirement rows, notes, proposed tests, assumptions, and review status fields. Manual cleanup can miss ambiguous language, weak verification hooks, hidden assumptions, and unclear pass/fail criteria.

## Engineering Context

This Project 1 prototype uses only synthetic automotive lighting examples. It prepares review artifacts for low beam, high beam, DRL, input-voltage behavior, diagnostics, boost-driver screening hooks, thermal review triggers, traceability, and human-review governance. It does not use restricted source material, nonpublic program data, internal identifiers, or real engineering documents.

## Workflow

1. Load [../../Synthetic Requirements Sample.csv](../../Synthetic%20Requirements%20Sample.csv).
2. Validate the required CSV schema.
3. Generate a deterministic trace matrix from the synthetic rows.
4. Detect weak language, missing limits, missing units, missing operating context, missing verification methods, unclear ownership, and unclear pass/fail criteria.
5. Generate linked assumptions for rows that need reviewer context.
6. Generate a design-review readiness checklist.
7. Export CSV, Markdown, and terminal-style mock capture files.

## Run

From the repo root:

```bash
python3 tools/requirements_to_verification.py --input "Synthetic Requirements Sample.csv" --output projects/requirements-to-verification/generated_outputs
```

The default capture folder is:

```text
projects/requirements-to-verification/captures
```

## Inputs

- [../../Synthetic Requirements Sample.csv](../../Synthetic%20Requirements%20Sample.csv): source-pack synthetic requirements CSV with 25 rows for the interview demo.
- [fixtures/ambiguous_requirements_fixture.csv](fixtures/ambiguous_requirements_fixture.csv): synthetic test fixture with intentionally weak language.

Required input columns:

- `Requirement_ID`
- `Source_Type`
- `Requirement_Text`
- `Subsystem`
- `Requirement_Type`
- `Verification_Method`
- `Risk_Level`
- `Assumptions`
- `Ambiguity_Flag`
- `Proposed_Test`
- `Human_Review_Status`

## Outputs

Generated outputs are written to [generated_outputs](generated_outputs):

- `trace_matrix.csv` and `trace_matrix.md`
- `ambiguity_report.csv` and `ambiguity_report.md`
- `assumptions_register.csv` and `assumptions_register.md`
- `review_checklist.csv` and `review_checklist.md`
- `run_summary.md`

Mock captures are written to [captures](captures):

- `cli_tool_run.md`
- `trace_matrix_preview.md`
- `ambiguity_report_preview.md`
- `assumptions_register_preview.md`
- `review_checklist_preview.md`

Current regenerated package summary:

- Requirements loaded: 25
- Trace matrix rows: 25
- Ambiguity findings: 41
- Assumptions: 37
- Checklist items: 8

## Human Review Controls

- Treat every generated artifact as draft decision support.
- Verify requirement interpretation, verification method, evidence suggestion, assumptions, risk/ambiguity flag, and pass/fail criteria.
- Assign a qualified reviewer before using the package in any design-review workflow.
- Keep ambiguous rows open until a qualified engineer accepts, revises, rejects, or escalates them.
- Do not represent the tool output as engineering approval.

## Jose Review Pass

Review completed on 2026-06-13 for synthetic portfolio demonstration use.

- Formulas/rules: domain classification, verification-method mapping, ambiguity flags, and acceptance-criteria suggestions were reviewed as deterministic demo rules.
- Assumptions: [generated_outputs/assumptions_register.md](generated_outputs/assumptions_register.md) was reviewed as a draft assumption register, not verified engineering fact.
- Synthetic data: [../../Synthetic Requirements Sample.csv](../../Synthetic%20Requirements%20Sample.csv) and generated outputs remain synthetic automotive-lighting examples.
- Screenshots: [captures](captures) remain draft proof artifacts and are public-safe as synthetic Markdown captures.
- Publication wording: generated artifacts keep the synthetic label, human-review note, and `Needs review` classification where the workflow needs visible review gates.

## Codex Contribution

Codex contributed the deterministic Python CLI, schema validation, trace matrix generation, ambiguity checks, assumptions register, review checklist, Markdown/CSV exports, mock captures, tests, and project documentation.

## Jose Contribution

Jose defines the portfolio proof objective, engineering workflow boundary, synthetic automotive lighting framing, required review controls, acceptable public-data boundary, and final engineering judgment.

## Tests

From this folder:

```bash
python3 -m unittest discover -s tests
```

The tests verify CSV loading, required-column enforcement, trace matrix generation, weak-language detection, assumption links back to requirement IDs, review checklist generation, and output writing.

## Safe to Publish Status

Safe to publish for synthetic portfolio demonstration. The prototype uses synthetic data and deterministic rules, and the generated outputs and capture files have been reviewed for demo use; they remain decision-support artifacts only.

## Next Improvements

- Add a compact HTML preview page if the Markdown/CSV workflow needs a lighter demo surface.
- Add reviewer signoff metadata fields to the generated outputs.
- Add configurable rule dictionaries for domain mapping and acceptance-criteria detection.
- Add final visual screenshots if the CLI evidence and generated capture files are not sufficient for a future portfolio page.
