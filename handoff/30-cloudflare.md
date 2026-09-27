## C — Cloudflare Workers

Cloudflare's create flow labels Pages "the legacy Pages workflow", so the
front ends are assets-only Workers built by Workers Builds on every push.

### C1 — Import each front-end repo

Where: https://dash.cloudflare.com → Workers & Pages → Create → Import a
repository. Connect the GitHub account `{{OWNER}}` if asked (this is a
second GitHub App install, Cloudflare's own).

For each repo below, the same settings:

{{CF_REPO_LIST}}

- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`
- Production branch: `prod`
- Builds for non-production branches: **on**. That is what makes `main` a
  preview deployment, which is staging.
- No environment variables{{CF_ENV_NOTE}}

Proof: a push to `main` shows a preview deployment with a URL, and the
URL serves the scaffold page.

### C2 — Custom domains (launch)

Where: the Worker → Settings → Domains & Routes. Not before launch.

{{CF_DOMAIN_LIST}}

`{{DOMAIN}}` must be on Cloudflare DNS for this to be one click. Add
`www.{{DOMAIN}}` as a redirect to the apex.

Proof: the domain serves the production Worker over HTTPS.
