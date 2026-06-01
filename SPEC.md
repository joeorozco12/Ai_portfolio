# SPEC.md — AI Engineering Portfolio Source Pack

[SYNTHETIC — FOR DEMONSTRATION ONLY]

## Product

A 20-file source pack for a custom work-account agent that can generate professional, sanitized AI engineering portfolio artifacts.

## User

Jose Orozco, Electrical Engineer building Codex-assisted tools for automotive engineering workflows.

## Goal

Create an agent-ready knowledge pack that communicates AI proficiency through evidence, skills maps, case-study templates, synthetic data, and strict sanitization rules.

## Non-Goals

- Do not publish confidential work examples.
- Do not imply AI approves engineering decisions.
- Do not build generic chatbot demos.
- Do not include internal employer, customer, supplier, schematic, BOM, harness, cost, validation, or requirements content.

## Scope

The source pack contains exactly 20 files so it can fit within a 20-file GPT knowledge upload limit:

1. AGENTS.md
2. SPEC.md
3. TASKS.md
4. Applied_AI_Engineering_Portfolio_Master.docx
5. Portfolio Evidence Matrix.xlsx
6. AI Fundamentals Map.md
7. Engineering Skills Map.md
8. Sanitization Rules.md
9. Human Review Required.md
10. Requirements-to-Verification README.md
11. WCCA Prep Tool README.md
12. Codex Case Study README.md
13. Design Review Assistant README.md
14. Lighting Feasibility Simulator README.md
15. AI Studio Bridge Demo README.md
16. Synthetic Requirements Sample.csv
17. Synthetic WCCA Sample.csv
18. Screenshot Index.md
19. Interview Story Bank.md
20. Resume LinkedIn Claims.md

## Functional Requirements

- FR-001: The agent shall identify AI fundamentals demonstrated by the portfolio materials.
- FR-002: The agent shall identify engineering skills demonstrated by the portfolio materials.
- FR-003: The agent shall generate public-safe artifacts using synthetic examples only.
- FR-004: The agent shall maintain a portfolio evidence matrix.
- FR-005: The agent shall produce a gap list for missing screenshots, plots, tests, diagrams, and demos.
- FR-006: The agent shall classify artifacts as Safe to publish, Needs review, Internal only, or Do not publish.
- FR-007: The agent shall separate Codex contribution from Jose contribution.
- FR-008: The agent shall include a human-review note in engineering artifacts.

## Quality Requirements

- QR-001: Outputs must be concise, technical, and interview-safe.
- QR-002: Claims must be evidence-backed or clearly labeled as planned.
- QR-003: Synthetic examples must be clearly labeled.
- QR-004: Public artifacts must avoid proprietary identifiers and internal details.
- QR-005: Every project README must follow the same structure.

## Data Boundary

Allowed:

- Synthetic automotive lighting requirements
- Synthetic WCCA parameters
- Generic engineering workflow descriptions
- Public-safe portfolio positioning
- Sanitized screenshots or recreated mockups

Not allowed:

- Employer/customer/OEM/supplier names in technical examples
- Internal file paths, repo names, ticket IDs, program codes, or requirement IDs
- Proprietary schematics, BOM rows, harness drawings, cost data, or validation data
- Screenshots of internal systems

## Success Criteria

The source pack is successful when an agent can generate:

- Portfolio evidence matrix
- AI fundamentals skills map
- Engineering skills map
- Six project case-study drafts
- Sanitization risk register
- Interview story bank
- Resume and LinkedIn claim drafts
- Gap list for remaining proof artifacts

## Standard Review Note

Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.
