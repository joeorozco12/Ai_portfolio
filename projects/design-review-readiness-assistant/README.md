# Engineering Design Review Readiness Assistant

Synthetic Codex-assisted workflow for preparing automotive lighting design-review packets, risk registers, validation gaps, mode-to-test matrices, and diagnostic response tables.

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Safe to publish

## Preparation-Only Boundary

This project structures synthetic automotive lighting review notes into draft design-review preparation artifacts. It does not approve requirements, circuits, validation plans, test results, risk disposition, design readiness, or release decisions. AI prepares structured review artifacts; qualified engineers own final judgment.

## Portfolio Workflow Fit

Project 4 sits downstream of:

- Project 1: Requirements-to-Verification Tool
- Project 6: LED Datasheet-to-Model Extractor evidence
- Project 5: Lighting Feasibility Mini-Simulator
- Project 2: AI-Assisted WCCA Prep Tool

Project 1 turns synthetic requirements into reviewable verification structure. Project 6 demonstrates reviewed LED model extraction boundaries. Project 5 performs first-pass feasibility screening from reviewed synthetic inputs. Project 2 prepares synthetic WCCA inputs, assumptions, and evidence prompts. Project 4 uses that kind of upstream structure as design-review preparation context: it converts review notes, risks, assumptions, validation gaps, mode behavior, and diagnostic expectations into structured artifacts that are easier for a qualified engineer to inspect before review.

## Problem

Design-review preparation can lose time when assumptions, unresolved risks, missing evidence, and validation gaps are spread across notes and informal action items.

## Engineering Context

The synthetic example uses a generic automotive lighting electronics workflow covering low beam, high beam, daytime running lamp behavior, input-voltage operation, thermal review triggers, diagnostic behavior, WCCA readiness, and validation planning. It excludes proprietary employer, customer, supplier, program, schematic, BOM, harness, cost, internal test, internal requirement, ticket, part-number, and file-path details.

## Workflow

1. Read [inputs/synthetic_lighting_review_notes.md](inputs/synthetic_lighting_review_notes.md).
2. Parse the synthetic review-note table.
3. Map review topics into draft risks, assumptions, validation gaps, reviewer placeholders, and a review agenda.
4. Generate Markdown, CSV, and screenshot artifacts, including a mode-to-test matrix and diagnostic response table.
5. Validate the risk-register schema, review-safe statuses, human-review fields, reviewer fields, and screenshot presence.
6. Keep generated outputs visibly review-owned, with reviewer disposition captured separately from generated draft rows.

```text
Synthetic review notes
-> Parser / generator script
-> Structured review artifacts
-> Schema and safety validation
-> Screenshots / portfolio evidence
-> Qualified engineer review
```

## Inputs

- [inputs/synthetic_lighting_review_notes.md](inputs/synthetic_lighting_review_notes.md)

## Outputs

- [outputs/design_review_packet.md](outputs/design_review_packet.md)
- [outputs/risk_register.csv](outputs/risk_register.csv)
- [outputs/assumptions_list.md](outputs/assumptions_list.md)
- [outputs/validation_test_gaps.md](outputs/validation_test_gaps.md)
- [outputs/human_review_required.md](outputs/human_review_required.md)
- [outputs/mode_to_test_matrix.csv](outputs/mode_to_test_matrix.csv)
- [outputs/mode_to_test_matrix.md](outputs/mode_to_test_matrix.md)
- [outputs/diagnostic_response_table.csv](outputs/diagnostic_response_table.csv)
- [outputs/diagnostic_response_table.md](outputs/diagnostic_response_table.md)
- [screenshots/dashboard_overview.png](screenshots/dashboard_overview.png)
- [screenshots/review_packet_preview.png](screenshots/review_packet_preview.png)
- [screenshots/risk_register_export.png](screenshots/risk_register_export.png)
- [screenshots/mode_to_test_matrix.png](screenshots/mode_to_test_matrix.png)
- [screenshots/diagnostic_response_table.png](screenshots/diagnostic_response_table.png)

The mode-to-test matrix and diagnostic response table support design-review preparation by making mode behavior, verification needs, required evidence, and diagnostic expectations easier to inspect before human review. They are not final validation plans or approved diagnostic strategies.

## Screenshots Or Screenshot Placeholders

- `dashboard_overview.png`: generated synthetic readiness dashboard mockup.
- `review_packet_preview.png`: generated synthetic review packet preview.
- `risk_register_export.png`: generated synthetic risk register export.
- `mode_to_test_matrix.png`: generated synthetic mode matrix preview.
- `diagnostic_response_table.png`: generated synthetic diagnostic response preview.

## Sanitized Sample Data

All examples are generated synthetic automotive lighting notes. Values are generic placeholders for demonstration only and must not be treated as validated engineering limits.

## Human Review Controls

- Confirm every input is synthetic or sanitized before use.
- Review each extracted risk, assumption, and validation gap.
- Confirm severity, likelihood, readiness, priority, and mitigation labels are draft only.
- Keep reviewer disposition fields as placeholders until a qualified engineer reviews them.
- Block publication if any proprietary or customer-specific detail appears.

## Jose Review Pass

Review completed on 2026-06-13 for synthetic portfolio demonstration use.

- Formulas/rules: risk, severity, likelihood, readiness, mode-to-test, and diagnostic-response mappings were reviewed as draft preparation mappings.
- Assumptions: [outputs/assumptions_list.md](outputs/assumptions_list.md) remains a draft assumption artifact with a reviewer disposition path.
- Synthetic data: [inputs/synthetic_lighting_review_notes.md](inputs/synthetic_lighting_review_notes.md) and generated CSV/Markdown outputs use only synthetic examples.
- Screenshots: [screenshots](screenshots) were reviewed for public-safe synthetic portfolio use and do not imply final design readiness.
- Publication wording: generated outputs retain the human-review boundary and do not imply engineering approval.

## Codex Contribution

Codex provides the deterministic generator, schema validation script, output templates, CSV export, screenshot mockups, and repeatable run commands.

## Jose Contribution

Jose defines the design-review readiness criteria, lighting-engineering framing, risk taxonomy, review boundaries, final engineering interpretation, and publication decision.

## How To Run

From this project folder:

```bash
python3 scripts/generate_design_review_packet.py
python3 scripts/validate_project4_outputs.py
```

From the portfolio root:

```bash
python3 projects/design-review-readiness-assistant/scripts/generate_design_review_packet.py
python3 projects/design-review-readiness-assistant/scripts/validate_project4_outputs.py
```

## Live Demo

From this project folder:

```bash
python3 demo_project4.py
```

The live demo runs the generator, runs validation, lists the key generated outputs, and repeats the human-review boundary for interview use.

## Example Validation Command

```bash
python3 scripts/validate_project4_outputs.py
```

Expected result:

```text
Project 4 validation passed.
README sections, output files, CSV schemas, statuses, human-review fields, reviewer fields, and screenshots are valid.
```

## Validation Checks

The validator checks:

- README section completeness.
- Required output file presence.
- Risk register schema.
- Mode-to-test matrix schema.
- Diagnostic response table schema.
- Review-safe status values.
- Human-review language in each generated row.
- Reviewer placeholder fields in generated Markdown outputs.
- Screenshot file presence.

## AI Fundamentals Demonstrated

- Structured extraction
- Deterministic mapping from notes to review artifacts
- Risk and assumption classification
- Gap detection
- Human-in-the-loop review design
- Schema validation
- Output completeness checks

## What This Demonstrates

- Unstructured notes can be converted into structured review artifacts.
- Risks, assumptions, validation gaps, mode behavior, and diagnostics can be organized for review.
- Schema checks and safety boundaries can be applied to generated engineering-preparation outputs.
- AI remains inside a human-review workflow.
- The project creates publishable evidence without proprietary data.

## Engineering Skills Demonstrated

- Design-review preparation
- Risk register creation
- Assumption management
- Validation planning
- Engineering communication
- Safe handling of public portfolio artifacts

## Risks And Mitigations

- Risk: A readiness packet can look like approval. Mitigation: label every output as draft preparation only.
- Risk: AI may misclassify engineering severity. Mitigation: require qualified engineer review before use.
- Risk: Synthetic examples may drift toward real program details. Mitigation: keep generic IDs, generic subsystem names, and publication checks.
- Risk: Generated screenshots may look more complete than the underlying workflow. Mitigation: keep `Needs review` labels visible and list proof gaps.

## Next Improvements

- Add a small local UI for reviewer dispositions.
- Add deeper tests for Markdown table row counts.
- Add a synthetic fault-injection checklist.
- Add richer reviewer signoff fields if future generated packets need embedded disposition metadata.

## Safe-to-Publish Status

- Synthetic automotive lighting examples only.
- No proprietary company, customer, supplier, schematic, requirement, or internal document content.
- Generated outputs may retain `Needs review` labels to preserve the human-review boundary.
- AI does not approve design readiness or engineering release.
- Safe to publish for synthetic portfolio demonstration.

## Proof Gaps

- No local review UI yet.
- No final validation evidence is attached.
- No final diagnostic validation evidence is attached.
- Future mapping, screenshot, packet-template, or validation changes require another review pass.
