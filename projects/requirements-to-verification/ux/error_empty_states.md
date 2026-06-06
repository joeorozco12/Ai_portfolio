# Requirements-to-Verification Error And Empty States

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This document defines workflow behavior when generated artifacts are missing, empty, stale, blocked, or not safe for publication.

This document does not define visual mockups, branding, colors, icons, layout, or UI polish.

## General Rules

- Error states must preserve the human-review boundary.
- Empty states must not imply the workflow is complete unless supporting evidence exists.
- Stale outputs must block export readiness.
- Failed publication checks must block safe-to-publish status.
- Every error or empty state must identify the source artifact and next reviewer action.

## Missing CSV Columns

| Item | Requirement |
|---|---|
| Trigger | Input file lacks one or more required columns. |
| Required message | Required input fields are missing; processing cannot create a traceable review package. |
| Required evidence | Missing column names, input file label, schema version or expected field list. |
| Review state | `Blocked` |
| Allowed actions | Fix input schema, choose a different synthetic input, or stop workflow. |
| Must not do | Do not infer missing fields silently or mark package export-ready. |

## Zero Ambiguity Findings

| Item | Requirement |
|---|---|
| Trigger | `ambiguity_report.csv` has zero rows. |
| Required message | No ambiguity findings were generated for this run; reviewer still owns requirement interpretation. |
| Required evidence | Requirement count, run marker, ambiguity report artifact. |
| Review state | `Needs review` until reviewer confirms the run is valid. |
| Allowed actions | Continue to trace matrix review, inspect requirement detail, or rerun with updated input. |
| Must not do | Do not imply every requirement is clear or approved. |

## Missing Assumptions

| Item | Requirement |
|---|---|
| Trigger | Assumptions register is missing, empty unexpectedly, or lacks linked requirement IDs. |
| Required message | Assumption evidence is missing or incomplete; reviewer cannot confirm whether generated outputs separate assumptions from facts. |
| Required evidence | Assumptions register path, row count, linked requirement status. |
| Review state | `Blocked` if expected assumptions are missing; otherwise `Needs review`. |
| Allowed actions | Regenerate outputs, inspect source input, or create a reviewer action to confirm no assumptions were generated. |
| Must not do | Do not treat missing assumptions as reviewed assumptions. |

## Blocked Rows

| Item | Requirement |
|---|---|
| Trigger | A row has missing required evidence, unresolved reviewer blocker, unsafe content, or invalid state transition. |
| Required message | This row cannot proceed to export until the blocker is resolved. |
| Required evidence | `Requirement_ID`, object type, blocker reason, corrective action, source artifact. |
| Review state | `Blocked` |
| Allowed actions | Correct input, revise reviewer note, exclude row from export, or return to `Needs review` after correction. |
| Must not do | Do not hide blocked rows from export summaries. |

## Stale Generated Outputs

| Item | Requirement |
|---|---|
| Trigger | Review log run marker does not match generated output marker, generated files are missing, or artifact counts disagree. |
| Required message | Generated outputs and review evidence may not describe the same run. |
| Required evidence | Run marker, artifact names, row counts, review-log marker. |
| Review state | `Blocked` for export readiness. |
| Allowed actions | Regenerate outputs, clear stale review evidence, or create a new review run marker. |
| Must not do | Do not combine review decisions from one run with artifacts from another run without explicit review. |

## Failed Publication Checks

| Item | Requirement |
|---|---|
| Trigger | Synthetic label missing, human-review note missing, restricted-detail check fails, or AI-approval wording check fails. |
| Required message | The package is not safe for portfolio use until publication blockers are resolved. |
| Required evidence | Failed checklist item, affected artifact, blocker reason, corrective action. |
| Review state | `Blocked` or `Needs review` depending on severity. |
| Allowed actions | Remove unsafe content, restore required label, restore human-review note, revise wording, or return package to review. |
| Must not do | Do not mark `Safe to publish` when any publication check fails. |

## Empty Export Package

| Item | Requirement |
|---|---|
| Trigger | Export package has no trace matrix, ambiguity report, assumptions register, review checklist, or run summary. |
| Required message | Export package is incomplete and cannot support review or portfolio proof. |
| Required evidence | Missing artifact list and output location. |
| Review state | `Blocked` |
| Allowed actions | Regenerate outputs or inspect run setup. |
| Must not do | Do not generate portfolio captures from incomplete package evidence. |

## Empty Review Log

| Item | Requirement |
|---|---|
| Trigger | Review log exists with headers only or no reviewer events. |
| Required message | No reviewer dispositions have been recorded yet. Generated findings remain decision-support artifacts only. |
| Required evidence | Review log path, event count, generated findings count. |
| Review state | Generated items remain `Needs review`. |
| Allowed actions | Begin reviewer disposition workflow or continue viewing generated findings. |
| Must not do | Do not derive `Reviewed demo`, `Export ready`, or `Safe to publish` from an empty review log. |

## Recovery Acceptance Criteria

An error or empty state is handled correctly when:

- The user can identify what failed or is missing.
- The user can identify the affected artifact.
- The user can identify the next reviewer or regeneration action.
- Export readiness is blocked when traceability is incomplete.
- Safe-to-publish status is blocked when publication checks fail.

