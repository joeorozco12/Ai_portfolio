# Codex Tool Development Case Study

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Publication Classification

Needs review

## Problem

Applied AI engineering work can be hard to evaluate when it is shown only as prompts or broad claims. This case study demonstrates a controlled, reviewable workflow for using Codex to build engineering workflow tools with synthetic automotive lighting examples.

## Engineering Context

Jose Orozco builds Codex-assisted engineering workflow tools for automotive lighting and electrical engineering teams. The tools accelerate structured requirements, WCCA preparation, risk review, validation planning, and design-review readiness. AI assists the workflow. Engineers own final judgment.

This project uses only synthetic and sanitized examples. It does not include proprietary company, customer, supplier, schematic, requirement, program, validation, cost, BOM, harness, or internal document data.

## Workflow

1. Define the engineering workflow objective and safe-data boundary.
2. Scope Codex work to one project folder.
3. Create clear task prompts with protected file areas and expected outputs.
4. Generate draft artifacts using synthetic examples only.
5. Validate structure, required sections, safety language, and example outputs.
6. Keep engineering approval with the qualified human reviewer.

## Inputs

- [examples/safe_task_prompt.md](examples/safe_task_prompt.md)
- [examples/scope_control_example.md](examples/scope_control_example.md)
- [examples/validation_log_example.md](examples/validation_log_example.md)
- [examples/human_review_boundary.md](examples/human_review_boundary.md)

## Outputs

- [codex_workflow_case_study.md](codex_workflow_case_study.md)
- Synthetic task prompt example
- Scope-control example
- Validation-log example
- Human-review-boundary example
- [validation_checklist.md](validation_checklist.md)
- Synthetic capture artifacts in [captures](captures)

## Screenshots Or Capture Placeholders

- [captures/codex_task_prompt.md](captures/codex_task_prompt.md)
- [captures/scoped_file_tree.md](captures/scoped_file_tree.md)
- [captures/validation_log.md](captures/validation_log.md)
- [captures/human_review_boundary.md](captures/human_review_boundary.md)

## Sanitized Sample Data

All examples use generic automotive lighting workflow scenarios, such as synthetic requirements cleanup, WCCA preparation, risk register generation, and validation-planning review. Examples avoid real company names, customer names, supplier names, program identifiers, schematics, part numbers, proprietary limits, validation records, and internal file paths.

## Human Review Controls

- Treat Codex outputs as draft workflow artifacts.
- Confirm the task stayed inside the approved project folder.
- Confirm examples are synthetic or sanitized before publication.
- Review generated requirements, calculations, risk labels, validation plans, and conclusions before reuse.
- Do not represent Codex output as final engineering approval.

## Codex Contribution

Codex helps structure tasks, draft project files, generate repeatable examples, propose validation checks, and organize review artifacts.

## Jose Contribution

Jose defines the engineering workflow problem, constrains the data boundary, reviews Codex output, accepts or rejects changes, and owns final engineering judgment.

## AI Fundamentals Demonstrated

- Context engineering
- Prompt scoping
- Tool-use planning
- Code and artifact generation
- Validation planning
- Human-in-the-loop review

## Engineering Skills Demonstrated

- Engineering workflow decomposition
- Requirements and verification awareness
- WCCA preparation awareness
- Risk-review discipline
- Validation-planning discipline
- Technical communication for review packets

## Risks and Mitigations

- Risk: Codex may produce overbroad or unreviewed claims. Mitigation: use explicit project scope, required sections, and review gates.
- Risk: Public artifacts may drift toward proprietary details. Mitigation: use synthetic examples and sanitization checks.
- Risk: Generated outputs may imply approval. Mitigation: include human-review language and keep engineers responsible for final conclusions.

## Next Improvements

- Replace Markdown captures with reviewed image screenshots only if needed for a public page.
- Add a one-page visual workflow diagram.
- Add a short validation transcript from a future deterministic tool build.
- Add a reusable task-template library for portfolio-safe engineering workflows.

## Proof Gaps

- Captures are synthetic Markdown captures rather than live IDE or terminal screenshots.
- Final public copy still needs qualified review.
- No live walkthrough capture is included yet.

## Safe to Publish Status

Needs review. The case study uses synthetic content, but screenshots and final public wording still need qualified review before publication.
