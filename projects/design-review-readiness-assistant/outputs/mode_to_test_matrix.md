# Synthetic Mode-To-Test Matrix

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Preparation-Only Boundary

This matrix is a draft design-review preparation artifact. It makes synthetic lighting-mode behavior, verification needs, required evidence, and related risks easier to inspect before human review. It does not approve mode behavior, verification coverage, validation results, or design readiness.

## Problem

Lighting-mode behavior can be difficult to review when mode inputs, expected outputs, and required evidence are scattered across notes.

## Engineering Context

The matrix uses generated automotive-lighting mode examples only: low beam, high beam, DRL, park lamp, turn signal, welcome animation, and fault safe-state behavior.

## Workflow

1. Parse synthetic review notes.
2. Map review topics into draft mode-to-test rows.
3. Link each mode to a candidate risk.
4. Keep all rows at review-safe status until a qualified engineer reviews them.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- `outputs/mode_to_test_matrix.csv`
- `outputs/mode_to_test_matrix.md`

## Screenshots Or Screenshot Placeholders

- `screenshots/mode_to_test_matrix.png`: generated synthetic matrix mockup.

## Sanitized Sample Data

All rows use generated `SYN-MODE-*` IDs and synthetic lighting-mode behavior.

## Mode-To-Test Matrix

| Mode ID | Mode Name | Input Condition | Expected Output | Verification Method | Required Evidence | Related Risk ID | Status | Human Review Required | Publication Classification | Synthetic Data Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYN-MODE-001 | Low Beam | Low beam command active with generic nominal input voltage. | Low beam output is commanded on; other lighting modes remain governed by their command state. | Synthetic bench functional test | Mode-command log and synthetic output-state capture. | SYN-DRR-R001 | Needs review | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |
| SYN-MODE-002 | High Beam | High beam command active with low beam state recorded for traceability. | High beam output is commanded on according to the synthetic command table. | Synthetic command truth-table test | Command matrix row and output-state capture. | SYN-DRR-R001 | Needs review | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |
| SYN-MODE-003 | DRL | Daytime running lamp command active and full-intensity command inactive. | DRL output uses a reduced-current demo target that remains pending engineer definition. | Analysis plus synthetic bench check | Demo current target, command log, and current-measurement placeholder. | SYN-DRR-R003 | Open | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |
| SYN-MODE-004 | Park Lamp | Park lamp command active with main forward-lighting commands inactive. | Park lamp output is commanded on at a synthetic demonstration level. | Synthetic functional inspection | Command-state capture and output-state checklist. | SYN-DRR-R001 | Needs review | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |
| SYN-MODE-005 | Turn Signal | Turn command active with a generic periodic command profile. | Turn output follows the synthetic on/off command profile. | Synthetic timing observation | Timing trace placeholder and output-state capture. | SYN-DRR-R001 | Needs review | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |
| SYN-MODE-006 | Welcome Animation | Synthetic welcome-event trigger active while vehicle state permits demo animation. | Sequence follows a public-safe synthetic animation step list. | Synthetic sequence inspection | Step list, timing notes, and screen capture placeholder. | SYN-DRR-R007 | Mitigation proposed | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |
| SYN-MODE-007 | Fault / Safe State | Synthetic diagnostic fault active for the selected channel. | Affected output enters the configured demo safe state while the review packet records the open diagnostic disposition. | Synthetic fault injection checklist | Fault injection row, response log, and reviewer disposition. | SYN-DRR-R005 | Open | Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval. | Needs review | [SYNTHETIC — FOR DEMONSTRATION ONLY] |

## Reviewer Disposition Fields

| Reviewer | Disposition | Engineering Decision | Evidence / Rationale | Date Reviewed |
| --- | --- | --- | --- | --- |
| TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |

## Human Review Controls

- A qualified engineer must review each expected output, verification method, evidence request, and risk link.
- Draft mode rows are preparation prompts, not approved requirements or accepted validation coverage.
- Any final mode behavior or test procedure must be reviewed separately under controlled engineering processes.

## Codex Contribution

Codex generates the draft matrix and links mode rows to synthetic risks.

## Jose Contribution

Jose defines which mode behaviors and evidence requests are meaningful for engineering review and owns final judgment.

## AI Fundamentals Demonstrated

- Structured extraction
- Traceability mapping
- Review-safe output generation

## Engineering Skills Demonstrated

- Mode behavior review
- Verification planning
- Traceability

## Risks And Mitigations

- Risk: Mode rows may look like accepted requirements. Mitigation: keep status as `Needs review`, `Open`, or `Mitigation proposed` and require engineer review.

## Next Improvements

- Add reviewer disposition capture.
- Add linkage from each mode row to validation gap closure status.

## Safe-to-Publish Status

Needs review. This matrix uses synthetic data only. Engineering review and final validation remain outside this artifact.

## Proof Gaps

- Reviewer disposition is not complete.
- No final validation evidence is attached.
