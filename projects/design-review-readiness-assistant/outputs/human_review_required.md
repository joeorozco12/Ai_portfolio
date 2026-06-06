# Human Review Required Section

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Preparation-Only Boundary

This section is included in every Project 4 design-review preparation output. It states that AI-generated packets, risks, assumptions, gaps, and agenda items are not engineering approvals.

## Problem

AI-assisted preparation artifacts can look authoritative unless review ownership and draft status are explicit.

## Engineering Context

This section applies to the synthetic automotive lighting design-review readiness assistant and all generated Project 4 outputs.

## Workflow

1. Generate draft outputs from synthetic notes.
2. Validate that required labels and risk-register fields are present.
3. Route outputs to a qualified engineer.
4. Record reviewer disposition only after human review.

## Inputs

- `inputs/synthetic_lighting_review_notes.md`

## Outputs

- Required human-review language for generated Project 4 artifacts.

## Screenshots Or Screenshot Placeholders

- `screenshots/risk_register_export.png`: generated synthetic risk register mockup.

## Sanitized Sample Data

This section uses placeholder reviewer fields only.

## Required Review Statement

AI-generated outputs in this project are draft decision-support artifacts. They may help organize notes, identify candidate risks, separate assumptions from facts, and list missing evidence. They do not approve requirements, electrical designs, calculations, validation plans, test results, risk closures, release decisions, or design readiness.

## Reviewer Disposition Checklist

| Check | Reviewer | Disposition | Engineering Decision | Evidence / Rationale | Date Reviewed |
| --- | --- | --- | --- | --- | --- |
| Input data is synthetic or sanitized. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |
| Risk statements are technically meaningful. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |
| Severity and likelihood labels are reviewed. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |
| Assumptions are separated from verified facts. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |
| Validation/test gaps are correctly scoped. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |
| Screenshots are generated from synthetic data. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |
| Publication classification is confirmed. | TBD - qualified engineer | Pending review | No engineering decision - preparation artifact only | Synthetic evidence pending | YYYY-MM-DD |

## Human Review Controls

- Keep all outputs at `Needs review` until a qualified engineer reviews them.
- Do not present draft readiness as design approval.
- Do not treat AI-generated severity, likelihood, or mitigation labels as accepted engineering judgment.
- Do not include proprietary employer, customer, supplier, program, schematic, BOM, harness, cost, internal test, internal requirement, ticket, part-number, or internal file-path details.

## Codex Contribution

Codex generates this review-control section and validates that the risk register keeps human review visible.

## Jose Contribution

Jose defines the review boundary and owns the final decision on publication and engineering interpretation.

## AI Fundamentals Demonstrated

- Governance prompt design
- Validation of required safety language
- Human-in-the-loop workflow design

## Engineering Skills Demonstrated

- Engineering governance
- Technical review discipline
- Public-safe documentation

## Risks And Mitigations

- Risk: Readers may infer signoff from a clean packet. Mitigation: use explicit preparation-only and review-required language.

## Next Improvements

- Add a reviewer signoff template after qualified review.
- Add a validation test for reviewer field completeness.

## Safe To Publish Status

Needs review. This section is synthetic and public-safe by design, but it is still pending final reviewer disposition.

## Proof Gaps

- Reviewer name and date are not filled in.
- Publication classification has not been independently confirmed.
