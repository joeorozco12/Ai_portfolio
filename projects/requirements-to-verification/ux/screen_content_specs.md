# Requirements-to-Verification Screen Content Specs

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This document defines the exact fields each Project 1 workflow screen must show. It is content design for traceability, review clarity, and export readiness.

This document does not define visual mockups, branding, colors, icons, layout, or UI polish.

## Global Required Content

Every screen must show or preserve:

- `[SYNTHETIC — FOR DEMONSTRATION ONLY]`
- Human-review note
- Current review state
- Source artifact name
- Linked `Requirement_ID` when row-level data is shown
- Clear separation between tool-generated suggestions and reviewer decisions

## Reviewer Dashboard

| Content Area | Required Fields |
|---|---|
| Workflow status summary | Requirement count, open ambiguity count, open assumption count, checklist needs-review count, blocked count, export-ready count, safe-to-publish status. |
| Priority queue | `Requirement_ID`, primary issue reason, source artifact, severity, current review state, next reviewer action. |
| Requirement table | `Requirement_ID`, requirement text excerpt, detected domain, verification method, ambiguity count, assumption count, acceptance criteria status, review state. |
| Ambiguity summary | Issue type counts, severity counts, unresolved count. |
| Assumption summary | Linked requirement count, unresolved assumption count, owner/reviewer placeholder status. |
| Export summary | Included artifacts, unresolved review count, blocked count, publication classification. |

Required reviewer actions:

- Select requirement.
- Filter by issue type.
- Filter by review state.
- Open ambiguity, assumption, mapping, or trace detail.
- Record disposition through the future review log.

## Requirement Detail View

| Content Area | Required Fields |
|---|---|
| Source requirement | `Requirement_ID`, requirement text, source row reference, source artifact. |
| Generated interpretation | Detected domain, verification method, suggested verification evidence, acceptance criteria. |
| Ambiguity findings | Issue type, trigger, explanation, severity, recommended reviewer action, status. |
| Assumptions | Assumption ID, statement, rationale, risk if incorrect, owner/reviewer placeholder, status. |
| Review controls | Prior state, reviewer action, new state, reviewer note, blocker reason if applicable. |
| Trace links | Trace matrix row, linked ambiguity rows, linked assumption rows, checklist references. |

Required reviewer actions:

- Accept for demo.
- Revise.
- Reject.
- Escalate.
- Block.
- Return edited content to review.

## Ambiguity Triage View

| Content Area | Required Fields |
|---|---|
| Finding identity | `Requirement_ID`, issue type, source artifact. |
| Detection evidence | Trigger, explanation, severity, recommended reviewer action. |
| Requirement context | Requirement text excerpt, detected domain, current verification method. |
| Review disposition | Reviewer action, prior state, new state, reviewer note, blocker reason. |

Required reviewer actions:

- Accept issue for synthetic demo.
- Revise the response or required action.
- Reject the finding.
- Escalate for clarification.
- Block export until resolved.

## Assumptions Review

| Content Area | Required Fields |
|---|---|
| Assumption identity | Assumption ID, linked `Requirement_ID`, source artifact. |
| Assumption content | Assumption statement, rationale, risk if incorrect. |
| Review ownership | Owner/reviewer placeholder, current status, reviewer note. |
| Export effect | Whether unresolved assumption blocks export or publication. |

Required reviewer actions:

- Accept for demo.
- Revise assumption text.
- Reject assumption.
- Escalate assumption.
- Block linked requirement.

## Verification Mapping View

| Content Area | Required Fields |
|---|---|
| Mapping identity | `Requirement_ID`, source artifact, current review state. |
| Requirement context | Requirement text excerpt, domain, requirement type if available. |
| Generated mapping | Verification method, suggested verification evidence, acceptance criteria. |
| Checklist context | Review area, checklist item, checklist status, evidence, reviewer notes. |
| Review controls | Reviewer action, revised method or evidence, blocker reason if applicable. |

Required reviewer actions:

- Confirm mapping for synthetic demo use.
- Revise method, evidence, or acceptance criteria.
- Reject mapping.
- Defer mapping.
- Send linked requirement back to review.

## Export Summary

| Content Area | Required Fields |
|---|---|
| Package identity | Run marker, artifact list, source package status. |
| Artifact counts | Trace matrix rows, ambiguity findings, assumptions, checklist items. |
| Review counts | Needs-review count, reviewed-demo count, blocked count, export-ready count. |
| Required artifacts | Trace matrix, ambiguity report, assumptions register, review checklist, run summary. |
| Export gate | Export allowed, export blocked reason, unresolved review summary. |
| Human-review boundary | Required note visible and unchanged. |

Required reviewer actions:

- Confirm package completeness.
- Open unresolved review items.
- Mark package export-ready only when required gates pass.
- Return package to review after edits.

## Safe-To-Publish Checklist

| Content Area | Required Fields |
|---|---|
| Publication status | Publication classification, safe-to-publish status, checklist result. |
| Required labels | Synthetic-data label, human-review note. |
| Safety checks | Restricted-detail screening result, AI-approval wording check, unresolved blocker count. |
| Evidence | Artifact names, capture references, reviewer note. |
| Final decision | Safe to publish, needs review, or blocked. |

Required reviewer actions:

- Confirm synthetic label is visible.
- Confirm human-review note is visible.
- Confirm no restricted details are visible.
- Confirm no AI approval wording is present.
- Mark safe for portfolio use only after all checks pass.

## Content Acceptance Criteria

- A reviewer can identify what came from the source input.
- A reviewer can identify what the tool generated.
- A reviewer can identify what remains unresolved.
- A reviewer can identify which action is required next.
- A reviewer can explain why export readiness is separate from safe-to-publish status.

