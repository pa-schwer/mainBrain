# {{PROJECT}}-app

The dashboard at {{APP_DOMAIN}}. Vite and React, TypeScript strict, served
by a Cloudflare Worker with static assets.

## Forbidden zone

**This repo must not contain business logic.**

It reads Firestore and it calls functions. It does not decide anything.

No pricing arithmetic, no qualification rules, no compliance check, no
status transition. A derived number is computed in the functions repo;
this repo renders the number it is given.

A calculation written here is a second source of truth for a rule that
already exists in the back end, and the two drift.

## Where this sits

```
{{PROJECT}}/
{{ARCHITECTURE_MAP}}
```

Sibling repos, no submodules.

## The schema rule

`src/schema/types.ts` is a copy. The original lives at
`{{PROJECT}}-ops/docs/schema/types.ts` and is the only place a data type may
change.

Never edit the copy. Change the canonical file, then copy it over in the
same work cycle. `{{PROJECT}}-ops/scripts/check-schema.sh` diffs the two and
exits 1 on drift, and the `schema` job in CI runs it on every pull request.

That job needs the `OPS_READ_TOKEN` secret, a fine-grained PAT with
`Contents: read` on `{{OWNER}}/{{PROJECT}}-ops`. Without it the job fails with
instructions. It does not skip.

All timestamps are epoch ms `number`. A Firestore document crosses the wire
into a component with no converter, and a latency metric is a subtraction.

## Firebase

`src/lib/firebase.ts` holds initialization and three handles. No query, no
rule, no derived value.

Config comes from four `VITE_FIREBASE_*` variables in `.env.staging` and
`.env.production`, both committed. These are public values that ship inside
the bundle by design; the security boundary is `firestore.rules` in the
functions repo: an account reads only its own subtree, and nothing is
client-writable. The values are blank until HANDOFF.md step F5 is done;
the client throws at startup naming the missing ones.

`scripts/build.mjs` picks the file by branch. `prod` builds with
`.env.production` ({{FIREBASE_PROD}}). Every other branch, and a local
machine with no branch variable, builds with `.env.staging`
({{FIREBASE_STAGING}}). The default is staging on purpose: a build that
cannot tell where it is must not point at prod. `npm run dev` runs in
staging mode for the same reason.

A real secret never appears here. Secrets live in Firebase Secret Manager
and are read by Cloud Functions alone.

`src/lib/firebase.ts` is wired and unused today, so the config is not in
the bundle yet; Vite drops the module. The first screen that reads
Firestore imports it.

## Deploy

`wrangler.jsonc` describes an assets-only Worker: no script, `dist/` served
as static files, single-page-application handling so the client router owns
every path that is not a file. Workers Builds runs `npm run build` then
`npx wrangler deploy` on every push. The production branch is `prod`;
every other branch is a preview deployment, and `main` is staging. Setup
is in `HANDOFF.md`.

## Design tokens

`src/styles/tokens.css` is the only file that may carry a color or a font
value. It is empty today, because `{{PROJECT}}-ops/docs/design-system.md` is
a placeholder. Build with Tailwind's own defaults until the real tokens
land. Do not invent brand values as a stand-in.

`scripts/no-hardcoded-tokens.sh` enforces this and runs in CI.

The dashboard follows system preference, so the real token set needs light
and dark from the start.

## Commands

```bash
npm run dev         # local dev server, staging mode
npm run typecheck   # tsc --noEmit
npm test            # node --test on the build-mode logic
npm run build       # typecheck, then scripts/build.mjs picks the mode by branch
npm run preview     # serve the build
bash scripts/no-hardcoded-tokens.sh
```

## Conventions

- TypeScript strict. `noUncheckedIndexedAccess`,
  `exactOptionalPropertyTypes`, `noUnusedLocals` and `verbatimModuleSyntax`
  are on.
- Conventional commits.
- `main` deploys to staging. `prod` deploys to prod and only moves on the
  founder's go after a staging test. Features go through a pull request
  that Claude merges when CI is green.
- The working agreement in `{{PROJECT}}-ops/docs/workflow.md` applies here
  in full.
- All copy in {{COPY_LANGUAGE}}, by the rules in `{{PROJECT}}-ops/BRAND.md`.
  Read that file in full before writing anything a user will read.
- Design tokens are never hardcoded.
- Motion goes through `animate` and is gated by `review-animations` when
  those skills are installed in ops.
- A pull request that touches markup, styles or components passes
  `web-design-guidelines` before merge, read by path from
  `{{PROJECT}}-ops/.claude/skills/`.
- A component, toast, chart or state library comes from `pick-ui-library`,
  read by path from the same folder, and lands after its line in
  `{{PROJECT}}-ops/docs/decisions.md`.
- `ui-ux-pro-max` answers static questions only. Leave its `--motion` dial
  unset: it attaches GSAP snippets, and an animation library lands only
  after its line in `{{PROJECT}}-ops/docs/decisions.md`.
- Every feature lands with a happy-path test, error logging, and a line in
  `{{PROJECT}}-ops/docs/decisions.md` if an architectural choice was made.
