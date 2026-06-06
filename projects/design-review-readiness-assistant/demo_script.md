# Project 4 Live Demo Script

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## 30-Second Explanation

Project 4 is a synthetic Codex-assisted workflow for automotive lighting design-review preparation. It takes structured synthetic review notes, generates a design-review packet, risk register, assumptions list, validation gaps, mode-to-test matrix, diagnostic response table, and screenshots, then validates that required schemas and human-review boundaries are present. The output is preparation support only. AI prepares review artifacts; qualified engineers own final decisions.

## 2-Minute Walkthrough

1. Open `inputs/synthetic_lighting_review_notes.md` and point out that the input is synthetic automotive lighting review content.
2. Run `python3 demo_project4.py`.
3. Show that the generator creates Markdown, CSV, and screenshot artifacts.
4. Show that the validator checks required files, CSV schemas, review-safe statuses, human-review language, reviewer placeholders, and screenshots.
5. Open `outputs/design_review_packet.md` to show the packet summary, risk links, assumptions, validation gaps, mode matrix preview, diagnostic response preview, and human-review controls.
6. Open `outputs/risk_register.csv` to show review-safe statuses and the human-review field.
7. Open `screenshots/dashboard_overview.png` or `screenshots/risk_register_export.png` as portfolio evidence.

## 5-Minute Technical Walkthrough

1. Explain the data boundary: all inputs are synthetic automotive lighting examples, with no proprietary company, customer, supplier, schematic, requirement, or internal document content.
2. Show how `scripts/generate_design_review_packet.py` parses the note table and maps review topics into deterministic outputs.
3. Show the generated CSV artifacts:
   - `outputs/risk_register.csv`
   - `outputs/mode_to_test_matrix.csv`
   - `outputs/diagnostic_response_table.csv`
4. Show the generated Markdown artifacts:
   - `outputs/design_review_packet.md`
   - `outputs/assumptions_list.md`
   - `outputs/validation_test_gaps.md`
   - `outputs/human_review_required.md`
5. Show `scripts/validate_project4_outputs.py` and explain that it checks README sections, required output files, CSV schemas, allowed statuses, human-review fields, reviewer placeholders, and screenshots.
6. Open one screenshot to show that the workflow produces visible portfolio evidence without exposing real engineering data.
7. Close by restating that this accelerates preparation, not approval or release.

## Expected Commands

From `projects/design-review-readiness-assistant/`:

```bash
python3 demo_project4.py
```

Direct validation commands:

```bash
python3 scripts/generate_design_review_packet.py
python3 scripts/validate_project4_outputs.py
python3 -m py_compile scripts/generate_design_review_packet.py scripts/validate_project4_outputs.py demo_project4.py
```

## Expected Output

```text
Project 4: Design Review Readiness Assistant
Synthetic Codex-assisted automotive lighting workflow demo...
Generated 8 risk rows from 8 synthetic notes.
Generated 7 mode-to-test rows.
Generated 8 diagnostic response rows.
Project 4 validation passed.
Demo completed successfully.
AI prepares review artifacts. Qualified engineers own final decisions.
```

## What To Open After Running The Demo

- `outputs/design_review_packet.md`
- `outputs/risk_register.csv`
- `outputs/mode_to_test_matrix.md`
- `outputs/diagnostic_response_table.md`
- `screenshots/dashboard_overview.png`
- `screenshots/risk_register_export.png`

## Interview-Safe Language

- “This is a synthetic workflow demonstration using automotive lighting examples.”
- “Codex helps generate structure, exports, validation checks, and evidence screenshots.”
- “The workflow organizes review preparation artifacts before human review.”
- “The validation script checks schemas and safety boundaries.”
- “AI prepares review artifacts. Qualified engineers own final decisions.”

## What Not To Claim

- Do not claim AI approves design readiness.
- Do not claim AI signs off requirements, validation plans, diagnostic strategy, or engineering release.
- Do not claim the synthetic examples represent real company, customer, supplier, schematic, requirement, or internal document content.
- Do not claim the generated statuses are final engineering conclusions.
- Do not present screenshots as evidence of completed validation.
