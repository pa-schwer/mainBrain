# Active skills for this repository

The skills below ship with this repo and apply to every session. Treat them
as standing instructions, not as optional tools.

## stop-slop — applies to all prose you write

Before delivering any prose (chat replies, commit messages, PR bodies,
docs, comments), apply `.claude/skills/stop-slop/SKILL.md`. Read the full
skill and its `references/` files the first time you write prose in a
session.

The rules you must not need reminding of: no adverbs, no em dashes, no
passive voice, no "not X, it's Y" contrasts, no throat-clearing openers,
no vague declaratives. Vary sentence length. State facts directly.

## mem — persistent memory at .claude/memory/

Read `.claude/commands/mem.md` for the protocol. In short:

- At session start, read `.claude/memory/me.md` and `.claude/memory/core.md`
  to pick up context from past sessions.
- When you learn something worth keeping (a user preference, a solved
  non-trivial problem, a project fact), append it to the matching
  `.claude/memory/topics/<topic>.md` and update `core.md` if it is
  significant.
- When stuck or starting unfamiliar work, grep `core.md` and follow its
  pointers before asking the user to repeat themselves.

Memory lives in git. Never write a secret, credential, or private personal
detail into it.

## task-observer — invoke before your first tool call

Read `.claude/skills/task-observer/SKILL.md` before the first tool call of
this session and before writing any plan. The skill watches the session for
patterns, corrections, and methodology worth keeping, and turns them into
skill candidates.

Workspace is pinned to this repo, not to `~/.claude/`:

    [workspace folder] = <repo root>
    observation log    = .claude/skill-observations/observation-log/

The default the skill suggests (`~/.claude/projects/<project-id>/`) does not
survive in this environment. Sessions run in a fresh container and the home
directory is discarded when it is reclaimed. Git is the only thing that
persists here, so observations must be committed to survive.

## code-simplifier — runs on every code change, before any commit

Whenever you write or modify code (not documentation, not configuration on
its own), in the same turn and before any commit: run the code-simplifier
agent on the files you changed, then re-run the project's tests, lint and
typecheck. One pass per diff. Do not chain it with the built-in /simplify
command. If the simplification breaks a test, revert the simplification
rather than adapting the test.

## product-board — specs live on the Notion board; every session keeps its card true

Read `.claude/skills/product-board/SKILL.md` before the first change of
any session that builds something the founder will test. The links to
this project's board are in `CLAUDE.md`, section "Product board".

In short: start from the card (Ready), ask questions on the card in one
batch (Questions), list pull requests on it (Building), set the staging
link and the journal when staging is green (Staging), set Live and the
date on go prod. Last update says, in one line of product terms, what is
true now and who acts next. Never write a secret into a card. A request
for a spec ("fais la spec de ...", a Claude Design mockup to turn into
cards) goes through `.claude/skills/write-spec/SKILL.md`.

## unlazy — substantial work is finished against written gates

Read `.claude/skills/unlazy/SKILL.md`, addendum first, before the first
change of any task with several outcomes: a card, a build, an audit, a
sweep over many files, or work that came back half done. A one-line fix
or a factual answer does not need it.

In short: write `GATES.md` before the work, one observable outcome per
gate, with a `CHECK:` and an `EXPECT:` wherever a command can decide it.
The card's Test section, the repo's tests, lint, typecheck and build
become gates. Run `gate-check.mjs` before reporting. No done report while
a gate is unmet; a gate that cannot be met gets an `ABANDON:` line and is
said out loud. The ledger stays out of git; its count, N of N met, goes in
the pull request body.

Independent leaves run as subagents in parallel: every launch in one
message, in the background, before the first result is read. `CLAUDE.md`
authorizes it, section "Conventions".
