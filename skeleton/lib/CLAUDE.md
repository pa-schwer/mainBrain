# {{PROJECT}}-lib

Pure logic: an algorithm, a model, a parser, a scoring function. TypeScript
strict, Node 22, no runtime dependency, no deploy target.

## Forbidden zone

**This repo must not touch the network, a database, or a file system.**

Every export is a function of its arguments. Reading a document, calling
an API or writing a file belongs in the functions repo, which imports this
one. That boundary is what makes everything here testable in milliseconds
without a project id, and what keeps a bounded algorithm from becoming an
unbounded process.

## Where this sits

```
{{PROJECT}}/
{{ARCHITECTURE_MAP}}
```

Sibling repos, no submodules. `{{PROJECT}}-ops` owns the data model; the
types this repo consumes are in its schema copy at `src/schema/types.ts`,
byte-identical to `{{PROJECT}}-ops/docs/schema/types.ts`, never edited here.

## Rules

- Every loop has a bound written in the code and held in a constant a test
  asserts. `LIMITS` in the schema is the place for a bound the back end
  must respect too.
- Every function is deterministic for the same input. Randomness and time
  come in as arguments.
- Every public function has a happy-path test and a test at each bound.
- No dependency lands without a line in `{{PROJECT}}-ops/docs/decisions.md`.

## How it is consumed

This repo is private, and none of GitHub Actions, Workers Builds or the
Cloud Build step of a Functions deploy can install a private git
dependency without a credential. So a release is a tarball, committed in
the `vendor/` folder of each repo that imports it:

```bash
npm pack                     # {{PROJECT}}-lib-<version>.tgz, dist/src only
cp {{PROJECT}}-lib-<version>.tgz ../{{PROJECT}}-functions/vendor/
```

```
"{{PROJECT}}-lib": "file:vendor/{{PROJECT}}-lib-<version>.tgz"
```

A release bumps `version` in `package.json`, is tagged `v<version>` on
`main`, and lands in every consumer in the same work cycle, the way the
schema copy does. `npm pack` runs `prepare`, so the tarball carries the
built `dist/src` with its declarations. It installs offline, so a deploy
is as reproducible as a tag.

## Commands

```bash
npm run typecheck   # tsc --noEmit
npm test            # build, then node --test on the compiled tests
npm run build       # tsc
```

## Conventions

- TypeScript strict. `noUncheckedIndexedAccess` and
  `exactOptionalPropertyTypes` are on.
- Conventional commits.
- The working agreement in `{{PROJECT}}-ops/docs/workflow.md` applies here
  in full.
- Substantial work runs under `unlazy`, read by path from
  `{{PROJECT}}-ops/.claude/skills/unlazy/SKILL.md`, and independent parts
  run as parallel subagents, as `{{PROJECT}}-ops/CLAUDE.md` says under
  "Conventions".
- A feature starts from its card on the product board, and the session
  moves the card as it goes: `{{PROJECT}}-ops/.claude/skills/product-board/SKILL.md`,
  with the links in `{{PROJECT}}-ops/CLAUDE.md`, "Product board".
- A label, level or message this code returns ends up in front of a user.
  Read `{{PROJECT}}-ops/BRAND.md` in full before adding or changing one.
