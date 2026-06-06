# Human Review Controls

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Tool Role

The Lighting Feasibility Mini-Simulator accelerates first-pass screening of synthetic automotive lighting examples. It can flag cases where simple electrical or thermal estimates suggest a candidate is feasible, marginal, or outside a synthetic limit.

The tool does not approve engineering decisions. AI and Codex can accelerate workflow execution by generating code, outputs, plots, and test scaffolds, but engineers own final judgment, assumptions, review, and approval.

## What The Tool Can Flag

- LED string voltage high and low corners based on synthetic tolerance inputs.
- Worst-case LED current based on synthetic current tolerance.
- Output power against a synthetic output-power limit.
- Input current at minimum supply against a synthetic current limit.
- Input voltage against a synthetic voltage rating.
- Non-boost voltage headroom concerns.
- Boost duty-cycle concerns.
- Driver case temperature margin using a simple thermal resistance assumption.
- LED junction temperature margin using a simple thermal resistance assumption.
- Pass, Marginal, or Fail status based on deterministic thresholds.

## What Engineers Must Review Manually

- Whether the equations are appropriate for the intended demonstration.
- Whether the input values are synthetic and public-safe.
- Whether each limit, rating, tolerance, and threshold is technically reasonable.
- Whether thermal resistance assumptions are directionally useful.
- Whether the selected topology is compatible with the synthetic LED string and supply range.
- Whether additional design constraints are missing, including optics, diagnostics, EMC, transients, dimming, aging, tolerance stackup, mechanical packaging, material limits, and reliability.
- Whether any output wording could be misread as design approval.
- Whether plots and screenshots show only synthetic data.

## Assumptions

- LED forward voltage and current tolerances are represented by simple percentage corners.
- Switching drivers use a low-corner efficiency estimate for input-power screening.
- Linear channel loss uses maximum supply and low LED voltage as a conservative heat corner.
- LED power is assumed to split evenly across the synthetic LED count.
- Driver and LED temperatures use lumped thermal resistance values.
- Thresholds are demonstration values, not company, regulatory, or program criteria.
- Generated plots are explanatory portfolio artifacts, not validated engineering plots.

## Risks

- A viewer may mistake a `Pass` result for approval. Mitigation: every artifact includes the human-review note and explains feasibility-only scope.
- Synthetic thresholds may appear more authoritative than intended. Mitigation: thresholds are labeled as synthetic and review-required.
- Simple thermal models can hide layout or material effects. Mitigation: thermal outputs are treated as flags for deeper analysis.
- Missing constraints can create false confidence. Mitigation: README and docs list excluded analyses.
- Portfolio screenshots can accidentally omit safety disclaimers. Mitigation: screenshot capture notes require the synthetic and human-review labels to stay visible.

## Validation Needs

- Equation review by a qualified engineer.
- Threshold review against the intended public demonstration scope.
- Unit tests for pass, marginal, fail, parsing, and CSV output schema.
- Regeneration check for Markdown, CSV, plots, and screenshot-ready outputs.
- Sanitization review before public use.
- Visual review of PNG plot readability.

## Release Controls

Before publishing any Project 5 artifact:

- Confirm it includes `[SYNTHETIC — FOR DEMONSTRATION ONLY]`.
- Confirm it includes the human-review note.
- Confirm it avoids proprietary organizations, programs, drawings, requirements, file paths, part numbers, costs, validation data, and controlled source documents.
- Confirm no result implies AI approval or final engineering signoff.
- Confirm the publication classification remains `Needs review` until reviewed.

## Safe To Publish Status

Needs review. The content is synthetic, but the equations, thresholds, outputs, screenshots, and claims require qualified engineering review before publication.
