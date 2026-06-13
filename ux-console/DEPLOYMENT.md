# QR Deployment Notes

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Static Deploy Root

Publish the `ux-console/` directory as the static site root.

The printed QR code should point to:

```text
https://joeorozco12.github.io/Ai_portfolio/tools
```

The `/tools` route is a static shim that opens `index.html#tools`. Deep links are available for:

- `/tools/requirements`
- `/tools/feasibility`
- `/tools/wcca`
- `/tools/design-review`
- `/tools/evidence`

## GitHub Pages Deploy

Use the repository workflow at `.github/workflows/deploy-ux-console.yml`.

The workflow runs on pushes to `main` and through manual `workflow_dispatch`. It uploads only the `ux-console/` directory as the Pages artifact. No build command, backend, login, API key, or server runtime is required.

Before using the QR code, configure the repository's GitHub Pages source to GitHub Actions and confirm the Actions deployment succeeds.

Expected final URL pattern:

```text
https://joeorozco12.github.io/Ai_portfolio/tools
```

## Public Demo Boundary

- No login is required.
- No backend is required.
- No API keys are used.
- No real employer, customer, supplier, program, part, validation, ticket, file-path, or internal-document data should be pasted into the demos.
- Generated outputs may retain `Needs review` labels; the separate review log records synthetic-publication disposition.

## Pre-QR Checklist

- Open `/tools` from a clean browser session.
- Test phone and laptop viewports.
- Confirm the synthetic/demo label and human-review note are visible.
- Confirm the UI does not offer a direct `Safe to publish` override for generated engineering outputs.
- Confirm both browser demos run and JSON download works.
- Confirm the final URL is public HTTPS and does not contain `localhost`, `127.0.0.1`, or `192.168`.
- Generate the QR code only after the public URL is stable.

## QR Evidence

Content review for synthetic portfolio use was completed on 2026-06-13. Final QR evidence still requires the GitHub Pages `/tools` URL to open from a phone camera and a clean browser.
