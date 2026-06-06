# Requirements-to-Verification Usability Test Plan

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Purpose

This test plan checks whether the Project 1 UX lets a reviewer move from synthetic input to reviewable output to human decision point without confusion.

This plan tests workflow clarity only. It does not test visual design, branding, colors, icons, or UI polish.

## Participants

- Electrical engineer
- Design reviewer
- Validation engineer
- Portfolio interviewer

## Test Materials

- `generated_outputs/trace_matrix.csv`
- `generated_outputs/ambiguity_report.csv`
- `generated_outputs/assumptions_register.csv`
- `generated_outputs/review_checklist.csv`
- `generated_outputs/run_summary.md`
- UX docs in `projects/requirements-to-verification/ux/`

## Task 1: Find Why `SYN-REQ-004` Needs Review

| Item | Details |
|---|---|
| User goal | Determine why `SYN-REQ-004` is not ready for export. |
| Starting point | Reviewer dashboard. |
| Expected path | Dashboard -> requirement detail view -> ambiguity triage -> assumptions review. |
| Expected findings | Missing numeric limits, unclear owner, unclear pass/fail criteria, source ambiguity flag, linked assumptions `SYN-ASM-005`, `SYN-ASM-006`, and `SYN-ASM-007`. |
| Success criteria | Reviewer can explain what the tool detected, what remains unresolved, and which human action is required. |
| Failure signal | Reviewer thinks the tool approved the DRL requirement or cannot find the linked assumptions. |

## Task 2: Identify Unresolved Assumptions

| Item | Details |
|---|---|
| User goal | Find assumptions that require reviewer disposition. |
| Starting point | Reviewer dashboard or assumptions review screen. |
| Expected path | Dashboard -> assumptions panel -> requirement detail view. |
| Expected findings | Assumptions remain `Needs review` until accepted, revised, rejected, or escalated. |
| Success criteria | Reviewer can distinguish assumptions from confirmed requirement content. |
| Failure signal | Reviewer treats assumptions as verified facts. |

## Task 3: Determine Whether The Package Is Export-Ready

| Item | Details |
|---|---|
| User goal | Decide whether the generated package can be marked `Export ready`. |
| Starting point | Export summary. |
| Expected path | Export summary -> unresolved review counts -> ambiguity/assumption/mapping review. |
| Expected findings | Package remains `Needs review` while ambiguity findings and assumptions are unresolved. |
| Success criteria | Reviewer can identify blockers and explain that export readiness is not engineering approval. |
| Failure signal | Reviewer marks package export-ready without resolving required review gates. |

## Task 4: Determine Whether The Package Is Safe To Publish

| Item | Details |
|---|---|
| User goal | Decide whether the package can be used for portfolio or interview discussion. |
| Starting point | Safe-to-publish checklist. |
| Expected path | Safe-to-publish checklist -> export summary -> run summary. |
| Expected findings | Safe-to-publish status requires synthetic label, human-review note, restricted-detail screening, and AI-approval wording check. |
| Success criteria | Reviewer can explain why publication status is separate from export readiness. |
| Failure signal | Reviewer treats `Export ready` as `Safe to publish`. |

## Task 5: Trace One Requirement From Input To Review Decision

| Item | Details |
|---|---|
| User goal | Follow one requirement from source row to generated output to reviewer decision. |
| Starting point | Requirement table. |
| Expected path | Requirement table -> requirement detail view -> trace matrix review -> review-log action. |
| Expected findings | Every row-level item preserves `Requirement_ID`, source artifact, generated suggestion, and review state. |
| Success criteria | Reviewer can identify what came from input, what the tool inferred, and what the reviewer decided. |
| Failure signal | Reviewer cannot tell generated suggestions apart from reviewer decisions. |

## Observation Checklist

During each task, observe whether the participant can:

- Locate `Requirement_ID`.
- Find linked ambiguity findings.
- Find linked assumptions.
- Identify generated verification suggestions.
- Identify current review state.
- Identify next reviewer action.
- Explain why AI output is not approval.
- Explain whether export or publication is blocked.

## Passing Criteria

The UX passes this test plan when:

- At least four of five tasks are completed without moderator explanation.
- No participant interprets AI-generated suggestions as approval.
- Participants can distinguish `Needs review`, `Blocked`, `Export ready`, and `Safe to publish`.
- Participants can explain why `SYN-REQ-004` needs human review.
- Participants can identify the safest portfolio proof screens.

