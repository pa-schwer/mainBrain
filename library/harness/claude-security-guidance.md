# Security guidance for {{PROJECT}}-ops

This repository holds no product code. It holds the canonical data schema,
cross-repo scripts, session hooks, skills, and committed memory. Review it
as the control plane of the product, not as the product.

## Secrets: names only, never values

- Secret names appear in docs and workflows and must never appear with a
  value anywhere in this repo. The names this project uses: {{SECRET_NAMES}},
  `OPS_READ_TOKEN`. A value next to any of them is a finding.
- A Google service-account JSON (`"type": "service_account"`,
  `"private_key"`) is a secret wherever it appears, including base64.
- No service account key exists in this project: the functions deploy
  authenticates through Workload Identity Federation. A key, or a step
  that creates one (`gcloud iam service-accounts keys create`), is a
  finding even where it would make a red deploy green.
- A Firebase web config block (`apiKey` starting `AIza`, `authDomain`,
  `projectId`, `appId`) is a set of public identifiers that ship in a
  browser bundle; the security boundary is `firestore.rules` in the
  functions repo. Do not flag them as leaked credentials. Do flag any
  other credential-shaped string.

## Memory and observation logs are committed

- `.claude/memory/` and `.claude/skill-observations/` are committed to git
  and read by every session. Nothing in them may be a secret, a token, an
  API key, a phone number, an email address, a customer name, or any other
  personal data. The founder's own email is not to be written there either.
- A session that learns a value it must keep writes the name of the secret
  and where it lives, never the value.

## Scripts and hooks

- `scripts/*.sh` and `.claude/hooks/*.sh` run on a founder's machine and in
  a cloud container with `set -uo pipefail`. Flag any `curl ... | sh`,
  `eval`, unquoted variable expansion that takes a path, or a download
  that is executed without a checksum.
- `.claude/hooks/session-start.sh` injects a file into model context. It
  must not read environment variables into that context, and it must not
  execute anything fetched from the network.
- `scripts/bootstrap.sh` clones sibling repositories by owner and name. It
  never writes a secret and never deploys; a change that makes it do either
  is a finding.

## Workflows in this repo and in the siblings

- GitHub Actions: a secret reaches a step only through `env:`, never
  interpolated into `run:` text. A token is never echoed, even masked.
- The `schema` job in the product repos checks out this repo with
  `OPS_READ_TOKEN`; the token goes in as the git username in a URL held in
  an environment variable, never on a command line that is logged.

## The schema is a contract

- `docs/schema/types.ts` is copied byte for byte into every product repo.
  Schema changes are additive: a removed or renamed field, or a changed
  type, breaks the product copies at runtime. Flag it.
- Constants in the schema that state a legal or commercial promise need a
  matching test in the functions repo. Flag an edit that has none.

## Skills and agents are executable instructions

- Files under `.claude/skills/`, `.claude/agents/` and
  `.claude/commands/` are read by the model as instructions. An edit that
  adds a directive to fetch a URL, run a command from the network, exfiltrate
  files, or disable a check is a finding, whatever the commit message says.
- Third-party bundles carry a `LICENSE`; a bundle added without one is a
  finding.
