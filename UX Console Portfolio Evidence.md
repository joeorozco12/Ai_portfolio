# UX Console Portfolio Evidence

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Problem

The portfolio proof tools existed as separate deterministic artifact packages, but the portfolio still needed visible workflow evidence that connected project inputs, review queues, artifacts, and publication gates in one coherent local UX.

## Engineering Context

The console uses only synthetic automotive lighting workflow examples from Projects 1, 2, 4, and 5. It does not show proprietary company, customer, supplier, program, schematic, BOM, harness, cost, validation, ticket, part-number, file-path, or internal document details.

## Workflow

Open [ux-console/index.html](ux-console/index.html), select a project route, inspect dashboard metrics, review queue items, indexed artifacts, and the publish gate. Reviewer decisions remain separate from generated deterministic outputs.

For interview QR use, publish `ux-console/` as the static site root and point the QR code to `/tools`. That route opens a browser-only public demo page with live synthetic demos for Requirements-to-Verification and Lighting Feasibility plus evidence dashboards for WCCA Prep and Design Review Readiness.

## Inputs

- Generated UX console data: [ux-console/data/portfolio_workflows.js](ux-console/data/portfolio_workflows.js)
- Project artifact packages from Requirements-to-Verification, WCCA Prep, Design Review Readiness, and Lighting Feasibility.
- Review-log template: [ux-console/review/review_log.csv](ux-console/review/review_log.csv)

## Outputs

- Unified local UX shell: [ux-console/index.html](ux-console/index.html)
- QR-ready tools route: [ux-console/tools/index.html](ux-console/tools/index.html)
- GitHub Pages deploy root: `ux-console/`
- Console screenshots: [ux-console/screenshots](ux-console/screenshots)
- Review validator: [tools/validate_ux_console_review.py](tools/validate_ux_console_review.py)

## Screenshots Or Screenshot Placeholders

- `portfolio_overview.png`
- `project1_requirements_to_verification.png`
- `project2_wcca_prep.png`
- `project4_design_review_readiness.png`
- `project5_lighting_feasibility.png`
- `mobile_project5_lighting_feasibility.png`

## Sanitized Sample Data

All visible examples are synthetic automotive lighting workflow rows, statuses, artifact names, and review states.

## Human Review Controls

- Every route keeps the synthetic/demo label and human-review note visible.
- `Export ready` is package-readiness only, not engineering approval.
- `Safe to publish` is blocked unless the review-log validator confirms the required publication checks.
- Screenshots remain `Needs review` until Jose explicitly approves publication.

## Codex Contribution

Codex implemented the static UX console, normalized console data generator, review-log validator, screenshot evidence pass, and tests.

## Jose Contribution

Jose defines the portfolio proof objective, project scope, review boundary, synthetic-data framing, and final publication decision.

## AI Fundamentals Demonstrated

- Structured data normalization
- Human-in-the-loop review-state design
- Deterministic validation
- Workflow UX prototyping

## Engineering Skills Demonstrated

- Requirements traceability review
- WCCA preparation review
- Design-review readiness organization
- Feasibility screening communication
- Portfolio-safe evidence packaging

## Risks And Mitigations

- Risk: a polished console could look like engineering approval. Mitigation: the review boundary and `Needs review` state stay visible on every route.
- Risk: screenshots may be mistaken for production tooling. Mitigation: the note frames the console as a local portfolio/workflow shell.
- Risk: publication status could be set accidentally. Mitigation: validator blocks unsafe `Export ready` and `Safe to publish` transitions.

## Next Improvements

- Deploy the GitHub Pages workflow and verify the public `/tools` route from a phone away from the Mac.
- Generate the final QR code only after the GitHub Pages URL is stable.
- Add real reviewer-disposition rows after Jose completes a review pass.
- Add final publication captions for each screenshot.

## Safe To Publish Status

Needs review.
