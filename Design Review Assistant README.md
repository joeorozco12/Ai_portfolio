# Design Review Readiness Assistant

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Workflow that converts synthetic project notes into a design-review readiness packet with risks, assumptions, actions, and missing evidence.

## Status

Secondary portfolio project

Working deterministic generator and validator are implemented under [projects/design-review-readiness-assistant](projects/design-review-readiness-assistant). The project already produces Markdown, CSV, and generated PNG evidence for the local interview demo.

## Problem

Design reviews lose time when assumptions, open questions, test gaps, and decision records are scattered or stale.

## Engineering Context

Synthetic automotive lighting electronics review packet with requirements, WCCA prep status, risks, validation hooks, and action items.

## Workflow

- Load synthetic design notes, requirement table, and action log.
- Extract assumptions, open issues, unresolved decisions, and missing evidence.
- Generate readiness score and review agenda.
- Export design-review packet and human-review checklist.

## Inputs

- [projects/design-review-readiness-assistant/inputs/synthetic_lighting_review_notes.md](projects/design-review-readiness-assistant/inputs/synthetic_lighting_review_notes.md)

## Outputs

- [projects/design-review-readiness-assistant/outputs/design_review_packet.md](projects/design-review-readiness-assistant/outputs/design_review_packet.md)
- [projects/design-review-readiness-assistant/outputs/risk_register.csv](projects/design-review-readiness-assistant/outputs/risk_register.csv)
- [projects/design-review-readiness-assistant/outputs/assumptions_list.md](projects/design-review-readiness-assistant/outputs/assumptions_list.md)
- [projects/design-review-readiness-assistant/outputs/validation_test_gaps.md](projects/design-review-readiness-assistant/outputs/validation_test_gaps.md)
- [projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.md](projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.md)
- [projects/design-review-readiness-assistant/outputs/diagnostic_response_table.md](projects/design-review-readiness-assistant/outputs/diagnostic_response_table.md)

## Screenshots Or Capture Placeholders

- [projects/design-review-readiness-assistant/screenshots/dashboard_overview.png](projects/design-review-readiness-assistant/screenshots/dashboard_overview.png)
- [projects/design-review-readiness-assistant/screenshots/review_packet_preview.png](projects/design-review-readiness-assistant/screenshots/review_packet_preview.png)
- [projects/design-review-readiness-assistant/screenshots/risk_register_export.png](projects/design-review-readiness-assistant/screenshots/risk_register_export.png)
- [projects/design-review-readiness-assistant/screenshots/mode_to_test_matrix.png](projects/design-review-readiness-assistant/screenshots/mode_to_test_matrix.png)
- [projects/design-review-readiness-assistant/screenshots/diagnostic_response_table.png](projects/design-review-readiness-assistant/screenshots/diagnostic_response_table.png)

## Sanitized Sample Data

Use the source-pack CSV files where applicable. Public examples must remain synthetic and should avoid internal naming, real customer requirements, proprietary schematics, internal limits, and program-specific values.

## Human Review Controls

Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Review checkpoints:

- Confirm all inputs are synthetic or sanitized.
- Confirm AI-proposed classifications are reviewed.
- Confirm calculations, formulas, limits, and pass/review labels are verified by an engineer.
- Confirm output is marked as draft until approved.

## Codex Contribution

Codex helps implement parsing, report assembly, schema checks, and reusable markdown templates.

## Jose Contribution

Jose defines readiness criteria, verifies risk severity, confirms assumptions, and decides what must be addressed before review.

## AI Fundamentals Demonstrated

- Summarization with structure
- Risk extraction
- Assumption extraction
- Review agenda drafting
- Gap detection

## Engineering Skills Demonstrated

- Design-review planning
- Risk management
- Validation readiness
- Cross-functional communication
- Engineering judgment

## Risks and Mitigations

- Readiness score can look authoritative. Mitigation: label as draft support metric.
- Missing evidence may be misclassified. Mitigation: engineer review checklist.

## Next Improvements

- Add a local reviewer-disposition UI after the generated packet is reviewed.
- Add deeper row-count tests for Markdown tables.
- Add final public screenshots only after Jose accepts the generated PNG evidence.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
