# Requirements-to-Verification Reviewer Dashboard Requirements

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This document defines the reviewer dashboard requirements for the Requirements-to-Verification Tool. The dashboard is the first portfolio proof screen because it shows whether an engineer can understand the synthetic input, generated findings, unresolved review work, export readiness, and publication gate without confusion.

This is a workflow requirements document. It does not define app code, visual mockups, branding, colors, icons, or UI polish.

## Dashboard Job

Help an electrical engineer, design reviewer, validation engineer, or portfolio interviewer answer:

- What requirements entered the workflow?
- What ambiguity did the tool detect?
- What assumptions still need review?
- Which verification mappings need attention?
- Which rows are blocked?
- Which rows are ready for export?
- Is the package safe for portfolio discussion?

## Data Sources

| Dashboard Area | Primary Source | Supporting Source |
|---|---|---|
| Requirement count and row status | `generated_outputs/trace_matrix.csv` | Input CSV and run summary |
| Ambiguity findings | `generated_outputs/ambiguity_report.csv` | Trace matrix |
| Assumptions | `generated_outputs/assumptions_register.csv` | Trace matrix |
| Verification mapping readiness | `generated_outputs/trace_matrix.csv` | `generated_outputs/review_checklist.csv` |
| Export readiness | Trace matrix, ambiguity report, assumptions register, review checklist | Run summary |
| Safe-to-publish status | Run summary and safe-to-publish checklist | Review states and export package |

## Required Top-Level Metrics

| Metric | Current Sample Count | Formula | Required Interpretation |
|---|---:|---|---|
| Requirements processed | 12 | Count rows in `trace_matrix.csv`. | Shows how many requirements entered trace review. |
| Open ambiguity findings | 19 | Count ambiguity report rows where `Human_Review_Status` is `Needs review`. | Shows issues requiring reviewer disposition. |
| Unresolved assumptions | 18 | Count assumptions register rows where `Status` is `Needs review`. | Shows assumptions that cannot be treated as confirmed facts. |
| Verification mapping gaps | Derived from checklist and trace rows | Count blank or rejected mapping fields, `TBD` acceptance criteria, and checklist rows that remain `Needs review`. | Shows where verification method or acceptance criteria review is incomplete. |
| Blocked rows | Not explicit in current generated files | Count rows with normalized review state `Blocked` after reviewer disposition exists. | Shows rows that cannot proceed to export. |
| Export-ready rows | 0 before reviewer dispositions | Count rows with normalized review state `Export ready`. | Shows rows eligible for package inclusion, not engineering approval. |
| Safe-to-publish status | Needs review | Read publication classification and publication checklist result. | Shows whether portfolio use is cleared. |

## Required Breakdown Metrics

### Ambiguity Breakdown

Current sample counts from `ambiguity_report.csv`:

| Issue Type | Count | Dashboard Use |
|---|---:|---|
| Unclear owner | 12 | Shows rows needing reviewer ownership before export. |
| Missing numeric limits | 3 | Shows requirements that may not be testable without measurable criteria. |
| Unclear pass/fail criteria | 3 | Shows requirements that need acceptance criteria review. |
| Source ambiguity flag | 1 | Shows source-tagged ambiguity carried into review. |

The dashboard should let the reviewer filter by issue type, severity, linked requirement ID, and reviewer disposition.

### Severity Breakdown

Current sample counts from `ambiguity_report.csv`:

| Severity | Count | Dashboard Use |
|---|---:|---|
| Low | 12 | Lower-risk review items, still requiring disposition. |
| Medium | 7 | Higher-priority ambiguity and acceptance-criteria review items. |

Severity does not approve or reject a requirement. It only helps prioritize review.

### Checklist Breakdown

Current sample counts from `review_checklist.csv`:

| Checklist Status | Count | Dashboard Use |
|---|---:|---|
| Ready for review | 4 | Generated checklist areas are available for human inspection. |
| Needs review | 4 | Generated checklist areas require reviewer action before export or publication. |

`Ready for review` means available for review. It does not mean accepted or approved.

## Required Row Groupings

| Group | Inclusion Rule | Primary Reviewer Action |
|---|---|---|
| Needs ambiguity disposition | Requirement has one or more ambiguity findings with `Needs review`. | Accept for demo, revise, reject, escalate, or block each finding. |
| Needs assumption disposition | Requirement has one or more linked assumptions with `Needs review`. | Accept for demo, revise, reject, escalate, or block each assumption. |
| Needs verification mapping review | Requirement has missing method, weak acceptance criteria, `TBD` criteria, or checklist dependency. | Confirm, revise, reject, or defer the mapping. |
| Blocked | Requirement or artifact has missing required evidence, unsafe content, or reviewer blocker. | Record blocker reason and corrective action. |
| Reviewed demo | Required findings are dispositioned for synthetic/demo use. | Continue to trace matrix review or return to review if edited. |
| Export ready | Required traceability, ambiguity, assumption, and mapping gates are complete for package inclusion. | Include in export package while retaining human-review language. |
| Safe to publish | Exported artifact passes synthetic-data, human-review, and restricted-detail checks. | Use for portfolio proof or interview discussion. |

## Required Dashboard Sections

### 1. Workflow Status Summary

Must show:

- Total requirements processed.
- Open ambiguity findings.
- Open assumptions.
- Checklist areas needing review.
- Blocked row count.
- Export-ready row count.
- Safe-to-publish status.

Must not imply that any generated output is engineering approval.

### 2. Review Priority Queue

Must show rows in this order:

1. Blocked rows.
2. Medium-severity ambiguity findings.
3. Requirements with missing numeric limits or unclear pass/fail criteria.
4. Requirements with unresolved assumptions.
5. Requirements with verification mapping gaps.
6. Rows ready for trace matrix review.

Each row must include `Requirement_ID`, primary issue reason, source artifact, current review state, and next reviewer action.

### 3. Requirement Review Table

Must show:

- `Requirement_ID`
- Requirement text excerpt
- Domain or subsystem category
- Verification method
- Ambiguity count
- Assumption count
- Acceptance criteria status
- Review state
- Next action

The table must preserve traceability back to source rows and generated artifacts.

### 4. Ambiguity Panel

Must show:

- Issue type
- Trigger
- Explanation
- Severity
- Recommended reviewer action
- Linked requirement ID
- Reviewer disposition

The reviewer must be able to move each item to `Reviewed demo`, `Needs review`, or `Blocked`.

### 5. Assumptions Panel

Must show:

- Assumption ID
- Linked requirement ID
- Assumption statement
- Rationale
- Risk if incorrect
- Owner/reviewer placeholder
- Status

Assumptions must remain separate from confirmed requirement content.

### 6. Verification Mapping Panel

Must show:

- Requirement ID
- Existing verification method
- Suggested verification evidence
- Acceptance criteria
- Related checklist area
- Reviewer note

Suggested mappings must remain review-owned and editable.

### 7. Export Readiness Summary

Must show:

- Included artifact list.
- Trace matrix row count.
- Ambiguity report count.
- Assumptions register count.
- Checklist count.
- Unresolved review count.
- Blocked item count.
- Human-review note.

Export readiness must be blocked when required review issues remain unresolved.

### 8. Safe-To-Publish Summary

Must show:

- Synthetic-data label.
- Human-review note.
- Publication classification.
- Restricted-detail screening result.
- AI-approval wording check.
- Final publication decision.

Safe-to-publish status must remain `Needs review` until the publication checklist passes.

## Required Interactions

| Interaction | Dashboard Requirement |
|---|---|
| Select requirement | Open requirement detail view with linked ambiguity, assumption, mapping, and trace rows. |
| Filter by issue type | Show only requirements linked to the selected ambiguity type. |
| Filter by review state | Show rows grouped by `Needs review`, `Blocked`, `Reviewed demo`, `Export ready`, and `Safe to publish`. |
| Filter by checklist area | Show requirements affected by testability, traceability, acceptance criteria, assumptions, or signoff gaps. |
| Record disposition | Capture reviewer action, note, prior state, new state, and linked requirement ID. |
| Send back to review | Move edited or challenged rows back to `Needs review`. |
| Mark export ready | Allow only when required linked review issues are resolved. |
| Open export summary | Show artifact list and unresolved counts before package use. |

## Portfolio Proof Requirements

The dashboard screenshot or capture should make these points obvious:

- The tool processed synthetic automotive lighting requirements.
- Ambiguity detection is traceable to requirement IDs.
- Assumptions are separated from confirmed content.
- Verification suggestions are draft review artifacts.
- Human review is required before export or publication.
- The export package is governed by review states.
- Safe-to-publish status is separate from export readiness.

## Acceptance Criteria

The reviewer dashboard requirements are satisfied when:

- Every displayed metric maps to a named generated artifact.
- Every row-level item preserves `Requirement_ID`.
- Every generated suggestion has a visible review state.
- Every unresolved ambiguity or assumption appears in a review queue.
- No row can appear export-ready while required linked issues remain unresolved.
- Safe-to-publish status cannot pass without synthetic label, human-review note, and restricted-detail screening.
- The dashboard can support an interview walkthrough without visual polish or restricted details.

## Open Implementation Questions

- Should dashboard counts be generated by a future normalized JSON package or computed directly from CSV outputs?
- Should reviewer dispositions be stored as a separate `review_log.csv` before adding any UI?
- Should the dashboard show all generated rows by default or start with unresolved review items only?
- Should blocked rows remain visible in export summaries by default?
