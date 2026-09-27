## G — GitHub

Repository creation has two paths. The **automatic** one is the default:
mainBrain's "Create repositories" workflow holds a token the session
cannot have, and the session triggers it. The **manual** one is the
fallback when that workflow was never armed for `{{OWNER}}`.

A session cannot create a repository on its own: on a personal account the
API refuses repository creation to any GitHub App, on an organization the
Claude App gets a 403 because its installation does not hold the
Administration permission, and the session's proxy replaces any token a
session sends with the app's own. So the credential lives in mainBrain's
Actions secrets, and acts from there. Everything after G1 is a click or a
paste.

### G1 — Create the repositories

The repositories this project needs, all **empty**: no README, no
.gitignore, no license. The generated repo already has all three, and an
initialized remote makes the first push a merge. Private.

{{REPO_CREATE_LIST}}

**Path A, automatic (default).** Done once for `{{OWNER}}`, in
`mainBrain/docs/repo-creation.md`: a fine-grained token with the account
(or the organization) as resource owner, Administration read and write on
all repositories, 365 days; stored as `REPO_ADMIN_TOKEN` in
`mainBrain`'s Actions secrets; the Claude App installed for **All
repositories** so the new repos are reachable without a second visit.

Then the session does the rest, with no click:

1. It triggers `Create repositories` in mainBrain (Actions → Create
   repositories → Run workflow) with `repos` = the names above,
   `owner` = `{{OWNER}}`, `visibility` = `private`.
2. The run prints one line per repo: `created {{OWNER}}/<name>`, or
   `exists {{OWNER}}/<name>` when it was already there (nothing is touched).
3. It pushes with `push-all.sh` (G3).

If the run is red, its log names the cause and the fix; the table in
`mainBrain/docs/repo-creation.md`, "Reading a red run", translates each
message. `REPO_ADMIN_TOKEN is not set` means path A was never armed:
fall back to path B, or arm it (ten minutes, once).

**Path B, by hand.** Where: https://github.com/new, signed in as
`{{OWNER}}`. One repo at a time, from the list above, empty, private.
Default branch name does not matter; the push sets `main`.

Proof, either path: the URLs above open and each shows "This repository
is empty" until G3.

### G2 — Let Claude reach them

Where: https://github.com/apps/claude/installations/select_target

Choose the `{{OWNER}}` account and **All repositories**, so a repo created
later is reachable without another visit here; or add each repo from G1
to the selection. Without this, a session cannot clone,
push or open a pull request on them, whatever else is configured.

Then, in the Claude Code environment, attach the repos (step E1).

Proof: a session runs `add_repo` for `{{OWNER}}/{{PROJECT}}-ops` and gets a
clone command back instead of an access error.

### G3 — Push the generated repos

Where: the workspace this file sits in, or a session with the repos
attached.

```bash
bash push-all.sh
```

The script pushes `main` of every repo to its `origin`. It is safe to
re-run. If it refuses because a remote is not empty, G1 was done with a
README; delete the remote's initial commit or recreate the repo empty.

Proof: every repo shows the scaffold commit on `main` and its CI runs.

### G4 — The ops read token

Where: https://github.com/settings/personal-access-tokens/new

Every product repo's CI clones `{{PROJECT}}-ops` to check its schema copy,
and `GITHUB_TOKEN` only reaches the repo it runs in. So:

1. Token name `{{PROJECT}}-ops-read`. Expiration: one year (put the date in
   your calendar; the `schema` job goes red with a 401 the day it expires).
2. Repository access: **Only select repositories** → `{{PROJECT}}-ops`.
   The default, "Public repositories", sees no private repo and yields a
   404 that reads like a typo in the owner.
3. Repository permissions: **Contents: Read**. Nothing else.
4. Generate, copy the value once.
5. In each product repo, Settings → Secrets and variables → Actions → New
   repository secret, name `OPS_READ_TOKEN`, paste the value:

{{OPS_TOKEN_REPO_LIST}}

Paste it nowhere else. Not in a chat, not in a file, not in an issue.

Proof: the `schema matches {{PROJECT}}-ops` job is green in each of those
repos. Red with "OPS_READ_TOKEN is not set" means the secret is missing;
red with `-> 404` means step 2 was skipped; `-> 401` means it expired or
was mistyped.
