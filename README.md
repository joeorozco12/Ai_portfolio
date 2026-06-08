# Applied AI Engineering Portfolio

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

Publication classification: Needs review

## Purpose

This repository contains Jose Orozco's public-safe applied AI engineering portfolio source pack and static interview console. The work demonstrates deterministic, Codex-assisted engineering workflow tools for synthetic automotive lighting examples.

Core message: AI accelerates engineering workflow execution. Engineers own final judgment.

## QR Web App

The public static console lives under [ux-console](ux-console). The QR route is:

```text
https://joeorozco12.github.io/Ai_portfolio/tools
```

The console is browser-only and does not require login, backend services, uploads, API keys, or live AI calls.

## Portfolio Tools

- Requirements-to-Verification Tool
- AI-Assisted WCCA Prep Tool
- Design Review Readiness Assistant
- Lighting Feasibility Mini-Simulator
- LED Datasheet-to-Model Extractor
- Codex Tool Development Case Study

All examples are synthetic or sanitized. Outputs remain `Needs review` until Jose completes and records a qualified review pass.

## Local Validation

Run the main validation checks from the repository root:

```bash
python3 tools/generate_ux_console_data.py --check
python3 -m unittest discover -s tests
python3 tools/validate_ux_console_review.py
python3 tools/validate_portfolio_toolbench.py
git diff --check
```

## Publication Boundary

Do not use this repository to publish proprietary employer, customer, supplier, OEM, program, schematic, BOM, harness, cost, internal test, internal requirement, ticket, part-number, or internal document details.

This portfolio does not claim that AI approves requirements, WCCA results, feasibility decisions, diagnostics, design readiness, validation strategy, or release decisions.
