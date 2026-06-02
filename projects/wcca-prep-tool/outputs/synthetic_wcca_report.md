# Synthetic WCCA Preparation Report

[SYNTHETIC -- FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Publication Classification

Needs review

## Input Summary

- Synthetic WCCA cases loaded: 8
- Synthetic operating conditions loaded: 4
- Calculation rows generated: 32
- Missing-data warnings generated: 3

## Deterministic Derating Policy

- Ratio greater than 1.00: Over synthetic limit.
- Ratio from 0.80 to 1.00: Review required.
- Ratio below 0.80 with complete derating inputs: Within synthetic prep limit.
- Missing derating inputs: Review required.

## Status Summary

- Over synthetic limit: 15
- Review required: 11
- Within synthetic prep limit: 6

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

## Missing-Data Warning Summary

- SYN-WCCA-004: Thermal_Rise_C_per_W is missing; thermal rise is unavailable.
- SYN-WCCA-007: optional field LED_String_VF_Tol_pct is blank; default 0 used.
- SYN-WCCA-008: Max_Junction_Temp_C is missing; thermal derating is unavailable.

## Human Review Controls

- Treat all calculations as draft WCCA preparation output.
- Verify formulas, units, ratings, tolerance assumptions, and status labels.
- Confirm all data remains synthetic before public use.
- Do not use this output as approval for any engineering decision.

## Proof Gaps

- No screenshots are included yet.
- No plots are included yet.
- No equation-review checklist is included yet.
- No reviewed signoff record is included yet.

## Safe to Publish Status

Needs review. This report uses synthetic data only, but the calculation approach and outputs require qualified engineering review before publication.
