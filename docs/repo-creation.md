# Letting mainBrain create repositories

Out of the box a session cannot create a GitHub repository: a GitHub App
installed on a personal account has no such right, and the session's
proxy replaces any token a session sends with the app's own. So
`HANDOFF.md` step G1 asks a human to click "New repository" once per repo.

This page removes that step. After it, a session runs the
"Create repositories" workflow of this repo, and the workflow creates the
repos with a token that never leaves GitHub. One setup, ten minutes, done
once per GitHub account.

## 0. If the repositories go to an organization

The token is still created from your user settings, but its **Resource
owner** is the organization, and the organization has to allow that
first. Once, as an organization owner:

https://github.com/organizations/<org>/settings/personal-access-tokens

"Allow access via fine-grained personal access tokens", and "Do not
require administrator approval" unless you want to approve each token by
hand. Then, when running the workflow, set its `owner` input to the
organization; empty means the account that owns the token.

## The flow, once armed

```
answers file ──spawn.sh──▶ workspace (first commit in every repo)
      │
      └──▶ session triggers "Create repositories" (repos, owner, private)
                 │  workflow: REPO_ADMIN_TOKEN ──▶ POST /orgs/{owner}/repos
                 │            or /user/repos, one per name, skip if exists
                 ▼
            empty private repos ──add_repo + push-all.sh──▶ main pushed, CI runs
```

Three properties the rest of this page protects:

- the token never leaves GitHub: it is read by the workflow, never by a
  session, never by a file;
- the workflow has one verb: create an empty repository, skip an existing
  one. It never pushes, deletes, or changes a setting;
- what lands in a repo still goes through the session's own credentials,
  so the app installation and the working agreement gate it as before.

## 1. Create the token

Where: https://github.com/settings/personal-access-tokens/new
(fine-grained), or https://github.com/settings/tokens/new (classic).

**Fine-grained** (preferred):

- Token name `mainbrain-repo-admin`.
- Resource owner: your user, or the organization from step 0.
- Expiration: **365 days or less**. An organization can cap the lifetime
  of the tokens it accepts, and the cap is 366 days by default; a longer
  token fails on create with a 403 that names the limit and links to the
  token. Put the date in your calendar; the workflow fails with a 401 the
  day it expires.
- Repository access: **All repositories**. Creating a repository is an
  account-level act, so the token cannot be scoped to repos that do not
  exist yet.
- Repository permissions: **Administration: Read and write**. Nothing
  else. (Contents is not needed: the workflow creates empty repos and the
  session pushes with its own credentials.)

**Classic**, only if the fine-grained token is refused for a reason the
log does not explain (the workflow creates through the REST API, which
accepts fine-grained tokens; `gh repo create` would not):

- Scopes: `repo` only. It is broader than needed; keep the expiration
  short and rotate.

Generate, copy the value once.

## 2. Store it as a secret of this repository

Where: this repository → Settings → Secrets and variables → Actions →
New repository secret.

- Name: `REPO_ADMIN_TOKEN`
- Value: the token.

Paste it nowhere else. Not in a chat, not in a file, not in an issue. The
security guidance of this repo treats a value next to that name as a
finding.

## 3. Let the Claude GitHub App reach new repositories automatically

Where: https://github.com/apps/claude/installations/select_target → the
account → **All repositories**.

With "Only select repositories", every new repo has to be added by hand
before a session can push to it, which brings back the click this page
removes. "All repositories" covers repos created later.

## 4. Proof

Actions → "Create repositories" → Run workflow, with
`repos: mainbrain-smoke-test`, `visibility: private`, and `owner` set to
the organization if the token was made for one. The run prints
`created <owner>/mainbrain-smoke-test`. Delete that repository afterwards
(Settings → Danger zone); a second run prints `exists` and does nothing,
which is the idempotence the session relies on.

## Reading a red run

Every failure seen while setting this up, what it means, and the fix. The
workflow prints GitHub's message as is; this table is the translation.

| The log says | It means | Fix |
|---|---|---|
| `REPO_ADMIN_TOKEN is not set` | step 2 not done | add the secret |
| `forbids access via a fine-grained personal access tokens if the token's lifetime is greater than 366 days` | the organization caps token lifetime; the token is longer or has no expiration | edit the token's expiration to 365 days or less (the message links to it); GitHub keeps the value, no re-paste |
| `does not have the correct permissions to execute CreateRepository` | an older version of the workflow used `gh repo create`, which goes through GraphQL | update mainBrain; the workflow creates through REST now |
| `You need admin access to the organization before adding a repository to it` | the token's Resource owner is your user, not the organization | generate a new token with the organization as Resource owner (step 0 first if it is not in the list), paste it into the secret |
| `401` | the token expired or was revoked | generate a new one, paste it |
| `exists <owner>/<name>` | not an error: the repo was already there, nothing was touched | none |

## How a session uses it

`spawn-project` step 4: after the generator has made the first commit in
every repo, the session triggers the workflow with the repo names from the
answers file, waits for the run, then attaches each repo and runs
`push-all.sh`. If the workflow is red with "REPO_ADMIN_TOKEN is not set",
the session says so, points here, and falls back to `HANDOFF.md` G1.

The workflow never pushes content and never touches an existing
repository: it creates empty ones and stops. The session pushes with its
own credentials, so what lands in a repo is still gated by the app
installation and the working agreement.

## Revoking

Delete the `REPO_ADMIN_TOKEN` secret, or revoke the token in the GitHub
settings. The workflow goes back to failing with instructions, and
`HANDOFF.md` G1 is a human step again. Nothing else changes.
