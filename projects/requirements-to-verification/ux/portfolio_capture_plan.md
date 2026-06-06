# Requirements-to-Verification Portfolio Capture Plan

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This plan identifies the proof captures needed to explain the Project 1 workflow in a portfolio or interview. Captures should show workflow clarity, traceability, review gates, and publication control.

This document does not define visual mockups, branding, colors, icons, or UI polish.

## Capture Principles

- Show synthetic labels and human-review language.
- Show `Requirement_ID` traceability.
- Show generated suggestions separately from reviewer decisions.
- Show assumptions separately from confirmed requirement content.
- Show unresolved review counts and blocked states.
- Show export readiness separately from safe-to-publish status.
- Avoid restricted organization, program, source-system, document, file-path, part, validation, cost, or private reviewer details.

## Required Captures

| Capture | Purpose | Required Evidence | Best Interview Point |
|---|---|---|---|
| Reviewer dashboard | Show workflow status and review priorities. | Requirement count, ambiguity count, assumption count, blocked count, export-ready count, safe-to-publish status. | "The tool makes unresolved review work visible before export." |
| Requirement detail view | Show source-to-decision traceability. | `Requirement_ID`, source text excerpt, generated interpretation, ambiguity findings, assumptions, verification mapping, review state. | "The engineer can see exactly what the tool inferred and what still needs review." |
| Ambiguity triage view | Show issue detection and human disposition. | Issue type, trigger, explanation, severity, recommended reviewer action, reviewer disposition field. | "AI accelerates ambiguity detection, but a reviewer owns disposition." |
| Export package summary | Show generated artifact package and unresolved counts. | Trace matrix, ambiguity report, assumptions register, review checklist, run summary, unresolved review count. | "The workflow produces reviewable artifacts, not final engineering approval." |
| Safe-to-publish checklist | Show portfolio governance. | Synthetic label, human-review note, publication classification, restricted-detail screening, AI-approval wording check. | "Publication is a separate gate from engineering workflow output." |

## Recommended Capture Order

1. Reviewer dashboard.
2. Requirement detail view for `SYN-REQ-004`.
3. Ambiguity triage view for `SYN-REQ-004`.
4. Export package summary.
5. Safe-to-publish checklist.

## `SYN-REQ-004` Capture Notes

Use `SYN-REQ-004` as the main walkthrough example because it has multiple review signals:

- Missing numeric limits.
- Unclear owner.
- Unclear pass/fail criteria.
- Source ambiguity flag.
- Linked assumptions `SYN-ASM-005`, `SYN-ASM-006`, and `SYN-ASM-007`.
- Acceptance criteria remains `TBD` pending qualified engineer review.

This makes it a strong portfolio example for ambiguity, assumptions, verification mapping, and human-review gates.

## Capture Acceptance Criteria

Each capture is acceptable when:

- Synthetic label is visible.
- Human-review note is visible or referenced.
- No restricted details are visible.
- The capture explains one workflow decision.
- The capture does not imply AI approves requirements or verification methods.
- The viewer can identify what the next human action is.

## Capture Backlog Before UI

Until a UI exists, portfolio captures may use:

- Markdown capture files.
- Generated Markdown outputs.
- Terminal-style run summaries.
- Static screenshot-ready summaries.

The first UI capture should not be started until the review-log template, validator, dashboard metric generator, and normalized export package exist.

