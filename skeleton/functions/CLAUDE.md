# {{PROJECT}}-functions

The back end. Firebase Cloud Functions v2 and Firestore, TypeScript strict,
Node 22.

## Forbidden zone

**This repo must not contain HTML.**

No templates, no rendered pages, no JSX. A function returns JSON, or the
XML document a third-party webhook demands, and nothing else. Markup here
means a view is being built in the back end, and the view belongs in the
site or the app.

## Where this sits

```
{{PROJECT}}/
{{ARCHITECTURE_MAP}}
```

Sibling repos, no submodules. `{{PROJECT}}-ops` owns the data model. Read
its CLAUDE.md before changing anything that crosses a repo boundary.

## The schema rule

`src/schema/types.ts` is a copy. The original lives at
`{{PROJECT}}-ops/docs/schema/types.ts` and is the only place a data type may
change.

Never edit the copy. Change the canonical file, then copy it over in the
same work cycle. `{{PROJECT}}-ops/scripts/check-schema.sh` diffs the two and
exits 1 on drift, and the `schema` job in CI runs it on every pull request.

That job needs the `OPS_READ_TOKEN` secret, a fine-grained PAT with
`Contents: read` on `{{OWNER}}/{{PROJECT}}-ops`. Without it the job fails with
instructions. It does not skip: a schema check that passes without running
is the failure mode this whole arrangement exists to prevent.

## Functions

Every entry point is exported from `src/index.ts`. Firebase deploys what
that file exports, so a function missing from it does not exist in prod.

| Function | Trigger | State |
|---|---|---|
| `health` | HTTP | live: proves the deploy pipeline end to end |

`health` answers `{ ok, project, schemaVersion, now }`. Keep it: the deploy
workflow verifies every export is live, and a repo with no export has
nothing to verify.

## Loops and runaway processing

On Cloud Functions a loop that never ends is not a hang, it is a bill: the
platform scales the instance that is stuck, and a Firestore trigger that
writes to the path that fired it scales without limit. These are rules, not
advice.

- Every loop over data has a bound written in the code: a page size, a
  maximum count, a deadline. `while (true)` with a `break` somewhere inside
  is not a bound. The bound is a constant in `src/policy.ts` or in the
  schema's `LIMITS`, so a test can assert it.
- Every retry has a cap and a backoff, both constants.
- No Firestore-triggered function (`onDocumentWritten` and friends) without
  a line in `{{PROJECT}}-ops/docs/decisions.md`. If one exists, it never
  writes to the path that fired it without a guard that makes the second
  pass a no-op, and a test that proves the second pass is a no-op.
- A scheduled sweep processes a bounded batch per run and leaves the rest
  to the next run. It never recurses and never schedules itself.
- Every function runs under `maxInstances`, set once in `src/config.ts`.
  A runaway cannot outscale the ceiling. Raising it is a decision, recorded.
- A retried webhook produces the same state as the first delivery. A
  handler that is not idempotent is a loop with an external driver.
- A budget alert exists on both projects (HANDOFF.md). It is the last
  safety net, and the only one that catches what the rules above miss.

## Secrets

Secret names this project uses: {{SECRET_NAMES_OR_NONE}}. They live in
Firebase Secret Manager, one set per project.

A secret is declared in `src/config.ts` with `defineSecret`, in the cycle
that first reads it, and listed in the runtime options of each function
that needs it. Not before: the deploy checks that every declared secret
exists, so declaring one ahead of its use blocks every deploy until someone
creates a value nothing reads. The scaffold declares none.

Before a cycle declares its first secret, the Secret Manager API has to be
enabled on the project and the secret created there; `HANDOFF.md` has the
steps. Never commit a secret, echo one into a log line, or paste one into
an issue.

## Firestore

Paths are built in `src/paths.ts` and nowhere else. The scaffold has one
top-level collection, `accounts/{accountId}`; add to that file as the
schema grows.

`firestore.rules` holds two invariants: an account reads only its own
subtree, and nothing is client-writable. Identity comes from an
`accountId` custom claim rather than a document lookup, which would cost a
read on every rule evaluation and can be raced during onboarding.

`firestore.indexes.json` is empty. An index lands with the query that needs
it. Firestore rejects a query with no index and prints the link to create
one, so an empty file fails loudly and an invented index fails silently.

All timestamps are epoch ms `number`, never a Firestore `Timestamp`.

## Commands

```bash
npm run typecheck   # tsc --noEmit
npm test            # build, then node --test on the compiled tests
npm run build       # tsc
npm run serve       # emulators, functions and firestore
```

## Environments and deploy

| Alias | Project | Deploys from |
|---|---|---|
| `staging` | `{{FIREBASE_STAGING}}` | `main` |
| `prod` | `{{FIREBASE_PROD}}` | `prod` |

`.firebaserc` holds the aliases. `.env.{{FIREBASE_STAGING}}` and
`.env.{{FIREBASE_PROD}}` hold per-project params that `firebase-tools` binds
to `defineInt` and `defineString` in `src/config.ts`. They are committed and
carry config only.

`.github/workflows/deploy.yml` runs on every push to `main` or `prod`,
after the tests. It needs `FIREBASE_SERVICE_ACCOUNT_STAGING` and
`FIREBASE_SERVICE_ACCOUNT_PROD` as repository secrets, each the whole JSON
of a service account key. The job refuses to run when the secret is absent,
refuses to deploy when the credential's `project_id` is not the target, and
verifies after deploying that every export is live.

The service account needs four roles in Google Cloud IAM on its project:
**Editor**, **Secret Manager Admin**, **Cloud Functions Admin** and
**Cloud Run Admin**. `HANDOFF.md` has the why for each.

`prod` only moves by fast-forward from `main`:

```bash
git push origin origin/main:prod
```

## Conventions

- TypeScript strict. `noUncheckedIndexedAccess` and
  `exactOptionalPropertyTypes` are on.
- Conventional commits.
- `main` deploys to staging. `prod` deploys to prod and only moves on the
  founder's go after a staging test. Features go through a pull request
  that Claude merges when CI is green.
- The working agreement in `{{PROJECT}}-ops/docs/workflow.md` applies here
  in full: one goal per session, side findings to
  `{{PROJECT}}-ops/docs/bugs.md`, an acceptance journal for every release
  to staging, and no promotion to prod until the founder has filled it.
- All copy in {{COPY_LANGUAGE}}, by the rules in `{{PROJECT}}-ops/BRAND.md`.
  Read that file in full before writing anything a user will read.
- Every feature lands with a happy-path test, error logging, and a line in
  `{{PROJECT}}-ops/docs/decisions.md` if an architectural choice was made.
