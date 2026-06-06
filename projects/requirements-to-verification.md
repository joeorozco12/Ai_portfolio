# Requirements-to-Verification Tool Case Study

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Problem

Requirements-to-verification work often starts with incomplete language: notes from design discussions, partial functional descriptions, spreadsheet rows, and early validation ideas. The risk is not just formatting. Ambiguous requirements can move forward without clear verification intent, assumptions can be mixed with facts, and reviewers may miss gaps until late in the design cycle.

## Engineering Context

This case study uses a synthetic automotive lighting module with low beam, high beam, DRL dimming, diagnostics, input-voltage behavior, thermal review triggers, and traceability needs. It demonstrates a workflow pattern only. It does not contain restricted source material, nonpublic program data, internal identifiers, or real engineering documents.

## Workflow

1. Start from the sanitized input CSV reference.
2. Convert each row into a structured requirement object.
3. Classify subsystem, requirement type, verification method, risk level, and ambiguity status.
4. Preserve assumptions separately from verified facts.
5. Generate a draft traceability package and review checklist.
6. Require human review before any row is treated as accepted engineering output.

## Inputs

- Input CSV reference: [../Synthetic Requirements Sample.csv](../Synthetic%20Requirements%20Sample.csv)
- Planned rule inputs: verification-method dictionary, review-rule schema, and synthetic prompt/output log.
- Data boundary: synthetic automotive lighting examples only.

## Outputs

- Structured requirements table
- Verification trace matrix
- Ambiguity and open-question report
- Assumptions register
- Human-review checklist
- CSV and Markdown exports in [requirements-to-verification/generated_outputs](requirements-to-verification/generated_outputs)

## Screenshots or Screenshot Placeholders

- `before_messy_requirement_notes.png`: synthetic messy notes before structuring
- `generated_trace_matrix.png`: generated traceability matrix using synthetic rows
- `review_checklist_export.png`: reviewer checklist with draft status fields

## Sanitized Sample Data

The sample input file is [../Synthetic Requirements Sample.csv](../Synthetic%20Requirements%20Sample.csv). It uses generated IDs such as `SYN-REQ-001`, generic subsystem names, synthetic assumptions, and `Needs review` status. It is the only input CSV referenced by this Task 1 page.

## Sample Sanitized Output Description

The expected output is a draft verification package. For each synthetic input row, the package should show the requirement ID, normalized requirement text, subsystem, requirement type, proposed verification method, assumptions, ambiguity flag, proposed test or inspection, risk level, and human-review status. Ambiguous rows stay marked for review instead of being treated as approved requirements.

## Human Review Controls

- AI-generated outputs remain draft decision-support artifacts.
- A qualified engineer must verify requirement interpretation, verification-method mapping, assumptions, risk labels, and review status.
- Ambiguous or incomplete rows must be revised or escalated before inclusion in a design-review packet.
- Public artifacts must be checked against the sanitization rules before publishing.
- Final approval belongs to the engineer, not the AI tool.

## Codex Contribution

Codex contributes workflow scaffolding, parser and schema ideas, draft export formats, Markdown documentation, test-case suggestions, and review-checklist structure.

## Jose Contribution

Jose contributes the engineering taxonomy, lighting-domain framing, verification judgment, acceptance criteria, risk interpretation, review controls, and final approval decisions.

## AI Fundamentals Demonstrated

- Context engineering for constrained synthetic-data workflows
- Structured output generation from messy inputs
- Classification of requirement type and verification method
- Gap and ambiguity detection
- Human-in-the-loop governance
- Documentation automation

## Engineering Skills Demonstrated

- Requirements engineering
- Verification planning
- Traceability
- Risk and assumption capture
- Automotive lighting workflow awareness
- Engineering review discipline

## Risks and Mitigations

- Risk: AI may infer missing engineering intent. Mitigation: mark inferred content as draft and require engineer disposition.
- Risk: Trace matrices can imply completeness. Mitigation: include ambiguity flags, open questions, and review status.
- Risk: Public examples may drift toward restricted detail. Mitigation: use only synthetic source rows and run the sanitization checklist.

## Working Prototype

- Project folder: [requirements-to-verification/README.md](requirements-to-verification/README.md)
- CLI wrapper: [../tools/requirements_to_verification.py](../tools/requirements_to_verification.py)
- Generated outputs: [requirements-to-verification/generated_outputs](requirements-to-verification/generated_outputs)
- Mock captures: [requirements-to-verification/captures](requirements-to-verification/captures)

## Next Improvements

- Add a small Streamlit or static review UI mockup using synthetic data.
- Extend parser tests for configurable rule dictionaries.
- Replace Markdown mock captures with recreated synthetic screenshots if needed.
- Add reviewer signoff fields to the exported Markdown brief.

## Proof Gaps

- Screenshots are Markdown mock captures rather than browser or terminal image captures.
- Rule dictionaries are deterministic code constants rather than editable external config files.
- Final public review is still required.

## Safe to Publish Status

Needs review. This Markdown page uses synthetic content only, but it should not be published externally until screenshots and generated output samples are created from synthetic data and reviewed by a qualified engineer.
