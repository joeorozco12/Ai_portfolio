# Design Review Readiness Assistant

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Workflow that converts synthetic project notes into a design-review readiness packet with risks, assumptions, actions, and missing evidence.

## Status

Secondary portfolio project

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

- synthetic_design_notes.md
- requirements_trace.csv
- risk_register.csv
- test_plan_outline.md

## Outputs

- readiness brief
- risk register
- assumption log
- action-item list
- review agenda
- evidence gap list

## Screenshot Placeholders

- readiness_dashboard.png
- review_packet_preview.png
- risk_register_export.png

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

- Add readiness dashboard.
- Add action-owner export.
- Add sample review packet screenshots.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
