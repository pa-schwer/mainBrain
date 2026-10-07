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

### C3 — API token for Claude sessions

Sessions reach Cloudflare through the API and the `cloudflare` plugin's
MCP server. Both take a bearer token; OAuth needs a browser, and a cloud
session has none.

Where: https://dash.cloudflare.com/profile/api-tokens → Create Token →
template "Edit Cloudflare Workers".

- Account Resources: the account that holds the Workers.
- Zone Resources: `{{DOMAIN}}`.
- Add the permission Zone → DNS → Edit, for the domains in C2.
- No Client IP Address Filtering: the MCP server refuses those tokens.

Then the Claude Code environment (claude.ai/code → environment menu →
Edit) → Network secrets → Add secret:

- Name: `Cloudflare`
- Allowed websites: `api.cloudflare.com` and `mcp.cloudflare.com`
- Header `Authorization`, prefix `Bearer`, value: the token.

The proxy adds the token after a request leaves the session, so no
session ever holds it. A plan without Network secrets takes it as the
environment variable `CLOUDFLARE_API_TOKEN` instead, readable by every
session.

Proof: in a new session,
`curl -s https://api.cloudflare.com/client/v4/user/tokens/verify` answers
`"status":"active"` with no header sent.
