## C — Cloudflare Workers

Cloudflare's create flow labels Pages "the legacy Pages workflow", so the
front ends are assets-only Workers built by Workers Builds on every push.

### C1 — Import each front-end repo

Where: https://dash.cloudflare.com → Workers & Pages → Create → Import a
repository. Connect the GitHub account `{{OWNER}}` if asked (this is a
second GitHub App install, Cloudflare's own).

For each repo below, the same settings:

{{CF_REPO_LIST}}

- Project name: the Worker name above
- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`
- Preview command: `npx wrangler preview`
- Enable Preview builds: **on**
- Protect with Cloudflare Access: off
- API token: **Create new token**. Never another project's token: it
  can lack a permission this build needs (the form warns), and revoking
  it for one project breaks the other.
- No environment variables{{CF_ENV_NOTE}}

The form has no production-branch field: it takes the repository's
default branch, `main`, and Settings → Build → Production branch lists
only branches that exist. `prod` does not, until the first go prod. So
until then `main` is the production branch, built with staging values
(only `prod` builds for prod) and served at
`<worker>.<subdomain>.workers.dev`. Every other branch builds a Preview.

At the first go prod, once `prod` exists: Settings → Build → Production
branch → `prod`, then one push to `main`. From then on `main` is a
Preview, which is staging, at `main-<worker>.<subdomain>.workers.dev`.

Preview builds live under Settings → Build → **Previews Base**: the
switch "Builds for Preview branches" and the Preview command. A session
with the C3 token can read and set the same through the API: `GET` or
`PATCH /accounts/<account>/builds/workers/<worker tag>`, with
`{"previews_enabled": true}`,
`{"previews_base_config": {"deploy_command": "npx wrangler preview"}}`,
or `{"git_repository": {"branch": "prod"}}` for the switch above. Not
`npx wrangler versions upload`: that makes a Version URL, not a Preview.

Proof: the first build of `main` is green, and
`https://<worker>.<subdomain>.workers.dev` serves the scaffold page. The
first push to another branch ends with a `Preview URL:`.

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

The proxy replaces an `Authorization` header a request already carries,
so Wrangler runs with any placeholder in `CLOUDFLARE_API_TOKEN`, next to
the real `CLOUDFLARE_ACCOUNT_ID`. `wrangler whoami` is the exception:
Cloudflare throttles it (code 971) from the proxy's shared address, so it
proves nothing; the `curl` above does.
