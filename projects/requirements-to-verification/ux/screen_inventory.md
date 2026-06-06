# Requirements-to-Verification UX Screen Inventory

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Scope

This inventory lists only the screens needed to complete the Requirements-to-Verification workflow. It is not a visual mockup, branding plan, component library, or UI polish pass.

The screen sequence should support an engineer moving from synthetic input -> reviewable output -> human decision point without confusion.

## Best Portfolio Proof Screens

1. Reviewer dashboard
2. Requirement detail view
3. Ambiguity triage view
4. Export package summary

These screens show the strongest evidence of requirements understanding, ambiguity detection, traceability, review gates, and export readiness.

## Global Confidentiality Boundary

Every screen must avoid showing nonpublic company, program, source-system, drawing, part, cost, validation, ticket, file-path, or controlled-document identifiers. Screens should use only synthetic automotive lighting examples and visible synthetic-data labeling.

## Project Landing / Run Setup

- **Screen purpose:** Start a controlled run of the Requirements-to-Verification workflow.
- **Primary user:** Electrical engineer
- **Key inputs shown:** Selected synthetic CSV path, required schema checklist, output folder, run mode.
- **Key outputs shown:** Readiness status before processing, expected artifact list.
- **Required user actions:** Confirm input is synthetic or sanitized; confirm output location; start run.
- **Review controls:** Human-review note must be visible before processing starts.
- **Portfolio screenshot value:** Moderate; shows disciplined setup but not the strongest proof artifact.
- **Data/provenance shown:** Input filename, row count after preview, required-column status, generation target.
- **What must NOT be shown because of confidentiality:** Restricted source-system paths, internal repository names, private document names, nonpublic program labels, or controlled source references.

## Input Preview

- **Screen purpose:** Let the user inspect incoming requirement rows before parsing outputs are trusted.
- **Primary user:** Electrical engineer
- **Key inputs shown:** Requirement IDs, requirement text excerpts, subsystem, requirement type, verification method, risk level, human-review status.
- **Key outputs shown:** Schema pass/fail result, row count, missing-column warnings, synthetic-data label.
- **Required user actions:** Confirm the displayed rows are appropriate for processing; stop if restricted details appear.
- **Review controls:** Block run if required columns are missing or if user does not confirm synthetic/sanitized input.
- **Portfolio screenshot value:** Moderate; useful for explaining source-to-output traceability.
- **Data/provenance shown:** Source filename, row numbers, required fields, import timestamp or run marker.
- **What must NOT be shown because of confidentiality:** Real requirement IDs, organization-specific requirement language, controlled document titles, nonpublic test identifiers, or controlled validation references.

## Requirement Table

- **Screen purpose:** Provide the main parsed dataset for sorting, filtering, and selecting rows for deeper review.
- **Primary user:** Electrical engineer
- **Key inputs shown:** Parsed requirement rows and source field values.
- **Key outputs shown:** Ambiguity count, assumption count, verification mapping status, review state per row.
- **Required user actions:** Filter by unresolved review needs; select rows for detail review.
- **Review controls:** Rows with ambiguity, missing assumptions, or incomplete verification mapping must remain in `Needs review` or `Blocked`.
- **Portfolio screenshot value:** High if shown as a reviewer dashboard summary.
- **Data/provenance shown:** Requirement ID, source row, original text excerpt, generated flags, review state.
- **What must NOT be shown because of confidentiality:** Full nonpublic requirement text, internal owner names, controlled source links, private validation IDs, or program-specific references.

## Ambiguity Triage Dashboard

- **Screen purpose:** Prioritize ambiguous requirements and expose why review is required.
- **Primary user:** Design reviewer
- **Key inputs shown:** Requirement ID, original text excerpt, ambiguity reason, risk level, proposed next action.
- **Key outputs shown:** Ambiguity category counts, open issue list, review status by row.
- **Required user actions:** Accept issue, revise wording, assign clarification action, or mark as blocked.
- **Review controls:** No ambiguity item can move to `Export ready` without reviewer disposition.
- **Portfolio screenshot value:** Very high; this is one of the best proof screens because it shows review intelligence and human gates.
- **Data/provenance shown:** Rule reason, source requirement ID, source row, prior review status, reviewer disposition placeholder.
- **What must NOT be shown because of confidentiality:** Real program issue text, named reviewers, internal action-item IDs, private requirement sources, or controlled meeting notes.

## Requirement Detail View

- **Screen purpose:** Show one requirement with its source text, generated findings, assumptions, verification mapping, and review controls.
- **Primary user:** Electrical engineer
- **Key inputs shown:** Original synthetic requirement row, subsystem, requirement type, proposed test, existing assumptions.
- **Key outputs shown:** Ambiguity findings, inferred assumptions, suggested verification method, trace links, review state.
- **Required user actions:** Confirm interpretation, edit reviewer notes, disposition assumptions, approve or reject verification suggestion.
- **Review controls:** Tool-generated suggestions must be marked as draft until the responsible engineer reviews them.
- **Portfolio screenshot value:** Very high; this is one of the best screens for interview discussion because it shows source-to-decision traceability.
- **Data/provenance shown:** Source row, requirement ID, generated artifact links, rule triggers, reviewer decision field.
- **What must NOT be shown because of confidentiality:** Nonpublic design limits, private document excerpts, named engineering owners, real part identifiers, or internal source links.

## Assumptions Review

- **Screen purpose:** Keep inferred assumptions separate from confirmed requirement content.
- **Primary user:** Design reviewer
- **Key inputs shown:** Requirement ID, assumption text, assumption source, reason the assumption was generated.
- **Key outputs shown:** Assumption status, reviewer note, linked requirement, export impact.
- **Required user actions:** Accept for demo, revise, reject, escalate, or block export.
- **Review controls:** Any unresolved assumption must prevent `Safe to publish` and should block engineering use.
- **Portfolio screenshot value:** High; shows human-in-the-loop controls and assumption discipline.
- **Data/provenance shown:** Linked requirement ID, assumption source, creation rule or trigger, reviewer disposition.
- **What must NOT be shown because of confidentiality:** Real engineering assumptions from controlled programs, private source notes, organization-specific review comments, or controlled document references.

## Verification Mapping View

- **Screen purpose:** Review how each requirement maps to a verification method, proposed test, evidence expectation, and checklist item.
- **Primary user:** Validation engineer
- **Key inputs shown:** Requirement ID, requirement type, existing verification method, proposed test.
- **Key outputs shown:** Suggested verification method, evidence prompt, mapping completeness, review state.
- **Required user actions:** Confirm, revise, reject, or defer the verification mapping.
- **Review controls:** Verification method suggestions must never be treated as approval; reviewer ownership must remain visible.
- **Portfolio screenshot value:** High; demonstrates verification thinking beyond text parsing.
- **Data/provenance shown:** Requirement ID, source verification field, generated suggestion reason, reviewer status.
- **What must NOT be shown because of confidentiality:** Real test plans, controlled acceptance limits, internal lab references, private validation records, or program-specific evidence.

## Trace Matrix Review

- **Screen purpose:** Inspect complete requirement-to-verification traceability before export.
- **Primary user:** Validation engineer
- **Key inputs shown:** Requirement ID, subsystem, requirement type, ambiguity status, assumption status, verification method.
- **Key outputs shown:** Trace matrix row, completeness status, unresolved review flags.
- **Required user actions:** Confirm trace completeness; send incomplete rows back to ambiguity, assumption, or verification review.
- **Review controls:** Rows with unresolved ambiguity or assumptions must remain visibly blocked or needing review.
- **Portfolio screenshot value:** High; demonstrates traceability and review readiness.
- **Data/provenance shown:** Source requirement ID, generated trace row ID, artifact links, review state.
- **What must NOT be shown because of confidentiality:** Real traceability matrices, controlled source references, organization-specific document IDs, or nonpublic validation evidence.

## Export Package View

- **Screen purpose:** Summarize generated Markdown and CSV artifacts before delivery or portfolio capture.
- **Primary user:** Electrical engineer
- **Key inputs shown:** Selected input file, run summary, included artifact list, unresolved review counts.
- **Key outputs shown:** Trace matrix, ambiguity report, assumptions register, review checklist, run summary, export status.
- **Required user actions:** Confirm export package completeness and review state; open or save artifacts.
- **Review controls:** Export package must show whether any artifact remains `Needs review`, `Blocked`, or not safe for publication.
- **Portfolio screenshot value:** Very high; this is one of the best proof screens because it shows a completed reviewable package.
- **Data/provenance shown:** Generated artifact names, row counts, output location, run marker, synthetic-data label.
- **What must NOT be shown because of confidentiality:** Private file paths, internal storage locations, controlled document names, real artifact IDs, or nonpublic project labels.

## Safe-To-Publish Checklist

- **Screen purpose:** Confirm whether the workflow evidence can be used in a public portfolio or interview discussion.
- **Primary user:** Portfolio interviewer
- **Key inputs shown:** Generated screenshots, artifact list, publication classification, unresolved review risks.
- **Key outputs shown:** Safe-to-publish status, blocked publication reasons, final checklist result.
- **Required user actions:** Confirm synthetic data label, human-review language, no restricted details, and no implied AI approval.
- **Review controls:** Publication should remain blocked until all checklist items pass.
- **Portfolio screenshot value:** High; supports interview-safe discussion of governance and sanitization.
- **Data/provenance shown:** Artifact names, publication classification, review note, synthetic-data status.
- **What must NOT be shown because of confidentiality:** Nonpublic company names, private source material, controlled document references, real engineering identifiers, or unreviewed screenshots.
