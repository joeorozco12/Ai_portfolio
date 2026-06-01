# Requirements-to-Verification Tool

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## One-Line Summary

Codex-assisted workflow that converts messy synthetic requirement inputs into a traceable verification matrix.

## Status

Priority proof spine

## Problem

Engineering requirements often arrive as paragraphs, tables, screenshots, meeting notes, and partial test-plan fragments. Manual consolidation creates risk: missed verification hooks, ambiguous wording, duplicated requirements, and weak traceability.

## Engineering Context

Synthetic automotive lighting module with low beam, high beam, DRL dimming, diagnostics, input voltage limits, thermal behavior, and review gates. The public example uses generated data only.

## Workflow

- Load synthetic requirement notes and validation-method dictionary.
- Normalize text into candidate requirements with stable IDs.
- Classify subsystem, requirement type, and proposed verification method.
- Flag ambiguity, missing assumptions, and review risks.
- Export trace matrix, unresolved-questions list, and human-review checklist.

## Inputs

- synthetic_requirements.csv
- validation_method_dictionary.json
- review_rules.yaml
- optional prompt log with synthetic content

## Outputs

- requirements table
- verification trace matrix
- risk and assumptions register
- ambiguity report
- Markdown review brief
- Excel export

## Screenshot Placeholders

- before_messy_requirement_notes.png
- generated_trace_matrix.png
- review_checklist_export.png

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

Codex helps create parsing utilities, schema definitions, tests, export formatting, README content, and review-checklist generation.

## Jose Contribution

Jose defines the engineering taxonomy, decides acceptable verification mappings, reviews every AI-proposed classification, and owns final interpretation.

## AI Fundamentals Demonstrated

- Context engineering for messy engineering inputs
- Structured output generation
- Classification of requirement type and verification method
- Gap detection draft
- Documentation scaffolding

## Engineering Skills Demonstrated

- Requirements engineering
- Verification planning
- Traceability
- Risk and assumption capture
- Automotive lighting workflow awareness

## Risks and Mitigations

- AI may over-classify vague requirements. Mitigation: require uncertainty field and human approval.
- Synthetic data may be too clean. Mitigation: include ambiguous and conflicting examples.
- Traceability can imply false completeness. Mitigation: include gap count and review status.

## Next Improvements

- Add Streamlit review UI.
- Add pytest coverage for parser edge cases.
- Add before/after screenshot pair.
- Add short demo video using synthetic data.

## Safe to Publish?

Needs review until screenshots, sample outputs, and generated reports are confirmed synthetic.
