# Screenshot Capture Summary

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Capture Intent

This file is a screenshot-ready portfolio artifact for the deterministic lighting feasibility mini-simulator. It uses synthetic data only and represents feasibility screening, not design approval.

## Portfolio Panels

- Feasibility status count
- Thermal margin by synthetic case
- Current margin by synthetic case
- Summary table with review reasons

## Plot Assets

- `outputs/plots/thermal_margin_by_case.png`
- `outputs/plots/current_margin_by_case.png`
- `outputs/plots/feasibility_status_count.png`

## Status Counts

- Pass: 1
- Marginal: 2
- Fail: 2

## Summary Table

| Case | Status | Review Reason |
|---|---|---|
| SYN-LGT-001 | Pass | All deterministic synthetic feasibility checks are below marginal limits. |
| SYN-LGT-002 | Marginal | voltage headroom 0.19 V is 0.75 V or less |
| SYN-LGT-003 | Fail | boost duty 0.67 exceeds synthetic max 0.62 |
| SYN-LGT-004 | Marginal | driver case temperature ratio 0.90 is at or above 0.85; LED junction temperature ratio 0.93 is at or above 0.85; LED junction margin 9.2 C is 10 C or less |
| SYN-LGT-005 | Fail | driver case temperature ratio 1.08 exceeds 1.00; voltage headroom -0.32 V is below 0 V; driver thermal margin -10.3 C is below 0 C |

## Capture Notes

- Capture this Markdown and the PNG plots only after confirming the synthetic-data disclaimer remains visible.
- Do not crop out the human-review note in public portfolio screenshots.
- Keep any future UI screenshots synthetic and free of proprietary identifiers.
