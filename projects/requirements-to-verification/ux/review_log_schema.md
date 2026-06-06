# Requirements-to-Verification Review Log Schema

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This schema defines how reviewer dispositions should be captured before any UI is built. The review log gives the future dashboard a clean source for `Reviewed demo`, `Blocked`, `Export ready`, and `Safe to publish` state changes.

This document is a workflow-design artifact. It does not create app code, visual mockups, branding, colors, icons, or a review-log data file.

## Review Log Role

The generated outputs show tool findings. The review log records human decisions about those findings.

The review log should:

- Preserve traceability to `Requirement_ID`, source artifact, and review object.
- Capture reviewer action and state transition.
- Keep generated suggestions separate from reviewer disposition.
- Support dashboard counts for blocked, reviewed, export-ready, and safe-to-publish items.
- Avoid storing restricted details or private reviewer information.

The review log should not:

- Replace engineering approval.
- Rewrite source requirements.
- Hide unresolved findings.
- Mark generated suggestions as accepted without reviewer action.
- Store nonpublic organization, program, document, file-path, part, validation, cost, or private reviewer details.

## Proposed File

| Item | Recommendation |
|---|---|
| Future file name | `review_log.csv` |
| Future location | `projects/requirements-to-verification/generated_outputs/review_log.csv` or a dedicated review output folder |
| Current task status | Schema only; no data file created yet |
| Write behavior | Append-only event log |
| Read behavior | Dashboard reads latest event per object to derive current state |

## Core Schema

| Field | Required | Allowed / Expected Values | Purpose |
|---|---|---|---|
| `Review_Event_ID` | Yes | `SYN-REV-001`, `SYN-REV-002`, increasing synthetic IDs | Unique event identifier. |
| `Run_ID` | Yes | Synthetic run marker such as `SYN-RUN-001` | Links review event to generated output package. |
| `Review_Marker` | Yes | Review date, run marker, or safe placeholder | Indicates when review action was recorded without exposing private details. |
| `Reviewer_Role` | Yes | `Electrical engineer`, `Design reviewer`, `Validation engineer`, `Portfolio reviewer` | Captures review perspective. |
| `Reviewer_Label` | Yes | `qualified engineer reviewer`, `portfolio reviewer`, or safe placeholder | Avoids private reviewer information. |
| `Object_Type` | Yes | `requirement_row`, `ambiguity_finding`, `assumption`, `verification_mapping`, `trace_row`, `export_package`, `publication_gate` | Identifies what was reviewed. |
| `Object_ID` | Yes | `Requirement_ID`, `Assumption_ID`, `Check_ID`, issue key, or artifact name | Identifies the reviewed item. |
| `Linked_Requirement_ID` | Conditional | `SYN-REQ-###` or blank for package-level events | Preserves requirement traceability. |
| `Source_Artifact` | Yes | `trace_matrix.csv`, `ambiguity_report.csv`, `assumptions_register.csv`, `review_checklist.csv`, `run_summary.md` | Preserves source artifact traceability. |
| `Prior_State` | Yes | `Draft`, `Needs review`, `Reviewed demo`, `Blocked`, `Export ready`, `Safe to publish` | State before the action. |
| `Reviewer_Action` | Yes | `inspect`, `accept_for_demo`, `revise`, `reject`, `escalate`, `block`, `return_to_review`, `mark_export_ready`, `clear_publication_gate` | Captures the reviewer action. |
| `New_State` | Yes | `Draft`, `Needs review`, `Reviewed demo`, `Blocked`, `Export ready`, `Safe to publish` | State after the action. |
| `Disposition_Summary` | Yes | Short synthetic-safe summary | Explains reviewer decision. |
| `Reviewer_Notes` | No | Synthetic-safe note | Adds context without restricted details. |
| `Blocker_Reason` | Conditional | Required when `New_State` is `Blocked` | Explains why progress is stopped. |
| `Corrective_Action` | Conditional | Required when blocked or revised | Defines what must happen next. |
| `Export_Allowed` | Yes | `true` or `false` | Supports export-readiness dashboard counts. |
| `Publication_Allowed` | Yes | `true` or `false` | Supports safe-to-publish dashboard counts. |
| `Synthetic_Label_Confirmed` | Yes | `true`, `false`, `not_applicable` | Confirms synthetic label presence. |
| `Human_Review_Note_Confirmed` | Yes | `true`, `false`, `not_applicable` | Confirms human-review note presence. |
| `Restricted_Detail_Check` | Yes | `pass`, `fail`, `needs_review`, `not_applicable` | Records restricted-detail screening result. |
| `AI_Approval_Wording_Check` | Yes | `pass`, `fail`, `needs_review`, `not_applicable` | Confirms wording does not imply AI approval. |
| `Evidence_Reference` | Yes | Artifact path, row ID, or capture reference | Links decision to evidence. |

## Object Type Rules

| Object Type | Required Object ID | Required Linked Requirement ID | Typical Source Artifact |
|---|---|---|---|
| `requirement_row` | `Requirement_ID` | Same as object ID | Input CSV or trace matrix |
| `ambiguity_finding` | Synthetic issue key or `Requirement_ID` + `Issue_Type` | Required | `ambiguity_report.csv` |
| `assumption` | `Assumption_ID` | Required | `assumptions_register.csv` |
| `verification_mapping` | `Requirement_ID` | Required | `trace_matrix.csv` |
| `trace_row` | `Requirement_ID` | Required | `trace_matrix.csv` |
| `export_package` | Package marker or artifact list name | Optional | Generated outputs and run summary |
| `publication_gate` | Publication checklist marker | Optional | Run summary and safe-to-publish checklist |

## State Transition Rules

| Reviewer Action | Allowed Prior States | Allowed New States | Required Conditions |
|---|---|---|---|
| `inspect` | Any state | Same state | Source artifact and object ID must be present. |
| `accept_for_demo` | `Needs review` | `Reviewed demo` | Disposition summary and reviewer role required. |
| `revise` | `Needs review`, `Reviewed demo`, `Export ready`, `Safe to publish` | `Needs review` | Corrective action or revised note required. |
| `reject` | `Needs review` | `Blocked` | Blocker reason required. |
| `escalate` | `Needs review` | `Blocked` | Escalation reason and corrective action required. |
| `block` | Any state before `Safe to publish` | `Blocked` | Blocker reason required. |
| `return_to_review` | `Reviewed demo`, `Export ready`, `Safe to publish` | `Needs review` | Change reason required. |
| `mark_export_ready` | `Reviewed demo` | `Export ready` | Linked ambiguity, assumption, and mapping gates must be resolved or excluded. |
| `clear_publication_gate` | `Export ready` | `Safe to publish` | Synthetic label, human-review note, restricted-detail check, and AI-approval wording check must pass. |

## Dashboard Derivation Rules

The reviewer dashboard should derive current state from the latest review event for each unique object.

| Dashboard Metric | Review Log Rule |
|---|---|
| Blocked rows | Count latest events where `New_State` is `Blocked` and object type is row-level. |
| Reviewed demo rows | Count latest events where `New_State` is `Reviewed demo`. |
| Export-ready rows | Count latest events where `New_State` is `Export ready` and `Export_Allowed` is `true`. |
| Safe-to-publish status | Package-level latest event where `New_State` is `Safe to publish` and `Publication_Allowed` is `true`. |
| Open review items | Generated `Needs review` items minus objects with later review-log dispositions. |
| Publication blockers | Count latest events with `Publication_Allowed` as `false` and blocker reason present. |

## Example Synthetic Rows

| Review_Event_ID | Object_Type | Object_ID | Linked_Requirement_ID | Prior_State | Reviewer_Action | New_State | Disposition_Summary | Export_Allowed | Publication_Allowed |
|---|---|---|---|---|---|---|---|---|---|
| `SYN-REV-001` | `ambiguity_finding` | `SYN-REQ-004:Missing numeric limits` | `SYN-REQ-004` | `Needs review` | `revise` | `Needs review` | Reviewer needs a synthetic measurable limit before export. | `false` | `false` |
| `SYN-REV-002` | `assumption` | `SYN-ASM-007` | `SYN-REQ-004` | `Needs review` | `accept_for_demo` | `Reviewed demo` | Assumption accepted for synthetic demo discussion only. | `false` | `false` |
| `SYN-REV-003` | `export_package` | `SYN-PKG-001` |  | `Reviewed demo` | `mark_export_ready` | `Export ready` | Package ready for review discussion with human-review note visible. | `true` | `false` |

Example rows are synthetic and are not a completed review record.

## Validation Rules

A future review-log validator should fail when:

- A required field is blank.
- `New_State` is `Blocked` and `Blocker_Reason` is blank.
- `Reviewer_Action` is inconsistent with the state transition table.
- `mark_export_ready` is used while required linked findings remain unresolved.
- `clear_publication_gate` is used without passing synthetic label, human-review note, restricted-detail, and AI-approval wording checks.
- A row references an object that does not exist in the generated outputs.
- A row includes restricted details or private reviewer information.

## Open Implementation Questions

- Should `review_log.csv` be generated empty with headers after each CLI run, or created only when review actions are recorded?
- Should the review log live in `generated_outputs/` or a separate `review_outputs/` folder?
- Should review actions update dashboard state only, or should reviewed export packages include a copy of the final review log?
- Should package-level publication review require a separate artifact from row-level engineering review?
