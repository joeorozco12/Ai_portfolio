# Sanitization Rules

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## Rule Zero

Assume public portfolio material must be synthetic unless proven otherwise. Workflow patterns can be discussed. Proprietary content cannot be reproduced.

## Never Include

- Employer, customer, OEM, or supplier confidential documents
- Internal spec numbers, program names, ticket IDs, repo names, branch names, file paths, or part numbers
- Proprietary schematics, BOMs, harness files, CAD screenshots, validation data, or test reports
- Screenshots showing internal tools, folders, email, tickets, chats, or company systems
- Customer load tables, internal derating rules, internal WCCA values, or internal requirements
- Anything that implies AI approved an engineering decision

## Safe Substitutes

| Sensitive Item | Public Substitute |
|---|---|
| Real requirement | Synthetic requirement with generic ID |
| Real schematic | Block diagram drawn from scratch |
| Real BOM | Fake component table with generic functions only |
| Real WCCA case | Synthetic LED-driver case |
| Real test report | Demo report using generated data |
| Customer program | Generic automotive lighting module |
| Internal tool screenshot | Recreated screenshot using demo data |
| Internal calculation spreadsheet | Simplified synthetic workbook with made-up inputs |

## Publication Labels

- Safe to publish: synthetic, public-safe, no review concerns.
- Needs review: likely safe but requires human check before upload.
- Internal only: useful privately, not safe for public portfolio.
- Do not publish: contains or implies confidential details.

## Required Public Banner

> [SYNTHETIC — FOR DEMONSTRATION ONLY]

## Required Engineering Review Note

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Final Checklist

- [ ] No employer/customer/supplier/OEM names appear in technical examples.
- [ ] No internal IDs, file paths, screenshots, tickets, branches, or repo names appear.
- [ ] All data is synthetic, public, or sanitized.
- [ ] AI is described as decision support only.
- [ ] Jose contribution and Codex contribution are separated.
- [ ] Claims are evidence-backed or labeled as planned.
