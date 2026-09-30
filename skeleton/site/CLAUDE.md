# {{PROJECT}}-site

The public site. Astro and Tailwind, static output, served by a Cloudflare
Worker with static assets.

## Forbidden zone

**This repo must not contain state or business logic.**

No stores, no session, no database reads, no pricing arithmetic, no
eligibility rules. Pages render markup and link out. A page that needs to
remember something belongs in the app; a rule that decides something
belongs in the functions repo.

The output is static and there is no server here. Anything that seems to
need one is in the wrong repo.

## Where this sits

```
{{PROJECT}}/
{{ARCHITECTURE_MAP}}
```

Sibling repos, no submodules. `{{PROJECT}}-ops` owns the data model, the
design system and the roadmap.

If the site ever posts a form to the back end, the payload type lives in
the canonical schema, this repo holds a byte-identical copy at
`src/lib/schema.ts`, and `check-schema.sh` checks it. The scaffold ships
that copy already so the `schema` job in CI has something to check.
Never edit it here.

## Design tokens

`src/styles/tokens.css` is the only file that may carry a color, font or
shadow value. It is empty today, because `{{PROJECT}}-ops/docs/design-system.md`
is a placeholder. Build with Tailwind's own defaults until the real tokens
land; do not invent brand values as a stand-in. When they land: raw CSS
variables named as in the design system (light, and dark under
`[data-theme="dark"]`), mapped by `@theme` to utilities.

`scripts/no-hardcoded-tokens.sh` enforces this and runs in CI. It fails on a
hex value, a color function, or a `font-family` declaration anywhere under
`src/` except `tokens.css`.

## Defaults to reach past

A model with no brief produces these. Check every page against the list,
and the real tokens against it when `design-system.md` gets filled:

> Do not default to: AI-purple gradients, centered hero over dark mesh,
> three equal feature cards, generic glassmorphism on everything,
> infinite-loop micro-animations everywhere, Inter + slate-900.

Quoted from `Leonxlnx/taste-skill` (MIT), section 0.D. An item on the
list ships only when the brief or `{{PROJECT}}-ops/docs/design-system.md`
names it.

## Pre-launch settings that have to change at launch

`robots.txt` disallows everything and `site` in `astro.config.mjs` is
`https://{{DOMAIN}}`. What remains before prod is in `LAUNCH.md`.

## Deploy

`wrangler.jsonc` describes an assets-only Worker: no script, `dist/` served
as static files. Cloudflare marks the older Pages flow as legacy, so this
is the Workers Builds path: on every push Cloudflare runs `npm run build`
then `npx wrangler deploy`. The production branch is `prod`; every other
branch is a preview deployment, and `main` is staging. Setup is in
`HANDOFF.md`.

`public/_headers` applies; Workers Static Assets reads it.

## Commands

```bash
npm run dev         # local dev server
npm run typecheck   # astro check
npm test            # vitest
npm run build       # static build into dist/
npm run preview     # serve the build
bash scripts/no-hardcoded-tokens.sh
```

`vite` is pinned in `devDependencies` on purpose. Astro and
`@tailwindcss/vite` resolve different majors otherwise, and the two copies
of the Vite types make `astro check` fail on the Tailwind plugin.

## Conventions

- TypeScript strict, through `astro/tsconfigs/strict`.
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
- `ui-ux-pro-max` answers static questions only. Leave its `--motion` dial
  unset: it attaches GSAP snippets, and an animation library lands only
  after its line in `{{PROJECT}}-ops/docs/decisions.md`.
