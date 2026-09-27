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

The functions repo installs it from git:

```
"{{PROJECT}}-lib": "github:{{OWNER}}/{{PROJECT}}-lib#<tag>"
```

A tag, never a branch, so a deploy is reproducible. `npm run build` emits
`dist/` with declarations; `prepare` runs it on install.

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
