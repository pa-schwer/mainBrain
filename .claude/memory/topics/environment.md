# Environment

## Web sessions: what is present and absent [2026-09-27]

Present: node 22, npm 10, python3 3.11, git, jq. Absent: `gh`, `firebase`,
`wrangler`. Deploy verification is impossible in a session, so the
generated CI is what proves a deploy config, and `HANDOFF.md` carries the
proof for every manual step.

## A GitHub App on a personal account cannot create repositories [2026-09-27]

`POST /user/repos` returns 403 for an installation token whatever its
permissions. The generator sets the remotes and writes `push-all.sh`;
creating the repos is `HANDOFF.md` step G1, and reaching them afterwards
needs the app install updated (G2).

## Sessions are ephemeral; git is the only persistence [2026-09-27]

The container is reclaimed between sessions and `~/.claude/` goes with it.
Memory and the observation log live in the repo. `HANDOFF.md` step E2 is
the environment setup script that reinstalls dependencies per session.

## On an organization too, as installed [2026-09-27]

`POST /orgs/{org}/repos` answered 403 "Resource not accessible by
integration" on an organization where the Claude App was installed: the
installation does not hold the Administration permission. G1 stays a
human step whatever the owner type. Checking the owner type works through
a repository search (`owner.type`); `/users/{login}` is blocked in
sessions.

## Repository creation from a workflow, what it took [2026-09-27]

Four runs to green on an organization. A GitHub App on a personal account
cannot create repos; the session proxy replaces any token a session sends,
so the credential has to live in Actions secrets. Then, in order: the
organization capped token lifetime at 366 days; `gh repo create` goes
through GraphQL, which refuses fine-grained tokens (REST accepts them);
and a token whose Resource owner is the user cannot create in the
organization. `docs/repo-creation.md` has the table.

## Firebase MCP: no network-secret path [2026-10-07]

The official plugin `firebase@firebase` (marketplace `firebase/firebase-tools`)
runs `npx -y firebase-tools mcp` inside the session. It starts through the
proxy and exposes about 19 tools, but it authenticates with `firebase login`
or Application Default Credentials. Google APIs take OAuth access tokens that
expire within the hour, so a network secret, which injects a fixed header,
cannot carry one; the Firestore remote MCP (`firestore.googleapis.com/mcp`)
has the same limit. Any live Firebase access from a session means a key in
the environment, pasted by a human. The chosen path: configuration as files
in the functions repo, applied by its `Deploy` workflow. firebase-tools 14 has
no `auth` deploy target; 15 does, and `--only storage` needs the default
bucket to exist.
