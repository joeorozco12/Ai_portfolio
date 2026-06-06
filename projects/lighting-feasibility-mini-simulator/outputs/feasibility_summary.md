# Automotive Lighting Feasibility Mini-Simulator Summary

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

Early lighting feasibility discussions need quick estimates for LED electrical load, driver stress, and thermal margin without presenting the result as design approval.

## Engineering Context

The engine screens synthetic automotive lighting load cases using first-pass LED string, driver input, voltage headroom, boost duty, and thermal equations.

## Workflow

- Load synthetic input parameters from CSV.
- Calculate worst-case LED string voltage, current, power, driver loss, and temperature estimates.
- Apply deterministic Pass, Marginal, or Fail logic.
- Export markdown and CSV summaries for human review.

## Inputs

- Input CSV: `data/synthetic_lighting_cases.csv`
- Parameters: LED count, LED forward voltage, current, supply range, topology, efficiency, ratings, thermal resistance, and ambient temperature.

## Outputs

- Feasibility status by synthetic case.
- Electrical and thermal calculated values.
- Review reason and recommended next step.
- PNG plot assets under `outputs/plots/`.
- Screenshot-ready capture notes under `outputs/screenshots/`.
- Sensitivity sweep outputs under `outputs/sensitivity/`.

## Screenshots or Screenshot Placeholders

- `outputs/screenshots/portfolio_capture_summary.md`
- `outputs/plots/thermal_margin_by_case.png`
- `outputs/plots/current_margin_by_case.png`
- `outputs/plots/feasibility_status_count.png`

## Sanitized Sample Data

All case IDs, load names, limits, ratings, and assumptions are synthetic demonstration values. No proprietary organization, program, part, drawing, BOM, harness, cost, validation, controlled source, or restricted design details are included.

## Human Review Controls

- Confirm all inputs are synthetic before public use.
- Verify formulas, units, thresholds, and assumptions before using the output in any engineering discussion.
- Treat Pass as a first-pass screen only, not an engineering approval.
- Escalate Marginal and Fail rows to detailed analysis with reviewed assumptions.

## Codex Contribution

Codex scaffolded the deterministic Python engine, sample CSV, output writers, and basic tests.

## Jose Contribution

Jose defines acceptable first-pass screening equations, engineering interpretation, and final review criteria.

## AI Fundamentals Demonstrated

- Deterministic code generation
- Structured data transformation
- Rule-based classification
- Test generation
- Report generation

## Engineering Skills Demonstrated

- LED load estimation
- Driver power and current screening
- Voltage headroom review
- Boost duty-cycle screening
- Thermal margin estimation

## Risks and Mitigations

- Risk: The simulator could be mistaken for final approval. Mitigation: every output states human review is required.
- Risk: Generic assumptions may not match a real design. Mitigation: use synthetic data only and keep formulas transparent.
- Risk: Marginal cases may be overinterpreted. Mitigation: recommend detailed analysis before design decisions.

## Next Improvements

- Add cross-variable sensitivity sweeps after single-variable behavior is reviewed.
- Add reviewed equation annotations from a qualified engineer.
- Add an optional Streamlit shell after equation review.

## Safe to Publish Status

Needs review. The data is synthetic, but formulas, limits, thresholds, screenshots, and claims require qualified engineering review before publication.

## Deterministic Feasibility Policy

- Fail: any calculated ratio exceeds 1.00, voltage headroom is below 0 V, boost duty exceeds the synthetic maximum, or thermal margin is below 0 C.
- Marginal: any calculated ratio is at least 0.85, voltage headroom is 0.75 V or less, boost duty is at least 85% of the synthetic maximum, or thermal margin is 10 C or less.
- Pass: no fail or marginal triggers are present.

## Status Summary

- Pass: 1
- Marginal: 2
- Fail: 2

## Calculation Results

| Case | Load | Topology | Pout W | Iin @ Min V A | Headroom V | Boost Duty | Driver C | LED Tj C | Max Ratio | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| SYN-LGT-001 | Synthetic two-LED DRL segment | Buck LED Driver | 1.85 | 0.236 | 1.70 | N/A | 89.9 | 108.2 | 0.80 | Pass |
| SYN-LGT-002 | Synthetic three-LED signature | Buck LED Driver | 2.23 | 0.284 | 0.19 | N/A | 90.8 | 99.9 | 0.74 | Marginal |
| SYN-LGT-003 | Synthetic long-string signal | Boost LED Driver | 11.58 | 1.593 | N/A | 0.67 | 122.6 | 128.1 | 1.00 | Fail |
| SYN-LGT-004 | Synthetic hot-compartment marker | Buck LED Driver | 2.32 | 0.301 | 1.90 | N/A | 112.1 | 125.8 | 0.93 | Marginal |
| SYN-LGT-005 | Synthetic linear accent channel | Linear LED Channel | 2.78 | 0.315 | -0.32 | N/A | 135.3 | 123.5 | 1.08 | Fail |

## Review Reasons

- SYN-LGT-001: All deterministic synthetic feasibility checks are below marginal limits.
- SYN-LGT-002: voltage headroom 0.19 V is 0.75 V or less
- SYN-LGT-003: boost duty 0.67 exceeds synthetic max 0.62
- SYN-LGT-004: driver case temperature ratio 0.90 is at or above 0.85; LED junction temperature ratio 0.93 is at or above 0.85; LED junction margin 9.2 C is 10 C or less
- SYN-LGT-005: driver case temperature ratio 1.08 exceeds 1.00; voltage headroom -0.32 V is below 0 V; driver thermal margin -10.3 C is below 0 C

## Warnings

- No input warnings were generated.

## Proof Gaps

- Equation set has not yet been independently reviewed.
- PNG plots are generated from synthetic data but have not been design-reviewed.
- Screenshot-ready Markdown is included, but no live UI screenshot exists yet.
- No Streamlit UI is included yet.
- No reviewed signoff record is included yet.
