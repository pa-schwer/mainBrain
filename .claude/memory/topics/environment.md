# Environment

## Web sessions: what is present and absent [2026-09-27]

Present: node 22, npm 10, python3 3.11, git, jq. Absent: `gh`, `firebase`,
`wrangler`. Deploy verification is impossible in a session, so the
generated CI is what proves a deploy config, and `HANDOFF.md` carries the
proof for every manual step.

## A GitHub App on a personal account cannot create repositories [2026-09-27]

`POST /user/repos` returns 403 for an installation token whatever its
permissions. On an organization it works through `/orgs/{org}/repos`. The
generator sets the remotes and writes `push-all.sh`; creating the repos is
`HANDOFF.md` step G1, and reaching them afterwards needs the app install
updated (G2).

## Sessions are ephemeral; git is the only persistence [2026-09-27]

The container is reclaimed between sessions and `~/.claude/` goes with it.
Memory and the observation log live in the repo. `HANDOFF.md` step E2 is
the environment setup script that reinstalls dependencies per session.
