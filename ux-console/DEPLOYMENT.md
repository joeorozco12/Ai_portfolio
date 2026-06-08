# QR Deployment Notes

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Static Deploy Root

Publish the `ux-console/` directory as the static site root.

The printed QR code should point to:

```text
https://jose-orozco-ai-workflow-console.netlify.app/tools
```

The `/tools` route is a static shim that opens `index.html#tools`. Deep links are available for:

- `/tools/requirements`
- `/tools/feasibility`
- `/tools/wcca`
- `/tools/design-review`
- `/tools/evidence`

## Netlify Deploy

Netlify should use the root `netlify.toml` file:

```toml
[build]
  publish = "ux-console"
  command = ""
```

The connected Netlify site should deploy from the Git repository root and publish only `ux-console/`. The `_redirects` file inside `ux-console/` keeps `/tools` and the deep-link routes working.

Expected Netlify URL:

```text
https://jose-orozco-ai-workflow-console.netlify.app/tools
```

## GitHub Pages Fallback

Use the repository workflow at `.github/workflows/deploy-ux-console.yml`.

The workflow runs on pushes to `main` and through manual `workflow_dispatch`. It uploads only the `ux-console/` directory as the Pages artifact. No build command, backend, login, API key, or server runtime is required.

Before using GitHub Pages as the fallback QR target, configure the repository's GitHub Pages source to GitHub Actions and confirm the Actions deployment succeeds.

Expected final URL pattern:

```text
https://joeorozco12.github.io/Ai_portfolio/tools
```

## Public Demo Boundary

- No login is required.
- No backend is required.
- No API keys are used.
- No real employer, customer, supplier, program, part, validation, ticket, file-path, or internal-document data should be pasted into the demos.
- All outputs remain `Needs review`.

## Pre-QR Checklist

- Open `/tools` from a clean browser session.
- Test phone and laptop viewports.
- Confirm the synthetic/demo label and human-review note are visible.
- Confirm `Safe to publish` is not available from the UI.
- Confirm both browser demos run and JSON download works.
- Confirm the final URL is public HTTPS and does not contain `localhost`, `127.0.0.1`, or `192.168`.
- Generate the QR code only after the public URL is stable.

## QR Evidence

Do not generate final QR evidence until the Netlify URL is live and verified from a phone away from the Mac. Once verified, generate the printed QR code from the final `/tools` URL and capture one phone screenshot as publication evidence.
