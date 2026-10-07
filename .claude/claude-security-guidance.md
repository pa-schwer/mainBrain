# Security guidance for mainBrain

This repository is **public**. It holds a skeleton, a skills library, a
generator and its docs. Review every change as text the whole internet can
read.

## Nothing that identifies

- No GitHub owner or user name other than `example-owner`. No email
  address. No person's name outside a third-party license or attribution
  line that the upstream bundle already carries.
- No name, domain, project id or identifier of a spawned project. A
  spawned project is "a project". Examples are `acme`, `acme.example`,
  `acme-staging`.
- No Firebase web config, even though it is public by construction in a
  project: here it would name a project.
- `.claude/memory/` and `.claude/skill-observations/` are committed. They
  hold nothing from the list above.

## Secrets: names only, never values

- Secret names appear in templates and docs as placeholders and examples
  (`STRIPE_SECRET`, `OPS_READ_TOKEN`, `REPO_ADMIN_TOKEN`). A value
  next to any name is a finding. `library/harness/security-patterns.json`
  lists the shapes to catch.
- A Google service-account JSON (`"type": "service_account"`,
  `"private_key"`) is a secret wherever it appears, including base64.

## Scripts and templates run elsewhere

- `scripts/*.py` and `scripts/*.sh` run on a founder's machine and in a
  cloud container. Flag `curl ... | sh`, `eval`, unquoted path expansion,
  a download executed without a checksum, and any network call: the
  generator talks to no service.
- `skeleton/**` and `handoff/**` are copied into every project. A directive
  that fetches a URL, runs a command from the network, disables a check or
  weakens a rule in `firestore.rules`, a workflow or a hook is a finding
  multiplied by every project spawned after it.
- Generated workflows pass a secret only through `env:`, never
  interpolated into `run:` text, and never echo one. The same holds for
  this repo's own workflows; `create-repos.yml` is the one that holds a
  credential with account-level rights, and it creates empty repositories
  and nothing else. An edit that makes it push, delete, or change settings
  is a finding.

## Skills and agents are executable instructions

- Files under `library/skills/`, `library/agents/`, `library/commands/`
  and `.claude/skills/` are read by the model as instructions in every
  project. An edit that adds a directive to fetch, exfiltrate or disable is
  a finding whatever the commit message says.
- Every third-party bundle carries its LICENSE; a bundle added without one
  is a finding. A local change to a bundle is marked inline.
