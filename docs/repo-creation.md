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

## 1. Create the token

Where: https://github.com/settings/personal-access-tokens/new
(fine-grained), or https://github.com/settings/tokens/new (classic).

**Fine-grained** (preferred):

- Token name `mainbrain-repo-admin`.
- Resource owner: your user, or the organization from step 0.
- Expiration: one year. Put the date in your calendar; the workflow fails
  with a 401 the day it expires.
- Repository access: **All repositories**. Creating a repository is an
  account-level act, so the token cannot be scoped to repos that do not
  exist yet.
- Repository permissions: **Administration: Read and write**. Nothing
  else. (Contents is not needed: the workflow creates empty repos and the
  session pushes with its own credentials.)

**Classic**, if the fine-grained token is refused on repository creation:

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
