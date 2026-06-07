# QR Deployment Notes

[SYNTHETIC — FOR DEMONSTRATION ONLY]

> Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.

## Static Deploy Root

Publish the `ux-console/` directory as the static site root.

The printed QR code should point to:

```text
https://<github-user>.github.io/<repo>/tools
```

The `/tools` route is a static shim that opens `index.html#tools`. Deep links are available for:

- `/tools/requirements`
- `/tools/feasibility`
- `/tools/wcca`
- `/tools/design-review`
- `/tools/evidence`

## GitHub Pages Deploy

Use the repository workflow at `.github/workflows/deploy-ux-console.yml`.

The workflow uploads only the `ux-console/` directory as the Pages artifact. No build command, backend, login, API key, or server runtime is required.

Expected final URL pattern:

```text
https://<github-user>.github.io/<repo>/tools
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

Do not generate final QR evidence until the GitHub Pages URL is live and verified from a phone away from the Mac. Once verified, generate the printed QR code from the final `/tools` URL and capture one phone screenshot as publication evidence.
