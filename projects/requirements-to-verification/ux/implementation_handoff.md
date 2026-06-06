# Requirements-to-Verification UX Implementation Handoff

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This handoff summarizes the Project 1 UX package and defines the first non-visual implementation tasks. It is the bridge from workflow design to engineering implementation.

This document does not define visual mockups, branding, colors, icons, or UI polish.

## UX Package Summary

| Document | Role |
|---|---|
| `workflow_map.md` | Defines the end-to-end workflow from synthetic input to reviewable export and safe-to-publish gate. |
| `screen_inventory.md` | Defines the screens needed to complete the workflow. |
| `review_states.md` | Defines `Draft`, `Needs review`, `Reviewed demo`, `Blocked`, `Export ready`, and `Safe to publish`. |
| `data_contract.md` | Maps generated artifacts to UX screens, review states, and data groups. |
| `interaction_spec.md` | Defines reviewer actions and state transitions. |
| `reviewer_dashboard_requirements.md` | Defines dashboard metrics, row groupings, and proof-screen behavior. |
| `review_log_schema.md` | Defines the future reviewer-disposition record. |
| `screen_content_specs.md` | Defines exact fields for each screen. |
| `error_empty_states.md` | Defines missing-data, stale-output, empty-result, and failed-gate behavior. |
| `usability_test_plan.md` | Defines reviewer tasks to test workflow clarity. |
| `portfolio_capture_plan.md` | Defines proof captures for portfolio and interview discussion. |
| `ux_readiness_checklist.md` | Defines the final UX gate before implementation. |

## Implementation Principle

Build the non-visual workflow layer before any dashboard shell:

1. Preserve generated output traceability.
2. Add reviewer-disposition capture.
3. Generate dashboard metrics from deterministic artifacts.
4. Generate a normalized export package.
5. Only then build a basic dashboard shell.

## First Non-Visual Implementation Tasks

| Task | Output | Purpose | Done When |
|---|---|---|---|
| Review-log template | `generated_outputs/review_log.csv` headers or `review_outputs/review_log.csv` headers | Gives reviewers a place to record dispositions before UI exists. | Header fields match `review_log_schema.md`; no restricted details are introduced. |
| Review-log validator | CLI validation report | Prevents invalid state transitions and missing required evidence. | Validator catches missing object IDs, invalid transitions, missing blocker reasons, and failed publication-gate checks. |
| Dashboard metric generator | Markdown/CSV or JSON dashboard summary | Creates counts for ambiguity, assumptions, mapping gaps, blocked rows, export-ready rows, and safe-to-publish status. | Counts are derived from generated outputs plus latest review-log events. |
| Normalized export package | Single normalized artifact package | Gives a future UI one stable data source. | Package includes requirements, findings, assumptions, mappings, checklist, review states, and publication status. |

## Recommended Implementation Order

1. Add a review-log template with headers only.
2. Add a review-log validator.
3. Add a dashboard metric generator.
4. Add a normalized JSON export package.
5. Add tests for the review-log and dashboard metric logic.
6. Add a basic dashboard shell only after the data layer is stable.

## Data Sources To Preserve

| Source | Required Preservation |
|---|---|
| `Synthetic Requirements Sample.csv` | Requirement IDs, source row identity, input schema. |
| `generated_outputs/trace_matrix.csv` | Requirement traceability, generated evidence, acceptance criteria, publication status. |
| `generated_outputs/ambiguity_report.csv` | Issue type, trigger, explanation, severity, review status. |
| `generated_outputs/assumptions_register.csv` | Assumption ID, linked requirement, rationale, risk if incorrect, owner/reviewer placeholder. |
| `generated_outputs/review_checklist.csv` | Review area, checklist item, status, evidence, reviewer notes. |
| `generated_outputs/run_summary.md` | Package-level synthetic label, human-review note, publication classification. |

## Implementation Guardrails

- Keep AI-generated suggestions separate from reviewer decisions.
- Do not let `Export ready` mean engineering approval.
- Do not let `Safe to publish` bypass the synthetic-data and human-review checks.
- Do not overwrite generated outputs with reviewer decisions unless the workflow intentionally creates a reviewed export copy.
- Do not add restricted organization, program, source-system, document, file-path, part, validation, cost, or private reviewer details.
- Keep current CSV and Markdown outputs usable without a UI.

## Handoff Acceptance Criteria

The UX package is ready for non-visual implementation when:

- Each future implementation task maps to a UX document.
- Review-log fields are defined before reviewer data is stored.
- Dashboard metrics can be computed from named artifacts.
- Export readiness and safe-to-publish status remain separate.
- The next implementation can proceed without visual design decisions.

