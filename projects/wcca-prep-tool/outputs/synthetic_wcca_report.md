# Synthetic WCCA Preparation Report

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Publication Classification

Needs review

## Executive Summary

This deterministic WCCA preparation report summarizes synthetic automotive lighting and LED-driver stress calculations. It is a pre-review engineering analysis aid and does not approve any engineering decision.

- Synthetic cases analyzed: 15
- Operating conditions analyzed: 4
- Case-condition calculation rows: 60
- Pass rows: 12
- Review rows: 26
- Fail rows: 22

## Input Summary

- Synthetic WCCA cases loaded: 15
- Synthetic operating conditions loaded: 4
- Calculation rows generated: 60
- Missing-data warnings generated: 3

## Assumptions

- All input data is synthetic or sanitized.
- Status thresholds are deterministic preparation thresholds, not final design-approval thresholds.
- Current tolerance and sense-resistor tolerance are applied as additive high-current contributors.
- VF tolerance is applied to the high-voltage LED-string corner.
- Switching-driver losses use low-corner efficiency.
- Linear-channel thermal loss uses positive voltage headroom only.

## Deterministic Derating Policy

- Ratio greater than 1.00: Over synthetic limit.
- Ratio from 0.80 to 1.00: Review required.
- Ratio below 0.80 with complete derating inputs: Within synthetic prep limit.
- Missing derating inputs: Review required.

## Status Summary

- Over synthetic limit: 22
- Review required: 26
- Within synthetic prep limit: 12

## Worst-Case Conditions

| Case | Worst Condition | Max Ratio | Margin pct | Pass/Fail Status | Review Status |
|---|---|---:|---:|---|---|
| SYN-WCCA-001 | SYN-OC-HIGHLOAD-HOT | 0.81 | 19.43 | Review | Review required |
| SYN-WCCA-002 | SYN-OC-HIGHLOAD-HOT | 0.87 | 13.31 | Review | Review required |
| SYN-WCCA-003 | SYN-OC-HIGHLOAD-HOT | 1.06 | -6.19 | Fail | Over synthetic limit |
| SYN-WCCA-004 | SYN-OC-HIGHLOAD-HOT | 1.62 | -62.02 | Fail | Over synthetic limit |
| SYN-WCCA-005 | SYN-OC-HIGHLINE-HOT | 1.11 | -11.04 | Fail | Over synthetic limit |
| SYN-WCCA-006 | SYN-OC-HIGHLOAD-HOT | 0.87 | 12.70 | Review | Review required |
| SYN-WCCA-007 | SYN-OC-HIGHLOAD-HOT | 1.18 | -17.64 | Fail | Over synthetic limit |
| SYN-WCCA-008 | SYN-OC-HIGHLOAD-HOT | 1.57 | -56.63 | Fail | Over synthetic limit |
| SYN-WCCA-009 | SYN-OC-HIGHLOAD-HOT | 0.84 | 15.52 | Review | Review required |
| SYN-WCCA-010 | SYN-OC-HIGHLINE-HOT | 0.96 | 4.47 | Review | Review required |
| SYN-WCCA-011 | SYN-OC-HIGHLOAD-HOT | 0.81 | 18.80 | Review | Review required |
| SYN-WCCA-012 | SYN-OC-HIGHLINE-HOT | 0.99 | 0.85 | Review | Review required |
| SYN-WCCA-013 | SYN-OC-HIGHLOAD-HOT | 0.89 | 11.40 | Review | Review required |
| SYN-WCCA-014 | SYN-OC-HIGHLOAD-HOT | 1.62 | -61.88 | Fail | Over synthetic limit |
| SYN-WCCA-015 | SYN-OC-HIGHLOAD-HOT | 1.03 | -3.30 | Fail | Over synthetic limit |

## Calculated Margins

Margins are calculated as `(1 - max stress ratio) * 100`. Negative margin means at least one synthetic preparation limit is exceeded.

| Case | Condition | Margin pct | Max Ratio | Status |
|---|---|---:|---:|---|
| SYN-WCCA-001 | SYN-OC-LOWLINE-HOT | 19.93 | 0.80 | Review |
| SYN-WCCA-001 | SYN-OC-NOMINAL | 33.27 | 0.67 | Pass |
| SYN-WCCA-001 | SYN-OC-HIGHLINE-HOT | 19.93 | 0.80 | Review |
| SYN-WCCA-001 | SYN-OC-HIGHLOAD-HOT | 19.43 | 0.81 | Review |
| SYN-WCCA-002 | SYN-OC-LOWLINE-HOT | 14.10 | 0.86 | Review |
| SYN-WCCA-002 | SYN-OC-NOMINAL | 27.44 | 0.73 | Pass |
| SYN-WCCA-002 | SYN-OC-HIGHLINE-HOT | 14.10 | 0.86 | Review |
| SYN-WCCA-002 | SYN-OC-HIGHLOAD-HOT | 13.31 | 0.87 | Review |
| SYN-WCCA-003 | SYN-OC-LOWLINE-HOT | -4.46 | 1.04 | Fail |
| SYN-WCCA-003 | SYN-OC-NOMINAL | 8.87 | 0.91 | Review |
| SYN-WCCA-003 | SYN-OC-HIGHLINE-HOT | -4.46 | 1.04 | Fail |
| SYN-WCCA-003 | SYN-OC-HIGHLOAD-HOT | -6.19 | 1.06 | Fail |
| SYN-WCCA-004 | SYN-OC-LOWLINE-HOT | -54.31 | 1.54 | Fail |
| SYN-WCCA-004 | SYN-OC-NOMINAL | -20.54 | 1.21 | Fail |
| SYN-WCCA-004 | SYN-OC-HIGHLINE-HOT | -9.98 | 1.10 | Fail |
| SYN-WCCA-004 | SYN-OC-HIGHLOAD-HOT | -62.02 | 1.62 | Fail |
| SYN-WCCA-005 | SYN-OC-LOWLINE-HOT | 30.00 | 0.70 | Pass |
| SYN-WCCA-005 | SYN-OC-NOMINAL | 22.08 | 0.78 | Pass |
| SYN-WCCA-005 | SYN-OC-HIGHLINE-HOT | -11.04 | 1.11 | Fail |
| SYN-WCCA-005 | SYN-OC-HIGHLOAD-HOT | 30.00 | 0.70 | Pass |
| SYN-WCCA-006 | SYN-OC-LOWLINE-HOT | 13.52 | 0.86 | Review |
| SYN-WCCA-006 | SYN-OC-NOMINAL | 26.86 | 0.73 | Pass |
| SYN-WCCA-006 | SYN-OC-HIGHLINE-HOT | 13.52 | 0.86 | Review |
| SYN-WCCA-006 | SYN-OC-HIGHLOAD-HOT | 12.70 | 0.87 | Review |
| SYN-WCCA-007 | SYN-OC-LOWLINE-HOT | -12.04 | 1.12 | Fail |
| SYN-WCCA-007 | SYN-OC-NOMINAL | 8.91 | 0.91 | Review |
| SYN-WCCA-007 | SYN-OC-HIGHLINE-HOT | -4.42 | 1.04 | Fail |
| SYN-WCCA-007 | SYN-OC-HIGHLOAD-HOT | -17.64 | 1.18 | Fail |
| SYN-WCCA-008 | SYN-OC-LOWLINE-HOT | -49.17 | 1.49 | Fail |
| SYN-WCCA-008 | SYN-OC-NOMINAL | -14.99 | 1.15 | Fail |
| SYN-WCCA-008 | SYN-OC-HIGHLINE-HOT | -4.31 | 1.04 | Fail |
| SYN-WCCA-008 | SYN-OC-HIGHLOAD-HOT | -56.63 | 1.57 | Fail |
| SYN-WCCA-009 | SYN-OC-LOWLINE-HOT | 16.21 | 0.84 | Review |
| SYN-WCCA-009 | SYN-OC-NOMINAL | 29.54 | 0.70 | Pass |
| SYN-WCCA-009 | SYN-OC-HIGHLINE-HOT | 16.21 | 0.84 | Review |
| SYN-WCCA-009 | SYN-OC-HIGHLOAD-HOT | 15.52 | 0.84 | Review |
| SYN-WCCA-010 | SYN-OC-LOWLINE-HOT | 22.78 | 0.77 | Pass |
| SYN-WCCA-010 | SYN-OC-NOMINAL | 24.34 | 0.76 | Pass |
| SYN-WCCA-010 | SYN-OC-HIGHLINE-HOT | 4.47 | 0.96 | Review |
| SYN-WCCA-010 | SYN-OC-HIGHLOAD-HOT | 22.42 | 0.78 | Pass |
| SYN-WCCA-011 | SYN-OC-LOWLINE-HOT | 19.34 | 0.81 | Review |
| SYN-WCCA-011 | SYN-OC-NOMINAL | 32.67 | 0.67 | Pass |
| SYN-WCCA-011 | SYN-OC-HIGHLINE-HOT | 19.34 | 0.81 | Review |
| SYN-WCCA-011 | SYN-OC-HIGHLOAD-HOT | 18.80 | 0.81 | Review |
| SYN-WCCA-012 | SYN-OC-LOWLINE-HOT | 9.24 | 0.91 | Review |
| SYN-WCCA-012 | SYN-OC-NOMINAL | 19.84 | 0.80 | Review |
| SYN-WCCA-012 | SYN-OC-HIGHLINE-HOT | 0.85 | 0.99 | Review |
| SYN-WCCA-012 | SYN-OC-HIGHLOAD-HOT | 8.90 | 0.91 | Review |
| SYN-WCCA-013 | SYN-OC-LOWLINE-HOT | 12.28 | 0.88 | Review |
| SYN-WCCA-013 | SYN-OC-NOMINAL | 25.62 | 0.74 | Pass |
| SYN-WCCA-013 | SYN-OC-HIGHLINE-HOT | 12.28 | 0.88 | Review |
| SYN-WCCA-013 | SYN-OC-HIGHLOAD-HOT | 11.40 | 0.89 | Review |
| SYN-WCCA-014 | SYN-OC-LOWLINE-HOT | -54.17 | 1.54 | Fail |
| SYN-WCCA-014 | SYN-OC-NOMINAL | -20.88 | 1.21 | Fail |
| SYN-WCCA-014 | SYN-OC-HIGHLINE-HOT | -34.22 | 1.34 | Fail |
| SYN-WCCA-014 | SYN-OC-HIGHLOAD-HOT | -61.88 | 1.62 | Fail |
| SYN-WCCA-015 | SYN-OC-LOWLINE-HOT | -1.71 | 1.02 | Fail |
| SYN-WCCA-015 | SYN-OC-NOMINAL | 11.62 | 0.88 | Review |
| SYN-WCCA-015 | SYN-OC-HIGHLINE-HOT | -1.71 | 1.02 | Fail |
| SYN-WCCA-015 | SYN-OC-HIGHLOAD-HOT | -3.30 | 1.03 | Fail |

## Calculation Results

| Case | Condition | Topology | Pout W | Iin A | Switch A | Max Ratio | Tj C | Status |
|---|---|---|---:|---:|---:|---:|---:|---|
| SYN-WCCA-001 | SYN-OC-LOWLINE-HOT | Buck LED Driver | 4.89 | 0.637 | 0.816 | 0.80 | 120.10 | Review required |
| SYN-WCCA-001 | SYN-OC-NOMINAL | Buck LED Driver | 4.89 | 0.424 | 0.816 | 0.67 | 100.10 | Within synthetic prep limit |
| SYN-WCCA-001 | SYN-OC-HIGHLINE-HOT | Buck LED Driver | 4.89 | 0.358 | 0.816 | 0.80 | 120.10 | Review required |
| SYN-WCCA-001 | SYN-OC-HIGHLOAD-HOT | Buck LED Driver | 5.14 | 0.669 | 0.857 | 0.81 | 120.86 | Review required |
| SYN-WCCA-002 | SYN-OC-LOWLINE-HOT | Buck LED Driver | 7.16 | 0.943 | 0.933 | 0.86 | 128.85 | Review required |
| SYN-WCCA-002 | SYN-OC-NOMINAL | Buck LED Driver | 7.16 | 0.629 | 0.933 | 0.73 | 108.85 | Within synthetic prep limit |
| SYN-WCCA-002 | SYN-OC-HIGHLINE-HOT | Buck LED Driver | 7.16 | 0.530 | 0.933 | 0.86 | 128.85 | Review required |
| SYN-WCCA-002 | SYN-OC-HIGHLOAD-HOT | Buck LED Driver | 7.52 | 0.990 | 0.979 | 0.87 | 130.04 | Review required |
| SYN-WCCA-003 | SYN-OC-LOWLINE-HOT | Boost LED Driver | 12.24 | 1.647 | 1.894 | 1.04 | 156.70 | Over synthetic limit |
| SYN-WCCA-003 | SYN-OC-NOMINAL | Boost LED Driver | 12.24 | 1.098 | 1.263 | 0.91 | 136.70 | Review required |
| SYN-WCCA-003 | SYN-OC-HIGHLINE-HOT | Boost LED Driver | 12.24 | 0.926 | 1.065 | 1.04 | 156.70 | Over synthetic limit |
| SYN-WCCA-003 | SYN-OC-HIGHLOAD-HOT | Boost LED Driver | 12.85 | 1.729 | 1.989 | 1.06 | 159.28 | Over synthetic limit |
| SYN-WCCA-004 | SYN-OC-LOWLINE-HOT | SEPIC LED Driver | 14.55 | 2.026 | 3.395 | 1.54 | N/A | Over synthetic limit |
| SYN-WCCA-004 | SYN-OC-NOMINAL | SEPIC LED Driver | 14.55 | 1.351 | 2.652 | 1.21 | N/A | Over synthetic limit |
| SYN-WCCA-004 | SYN-OC-HIGHLINE-HOT | SEPIC LED Driver | 14.55 | 1.140 | 2.420 | 1.10 | N/A | Over synthetic limit |
| SYN-WCCA-004 | SYN-OC-HIGHLOAD-HOT | SEPIC LED Driver | 15.28 | 2.127 | 3.564 | 1.62 | N/A | Over synthetic limit |
| SYN-WCCA-005 | SYN-OC-LOWLINE-HOT | Linear LED Channel | 4.01 | 0.594 | 0.371 | 0.70 | 105.00 | Within synthetic prep limit |
| SYN-WCCA-005 | SYN-OC-NOMINAL | Linear LED Channel | 4.01 | 0.396 | 0.371 | 0.78 | 116.88 | Within synthetic prep limit |
| SYN-WCCA-005 | SYN-OC-HIGHLINE-HOT | Linear LED Channel | 4.01 | 0.334 | 0.371 | 1.11 | 166.56 | Over synthetic limit |
| SYN-WCCA-005 | SYN-OC-HIGHLOAD-HOT | Linear LED Channel | 4.21 | 0.624 | 0.390 | 0.70 | 105.00 | Within synthetic prep limit |
| SYN-WCCA-006 | SYN-OC-LOWLINE-HOT | Buck LED Driver | 6.55 | 0.853 | 0.583 | 0.86 | 129.72 | Review required |
| SYN-WCCA-006 | SYN-OC-NOMINAL | Buck LED Driver | 6.55 | 0.568 | 0.583 | 0.73 | 109.72 | Within synthetic prep limit |
| SYN-WCCA-006 | SYN-OC-HIGHLINE-HOT | Buck LED Driver | 6.55 | 0.480 | 0.583 | 0.86 | 129.72 | Review required |
| SYN-WCCA-006 | SYN-OC-HIGHLOAD-HOT | Buck LED Driver | 6.88 | 0.895 | 0.612 | 0.87 | 130.95 | Review required |
| SYN-WCCA-007 | SYN-OC-LOWLINE-HOT | Boost LED Driver | 11.45 | 1.559 | 1.793 | 1.12 | 156.63 | Over synthetic limit |
| SYN-WCCA-007 | SYN-OC-NOMINAL | Boost LED Driver | 11.45 | 1.039 | 1.195 | 0.91 | 136.63 | Review required |
| SYN-WCCA-007 | SYN-OC-HIGHLINE-HOT | Boost LED Driver | 11.45 | 0.877 | 1.008 | 1.04 | 156.63 | Over synthetic limit |
| SYN-WCCA-007 | SYN-OC-HIGHLOAD-HOT | Boost LED Driver | 12.02 | 1.637 | 1.882 | 1.18 | 159.21 | Over synthetic limit |
| SYN-WCCA-008 | SYN-OC-LOWLINE-HOT | SEPIC LED Driver | 13.23 | 1.864 | 2.983 | 1.49 | 190.16 | Over synthetic limit |
| SYN-WCCA-008 | SYN-OC-NOMINAL | SEPIC LED Driver | 13.23 | 1.243 | 2.300 | 1.15 | 170.16 | Over synthetic limit |
| SYN-WCCA-008 | SYN-OC-HIGHLINE-HOT | SEPIC LED Driver | 13.23 | 1.049 | 2.086 | 1.04 | 190.16 | Over synthetic limit |
| SYN-WCCA-008 | SYN-OC-HIGHLOAD-HOT | SEPIC LED Driver | 13.89 | 1.957 | 3.133 | 1.57 | 194.42 | Over synthetic limit |
| SYN-WCCA-009 | SYN-OC-LOWLINE-HOT | Buck LED Driver | 6.88 | 0.885 | 0.765 | 0.84 | 125.69 | Review required |
| SYN-WCCA-009 | SYN-OC-NOMINAL | Buck LED Driver | 6.88 | 0.590 | 0.765 | 0.70 | 105.69 | Within synthetic prep limit |
| SYN-WCCA-009 | SYN-OC-HIGHLINE-HOT | Buck LED Driver | 6.88 | 0.498 | 0.765 | 0.84 | 125.69 | Review required |
| SYN-WCCA-009 | SYN-OC-HIGHLOAD-HOT | Buck LED Driver | 7.22 | 0.929 | 0.803 | 0.84 | 126.72 | Review required |
| SYN-WCCA-010 | SYN-OC-LOWLINE-HOT | Linear LED Channel | 0.82 | 0.121 | 0.131 | 0.77 | 115.83 | Within synthetic prep limit |
| SYN-WCCA-010 | SYN-OC-NOMINAL | Linear LED Channel | 0.82 | 0.081 | 0.131 | 0.76 | 113.49 | Within synthetic prep limit |
| SYN-WCCA-010 | SYN-OC-HIGHLINE-HOT | Linear LED Channel | 0.82 | 0.068 | 0.131 | 0.96 | 143.30 | Review required |
| SYN-WCCA-010 | SYN-OC-HIGHLOAD-HOT | Linear LED Channel | 0.86 | 0.127 | 0.137 | 0.78 | 116.37 | Within synthetic prep limit |
| SYN-WCCA-011 | SYN-OC-LOWLINE-HOT | Buck LED Driver | 4.32 | 0.569 | 0.641 | 0.81 | 120.99 | Review required |
| SYN-WCCA-011 | SYN-OC-NOMINAL | Buck LED Driver | 4.32 | 0.380 | 0.641 | 0.67 | 100.99 | Within synthetic prep limit |
| SYN-WCCA-011 | SYN-OC-HIGHLINE-HOT | Buck LED Driver | 4.32 | 0.320 | 0.641 | 0.81 | 120.99 | Review required |
| SYN-WCCA-011 | SYN-OC-HIGHLOAD-HOT | Buck LED Driver | 4.54 | 0.598 | 0.673 | 0.81 | 121.79 | Review required |
| SYN-WCCA-012 | SYN-OC-LOWLINE-HOT | Linear LED Channel | 0.11 | 0.018 | 0.033 | 0.91 | 113.45 | Review required |
| SYN-WCCA-012 | SYN-OC-NOMINAL | Linear LED Channel | 0.11 | 0.012 | 0.033 | 0.80 | 100.19 | Review required |
| SYN-WCCA-012 | SYN-OC-HIGHLINE-HOT | Linear LED Channel | 0.11 | 0.010 | 0.033 | 0.99 | 123.94 | Review required |
| SYN-WCCA-012 | SYN-OC-HIGHLOAD-HOT | Linear LED Channel | 0.12 | 0.019 | 0.035 | 0.91 | 113.87 | Review required |
| SYN-WCCA-013 | SYN-OC-LOWLINE-HOT | Boost LED Driver | 6.99 | 0.941 | 1.082 | 0.88 | 131.57 | Review required |
| SYN-WCCA-013 | SYN-OC-NOMINAL | Boost LED Driver | 6.99 | 0.627 | 0.721 | 0.74 | 111.57 | Within synthetic prep limit |
| SYN-WCCA-013 | SYN-OC-HIGHLINE-HOT | Boost LED Driver | 6.99 | 0.529 | 0.608 | 0.88 | 131.57 | Review required |
| SYN-WCCA-013 | SYN-OC-HIGHLOAD-HOT | Boost LED Driver | 7.34 | 0.988 | 1.136 | 0.89 | 132.90 | Review required |
| SYN-WCCA-014 | SYN-OC-LOWLINE-HOT | SEPIC LED Driver | 15.43 | 2.201 | 3.238 | 1.54 | 201.33 | Over synthetic limit |
| SYN-WCCA-014 | SYN-OC-NOMINAL | SEPIC LED Driver | 15.43 | 1.468 | 2.431 | 1.21 | 181.33 | Over synthetic limit |
| SYN-WCCA-014 | SYN-OC-HIGHLINE-HOT | SEPIC LED Driver | 15.43 | 1.238 | 2.178 | 1.34 | 201.33 | Over synthetic limit |
| SYN-WCCA-014 | SYN-OC-HIGHLOAD-HOT | SEPIC LED Driver | 16.21 | 2.311 | 3.400 | 1.62 | 206.14 | Over synthetic limit |
| SYN-WCCA-015 | SYN-OC-LOWLINE-HOT | Buck LED Driver | 9.01 | 1.212 | 0.875 | 1.02 | 152.57 | Over synthetic limit |
| SYN-WCCA-015 | SYN-OC-NOMINAL | Buck LED Driver | 9.01 | 0.808 | 0.875 | 0.88 | 132.57 | Review required |
| SYN-WCCA-015 | SYN-OC-HIGHLINE-HOT | Buck LED Driver | 9.01 | 0.682 | 0.875 | 1.02 | 152.57 | Over synthetic limit |
| SYN-WCCA-015 | SYN-OC-HIGHLOAD-HOT | Buck LED Driver | 9.46 | 1.273 | 0.918 | 1.03 | 154.95 | Over synthetic limit |

## Missing-Data Warning Summary

- SYN-WCCA-004: Thermal_Rise_C_per_W is missing; thermal rise is unavailable.
- SYN-WCCA-007: optional field LED_String_VF_Tol_pct is blank; default 0 used.
- SYN-WCCA-008: Max_Junction_Temp_C is missing; thermal derating is unavailable.

## Human Review Controls

- Treat all calculations as draft WCCA preparation output.
- Verify formulas, units, ratings, tolerance assumptions, and status labels.
- Confirm all data remains synthetic before public use.
- Do not use this output as approval for any engineering decision.

## Review Notes Placeholder

- Reviewer notes: _pending qualified engineering review_
- Open questions: _pending qualified engineering review_
- Required corrections: _pending qualified engineering review_

## Engineer Signoff Placeholder

| Field | Entry |
|---|---|
| Reviewer name |  |
| Review date |  |
| Review status | Needs review |
| Final engineering conclusion | Not approved by this tool |

## Proof Gaps

- Screenshots are mock captures until real screenshots are captured.
- Plot gallery requires qualified review before publication.
- Equation-review checklist is not completed.
- No reviewed signoff record is included yet.

## Safe to Publish Status

Needs review. This report uses synthetic data only, but the calculation approach and outputs require qualified engineering review before publication.
