# Requirements-to-Verification Tool

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Project README Section

Codex-assisted engineering workflow that converts synthetic automotive-lighting requirement notes into a reviewable requirements-to-verification matrix. The tool drafts requirement IDs, subsystem labels, verification methods, ambiguity flags, assumptions, risk levels, and review status for engineer review.

- Portfolio role: Priority proof spine item 1
- Working prototype: [projects/requirements-to-verification/README.md](projects/requirements-to-verification/README.md)
- Case study page: [projects/requirements-to-verification.md](projects/requirements-to-verification.md)
- Sample input CSV: [Synthetic Requirements Sample.csv](Synthetic%20Requirements%20Sample.csv)
- Publication classification: Needs review

## Status

Working deterministic prototype added for Project 1. Public publication still needs qualified human review of generated outputs and capture files.

## Problem

Engineering requirements often arrive as paragraphs, tables, screenshots, meeting notes, and partial test-plan fragments. Manual consolidation creates risk: missed verification hooks, ambiguous wording, duplicated requirements, and weak traceability.

## Engineering Context

Synthetic automotive lighting module with low beam, high beam, DRL dimming, diagnostics, input voltage limits, thermal behavior, and review gates. The public example uses generated data only.

## Workflow

1. Load synthetic requirement rows or notes.
2. Normalize text into candidate requirements with stable IDs.
3. Classify subsystem, requirement type, and proposed verification method.
4. Flag ambiguity, missing assumptions, and review risks.
5. Export trace matrix, unresolved-questions list, and human-review checklist.
6. Require qualified engineer review before any artifact is treated as accepted.

## Inputs

- [Synthetic Requirements Sample.csv](Synthetic%20Requirements%20Sample.csv): sanitized source CSV used by the portfolio example.
- Deterministic rules in [projects/requirements-to-verification/requirements_to_verification/core.py](projects/requirements-to-verification/requirements_to_verification/core.py) for inspection, analysis, demonstration, test, review, ambiguity flags, and human-review status.
- Optional prompt log: synthetic prompt/output transcript only, with no restricted source details.

## Sample Sanitized Input CSV Reference

The current sample input file is [Synthetic Requirements Sample.csv](Synthetic%20Requirements%20Sample.csv). It contains generated rows only and uses generic IDs such as `SYN-REQ-001`.

Required columns:

- `Requirement_ID`
- `Source_Type`
- `Requirement_Text`
- `Subsystem`
- `Requirement_Type`
- `Verification_Method`
- `Risk_Level`
- `Assumptions`
- `Ambiguity_Flag`
- `Proposed_Test`
- `Human_Review_Status`

## Outputs

- Requirements table with stable synthetic IDs and normalized requirement text.
- Verification trace matrix connecting each requirement to verification method, proposed test or inspection, risk, assumptions, and review status.
- Risk and assumptions register separating generated assumptions from verified facts.
- Ambiguity report listing vague wording, missing thresholds, and items requiring engineer disposition.
- Markdown review brief summarizing open questions and publish-readiness gaps.
- CSV and Markdown exports in [projects/requirements-to-verification/generated_outputs](projects/requirements-to-verification/generated_outputs).

## Sample Sanitized Output Description

For the sample CSV, the output should be a draft traceability package. A representative output row would preserve `SYN-REQ-004`, classify it under DRL functional behavior, propose `Analysis + Test`, carry forward the synthetic assumption about configurable current reduction, flag the row as ambiguous, and leave `Human_Review_Status` as `Needs review`.

## Screenshot Placeholders

- before_messy_requirement_notes.png
- generated_trace_matrix.png
- review_checklist_export.png

## Sanitized Sample Data

Use [Synthetic Requirements Sample.csv](Synthetic%20Requirements%20Sample.csv) as the input reference. Public examples must remain synthetic and must avoid restricted source material, nonpublic program data, internal identifiers, and real engineering documents.

## Human Review Controls

Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Review checkpoints:

- Confirm all inputs are synthetic or sanitized.
- Confirm AI-proposed classifications are reviewed and either accepted, revised, rejected, or escalated.
- Confirm calculations, formulas, limits, and pass/review labels are verified by an engineer.
- Confirm ambiguous requirements remain blocked from final design-review packets until dispositioned.
- Confirm output is marked as draft until approved by a qualified engineer.

## Codex Contribution vs Jose Contribution

### Codex Contribution

Codex helps create parsing utilities, schema definitions, tests, export formatting, README content, and review-checklist generation.

### Jose Contribution

Jose defines the engineering taxonomy, decides acceptable verification mappings, reviews every AI-proposed classification, and owns final interpretation.

## AI Fundamentals Demonstrated

- Context engineering for messy engineering inputs
- Structured output generation
- Classification of requirement type and verification method
- Gap detection draft
- Documentation scaffolding

## Engineering Skills Demonstrated

- Requirements engineering
- Verification planning
- Traceability
- Risk and assumption capture
- Automotive lighting workflow awareness

## Risks and Mitigations

- AI may over-classify vague requirements. Mitigation: require uncertainty field and human approval.
- Synthetic data may be too clean. Mitigation: include ambiguous and conflicting examples.
- Traceability can imply false completeness. Mitigation: include gap count and review status.
- Public artifacts may accidentally include restricted context. Mitigation: use synthetic source files only and run the sanitization checklist before publication.

## Proof Gaps

- Replace screenshot placeholders with recreated UI screenshots using synthetic data only.
- Add a generated sample traceability output file after the schema is finalized.
- Add a short parser/test transcript showing deterministic checks on the CSV columns.
- Complete final human review before publishing externally.

## Next Improvements

- Add optional Streamlit or static HTML review UI after CLI evidence is reviewed.
- Add more parser tests for configurable rule dictionaries.
- Add real screenshot pair if the static capture files are not enough for the portfolio page.
- Add short demo video using synthetic data after reviewer signoff.
- Add reviewer signoff fields to the exported review brief.

## Safe to Publish Status

Needs review. The written content and sample CSV are synthetic, but the public page should not be published until screenshot placeholders are replaced with public-safe images and a qualified reviewer confirms the output package contains no restricted content.
