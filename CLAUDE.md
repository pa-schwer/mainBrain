# mainBrain

The repo above the projects. It holds the blank skeleton of a working
stack, the library of every skill the projects use, and the generator that
turns a questionnaire into a ready workspace. Its job is to make the next
project start where the last one left off.

**This repo is public.** Nothing in it may name a customer, a person, an
account, a project id, a domain that is not an example, or a secret.
Examples use `example-owner` and `acme.example`. The projects it spawns are
private and stay out of here; they are referred to as "a project", never
by name.

This repo never contains product code, and never contains a spawned
project. A workspace generated here is written next to this repo, not
inside it.

## What is here

```
mainBrain/
├── skeleton/       one blank repo per kind, with {{PLACEHOLDERS}}
│   ├── ops/        orchestrator: schema, docs, scripts, harness seed
│   ├── site/       Astro + Tailwind → Cloudflare Workers
│   ├── functions/  Firebase Cloud Functions v2 + Firestore
│   ├── app/        Vite + React → Cloudflare Workers
│   ├── lib/        pure TypeScript, no I/O, no deploy target
│   └── _shared/    fragments rendered into several kinds (schema CI job, token check)
├── library/        the skills library
│   ├── catalog.json  every entry: kind, mode, origin, license, needs, defaults
│   ├── skills/       vendored bundles, each with its LICENSE
│   ├── agents/       code-simplifier
│   ├── commands/     mem
│   └── harness/      settings, hook, session-context, security guidance and patterns
├── handoff/        the human steps, one section per service, rendered per stack
├── scripts/        spawn, skills, upstream, check-library, check-drift
├── examples/       an answers file that spawns every kind
└── docs/           questionnaire, workflow, decisions, upstream rule
```

## Spawning a project

The conversation is the questionnaire. When someone asks for a new
project, load `.claude/skills/spawn-project/SKILL.md` and follow it: it
asks the questions in `docs/questionnaire.md`, one batch, writes the
answers file, runs the generator, and hands over the workspace with its
`HANDOFF.md`.

```bash
bash scripts/spawn.sh <answers.json> --out <parent dir>
```

The generator renders the skeleton for each requested repo kind, copies
the schema into every product repo, installs the harness and the selected
skills into the ops repo, writes `HANDOFF.md` with only the human steps
that stack needs, installs dependencies, runs typecheck, tests, builds and
the token check in every repo, and makes the first commit on `main`. It
never talks to GitHub, Firebase or Cloudflare; `HANDOFF.md` is where that
starts, and each step there ends with the check that proves it done.

Autonomy is the goal: everything a session can do, the generator does.
What it cannot do (create a repo on a personal account, a billing account,
a console click, a secret paste) is written down step by step, with the
proof, so the human does it once and never guesses.

## The library

`library/catalog.json` is the index. Each entry says what the skill is,
where it came from, its license, which `needs` it answers and which repo
kinds get it by default. `scripts/skills.py select` shows what a project
would get; `scripts/skills.py install` puts it in an ops repo.

Three modes, and the mode decides how the skill starts in a project:
**standing** directives load from the session hook; **automatic** plugins
run their own hooks; **on-demand** skills trigger on the work. A **gate**
is read by path before a merge.

Adding a bundle: vendor it with its LICENSE under `library/skills/`, add
the catalog entry, mark any local change inline so an update can strip it,
and run `scripts/check-library.sh`. Two advisors on one domain is the
failure to avoid: one source for static UI, one for motion, one for
security review.

## The way back: structural changes flow up

Every spawned project carries `.mainbrain/manifest.json`: the answers, the
mainBrain commit, and the list of files the skeleton owns in each repo. A
project that improves one of those files (a workflow, a script, a harness
file, a skill addendum, a convention) owes the change to mainBrain in the
same session, as a second pull request here. That is the rule written into
every spawned ops repo, and this is where it lands.

```bash
python3 scripts/upstream.py <path to a project's ops repo>          # what is owed, both directions
python3 scripts/upstream.py <path to a project's ops repo> --patch  # diffs against skeleton/, placeholders restored
bash scripts/check-drift.sh <path to a project's ops repo>          # the library side: skills, agent, command, harness
```

A change that only makes sense for one product stays in that product. A
change that would help the next project comes here first, then goes back
down to every project that wants it. Newest structure wins; the skeleton is
never older than the best project.

## Checks

```bash
bash scripts/check-library.sh          # catalog vs disk, placeholders vs spawn.py, json, shell, python
bash scripts/spawn.sh examples/answers.example.json --out /tmp/x --force   # the whole thing, end to end
```

CI runs both on every pull request. A skeleton change that does not spawn
green does not merge.

## Conventions

- Templates are plain files with `{{UPPER_SNAKE}}` placeholders. A
  placeholder spawn.py does not set fails the library check; a placeholder
  left in a generated file fails the spawn.
- Standard library only in `scripts/`: python3 and bash, no package to
  install. python3 is already required by the harness.
- Conventional commits. Every change goes through a pull request that
  Claude opens and merges when the checks are green, without asking.
- A change to the skeleton says why in `docs/decisions.md`, one line.
- The stack itself (Astro, Firebase, Vite, Cloudflare Workers, the
  two-environment workflow) is a decision recorded in `docs/decisions.md`.
  Adding a kind of repo is a new `skeleton/<kind>/` plus a `PURPOSE` and
  `FORBIDDEN` line in `spawn.py`, and its own CI template.

## Memory and skills for this repo

`.claude/memory/` holds what sessions here learn; it is committed and
public, so it holds nothing private. The standing directives (stop-slop,
task-observer, mem, code-simplifier) load from `.claude/session-context.md`
through the SessionStart hook and point at the library copies, so this
repo does not carry a second copy of its own skills. `spawn-project` is the
one skill that lives in `.claude/skills/` here, because only this repo
uses it.
