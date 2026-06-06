# Codex Tool Development Case Study

[SYNTHETIC -- FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Publication Classification

Needs review

## Problem

Engineering workflow tools are useful only when they are scoped, repeatable, reviewable, and safe to publish. A loose prompt can produce impressive-looking text, but it does not prove that an engineer can build controlled tools for requirements cleanup, WCCA preparation, validation planning, risk review, or design-review readiness.

This case study shows how Jose Orozco uses Codex as a coding assistant to build practical engineering workflow tools with deterministic outputs, synthetic inputs, tests, and human review gates.

## Engineering Context

The synthetic scenario is an automotive lighting workflow where structured inputs need to become engineering review artifacts. Example outputs include requirements tables, assumptions lists, risk notes, WCCA preparation fields, validation needs, and design-review checklists.

All examples are synthetic or sanitized. The case study does not use restricted organization data, real schematics, real requirements, internal program details, or local machine paths.

## Why Codex Was Useful

Codex was useful because it helped turn a scoped engineering workflow into concrete project assets:

- folder structure
- CSV loaders
- deterministic calculations
- Markdown reports
- plot and capture outputs
- tests
- documentation
- review checklists

The value is execution speed and repeatability. Codex does not approve engineering decisions.

## Tool-Development Workflow

1. Define the engineering workflow problem.
2. Set the data boundary to synthetic or sanitized examples only.
3. Scope file edits to one project area.
4. Build deterministic logic before adding portfolio narrative.
5. Generate structured outputs such as CSV, Markdown, plots, or checklists.
6. Add tests for loaders, calculations, statuses, and generated files.
7. Review changed files before committing.
8. Keep final engineering judgment with the qualified reviewer.

## Example Input

```csv
Case_ID,Workflow_Input,Requested_Output,Review_Gate
SYN-WF-001,LED current tolerance note,WCCA prep fields,Formula review
SYN-WF-002,Validation gap note,Validation need table,Engineer review
SYN-WF-003,Thermal assumption note,Risk and assumption register,Design review
```

## Example Output

| Case | Generated Artifact | Draft Status | Human Review Gate |
|---|---|---|---|
| SYN-WF-001 | WCCA prep row with margin field | Needs review | Formula and unit review |
| SYN-WF-002 | Validation need with proposed method | Needs review | Verification planning review |
| SYN-WF-003 | Risk note with mitigation placeholder | Needs review | Design-review disposition |

## Iteration History

- Initial pass: scaffolded a small deterministic tool with CSV input and Markdown output.
- Cleanup pass: added explicit review boundaries, Codex/Jose contribution split, and safe-public status.
- Proof pass: expanded synthetic data, generated CSV summaries, plots, mock captures, and tests.
- Current case-study pass: packages the development process as an interview-ready artifact.

## Testing and Validation Approach

- Run deterministic unit tests for calculation logic when scripts are touched.
- Run output-generation tests when reports, CSV summaries, plots, or capture artifacts are produced.
- Run `git diff --check` before committing.
- Review staged files so unrelated work is not mixed into the same commit.
- Run a publication-safety text scan before publishing.

Tests support workflow reliability. They do not prove final engineering correctness.

## Human Review Controls

- A qualified engineer reviews formulas, units, assumptions, thresholds, statuses, and conclusions.
- AI-generated artifacts remain draft support materials until reviewed.
- Synthetic examples are checked before publication.
- Scope boundaries are verified through changed-file review.
- Final approval remains with the engineer.

## Codex Contribution

Codex contributes scaffolding, refactoring, deterministic script implementation, test generation, report formatting, plot/capture packaging, and documentation drafts.

## Jose Contribution

Jose defines the engineering workflow, data boundary, review gates, domain assumptions, validation expectations, acceptable claims, and final judgment.

## Limitations

- Synthetic examples do not represent a released design.
- Deterministic checks are simplified workflow demonstrations.
- Mock captures are not real screenshots.
- Review checklists are not complete until a qualified reviewer fills them out.
- The case study shows controlled development practice, not final engineering approval.

## Next Improvements

- Add final reviewed screenshots from a clean synthetic demo environment.
- Add a compact workflow diagram showing prompt, scoped files, validation, and review.
- Add a short transcript showing one controlled Codex iteration from task to tests.
- Link this case study to the strongest finished proof assets after review.

## Proof Gaps

- Final public-copy review is still needed.
- Screenshots are placeholders or mock captures unless explicitly labeled otherwise.
- The case study should be reviewed alongside the committed proof assets before publication.

## Safe to Publish Status

Needs review. The content is synthetic and portfolio-safe in structure, but final wording and screenshots still need qualified review before publication.
