# Active skills for this repository

The standing directives live in the library, not in a second copy under
`.claude/skills/`. Read them by path.

## stop-slop — applies to all prose you write

Before delivering any prose (chat replies, commit messages, PR bodies,
docs, templates), apply `library/skills/stop-slop/SKILL.md`. Read the full
skill and its `references/` files the first time you write prose in a
session.

The rules you must not need reminding of: no adverbs, no em dashes, no
passive voice, no "not X, it's Y" contrasts, no throat-clearing openers,
no vague declaratives. Vary sentence length. State facts directly.

## mem — persistent memory at .claude/memory/

Read `library/commands/mem.md` for the protocol. At session start, read
`.claude/memory/me.md` and `.claude/memory/core.md`. When you learn
something worth keeping, append it to `.claude/memory/topics/<topic>.md`
and update `core.md` if it is significant.

Memory lives in git, and this repo is public. Never write a secret, a
credential, a person, an account, a project name, a domain or an id into
it.

## task-observer — invoke before your first tool call

Read `library/skills/task-observer/SKILL.md` before the first tool call of
this session and before writing any plan.

Workspace is pinned to this repo:

    [workspace folder] = <repo root>
    observation log    = .claude/skill-observations/observation-log/

Sessions run in a fresh container; git is the only thing that persists.

## code-simplifier — runs on every code change, before any commit

Whenever you write or modify code in `scripts/` or in a skeleton (not
documentation, not a template's prose), in the same turn and before any
commit: run the code-simplifier agent from `library/agents/code-simplifier.md`
on the files you changed, then run `bash scripts/check-library.sh`. One
pass per diff.

## spawn-project — the one skill of this repo

`.claude/skills/spawn-project/SKILL.md` runs when a new project is asked
for. It is the questionnaire and the handover; `scripts/spawn.sh` is the
work.

## This repository is public

Nothing confidential, ever. `.claude/claude-security-guidance.md` says
what that means in patterns.
