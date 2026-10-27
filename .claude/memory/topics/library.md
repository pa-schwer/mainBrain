# Library

## Candidates weighed and their verdicts [2026-09-30]

- `vercel-labs/agent-skills` web-design-guidelines (MIT): installed as a
  gate on site and app PRs [2026-09-30]. About 100 code-level rules, output `file:line`. The
  upstream skill fetches its rules from GitHub on each run; vendor
  `vercel-labs/web-interface-guidelines/command.md` instead. Its Animation
  section yields to review-animations, its Content & Copy section (US
  English, Title Case) to BRAND.md. ui-ux-pro-max already holds 119 UX
  rules that overlap part of it, with no diff-review mode.
- `microsoft/playwright-cli` (Apache 2.0, 0.1.x on a Playwright alpha):
  replaced webapp-testing [2026-10-01], pinned at 0.1.22. Runs in the web
  container once `open` gets `PLAYWRIGHT_MCP_BROWSER=chromium` and
  `PLAYWRIGHT_MCP_EXECUTABLE_PATH=/opt/pw-browsers/chromium`; later
  commands reuse that browser. Without them it looks for Chrome at
  `/opt/google/chrome` and fails. `PLAYWRIGHT_MCP_OUTPUT_DIR` keeps its
  files out of the repo. It blocks `file://`, so serve pages over http.
- `Leonxlnx/taste-skill` (MIT): out. Second static advisor, also drives
  motion (a MOTION_INTENSITY dial, prescribes the Motion library), assumes
  Next.js Server Components, landing pages only. Its anti-default list
  (section 0.D) lives in `skeleton/site/CLAUDE.md`.
- `VoltAgent/awesome-design-md` (MIT): out. 74 DESIGN.md files imitating
  real brands; the skeleton's design source is `ops/docs/design-system.md`.

## ui-ux-pro-max drifts into motion [2026-09-30]

v2.13 has `--variance/--motion/--density` dials; `--motion` attaches GSAP
snippets. The plugin is not vendored, so no addendum can stop it; the rule
sits in the site and app `CLAUDE.md` instead.

## Product UI coverage [2026-09-30]

ui-ux-pro-max covers dashboards and product types (BI/Analytics styles, a
density dial, a shadcn stack), and animate targets product components
(drawers, toasts, dropdowns). Upstream `emilkowalski/skills` also ships
`pick-ui-library`, vendored for the app [2026-09-30]: each pick is a
decision line in the project before the install.

## unlazy and parallel subagents [2026-10-12]

`Leonxlnx/unlazy` 2.1.0 vendored with its run-time files (scripts, lib,
references, templates, SECURITY, research). Node only, no network, nothing
runs on load; `gate-check --approve` is the one door to running a
`CHECK:`. Registry mirrors (aiskillstore) carry 2.0.0: take upstream. `references/gates.md` writes `node scripts/gate-lint.mjs`
relative to cwd; the addendum says it means the skill dir.

The Agent tool needs no permission in Claude Code; `Agent` in
`permissions.allow` only states it. A multi-repo cloud session reads
nothing from a repo's `settings.json` but `enabledPlugins` and
`extraKnownMarketplaces`, so the written convention in each `CLAUDE.md` is
what carries the authorization there. `Workflow` is a separate tool that
does need a rule or a prompt; not pre-approved.

## Founder skill pack [2026-10-22]

"Founder skill" names `Jakeschincariol/founder-skill` (MIT, `fd9385b`),
whose README is titled "The Founder skill": eleven `founder-*` skills,
vendored under the `validation` need, addenda in brand, marketing and
launch. Other repos share the name and are other bundles, not weighed:
`djanmagno/founder-skills` (42 skills, SaaS idea to revenue),
`gvkhosla/founder-skills` (an npx CLI), `shawnpang/startup-founder-skills`
(50 skills), `lool-ventures/founder-skills` (a Cowork plugin),
`wulaosiji/founder-skills` (pitch decks). If one is asked for, weigh it
against the founder-* domain first: two advisors on one domain.

Upstream's `tests/` run against the vendored copies when copied next to a
`skills/` folder holding them (`_load.py` resolves `SKILLS_DIR` from its
own path); `test_repo` also reads the README and the plugin manifests, so
copy those with it. The tools take paths through `${CLAUDE_SKILL_DIR}`,
and the pack writes `founder/` in the cwd: the ops repo root.

## Design need: impeccable [2026-10-22]

`npx skills find` reached skills.sh from the web container (the earlier
"blocked" note was stale). Design search, by installs: anthropics
frontend-design 1M, taste-skill 657K (out since 2026-09-30),
pbakaus/impeccable 351K, emilkowalski apple-design 234K. Taken:
impeccable 4.7.0 at `69c34b7`, as the `design` need, superseding
ui-ux-pro-max (catalog key `supersedes`). Facts that shaped the fit:

- Its engine is a Rust binary the launcher fetches from the repo's GitHub
  releases into `~/.impeccable`, checked against digests pinned in
  `scripts/engine.sha256` (the release's own sidecar proves only the
  transfer); it ran in the container.
- `detect <dir>` scans static HTML and CSS, exit 2 on findings, 0 clean.
- Context lookup: PRODUCT.md / DESIGN.md (any case) in the project root,
  `.agents/context/` or `docs/`. So `docs/product.md` is found;
  `docs/design-system.md` is not, and the addendum points at it.
- Telemetry (the "roll" API pings) is off with `"telemetry": false` in
  `.impeccable/config.json` or `IMPECCABLE_NO_TELEMETRY=1`.
- Its hook installs into `.claude/settings.local.json`; `pin` writes
  skill shortcuts. Both stay off.
- emilkowalski's newer `prototype` and `break-ui` overlap impeccable's
  `generate` and `harden`; not taken.

## Logo need: logo-design [2026-10-27]

"Logo design skill" names `kaankiziltug/logo-design-skill` (MIT, 1.4.5 at
`7340903`), whose README is titled "Logo Design Skill". Taken under a new
`logo` need, opt-in. skills.sh search for "logo", by installs:
ui-ux-pro-max `design` 41.8K (a raster generator that needs a Gemini,
Atlas Cloud or MuAPI key), rknall SVG Logo Designer 8.2K ("as-is", no
license granted), op7418 logo-generator 3.9K (MIT in the README, no
LICENSE file), resciencelab logo-creator 3.2K (three API keys),
kaankiziltug 1.2K. The last is the only one with a full method, tools
and tests, and no key.

- Upstream ships 1,432 reference SVGs of real brands, outside its MIT
  license (TRADEMARKS.md). The bundle leaves them and `gallery.html` out,
  as upstream's lite zip does; `scripts/setup.sh` fetches them at the
  vendored commit into `~/.cache/logo-design/` (sparse, blobless: under
  two seconds), and a marked fallback in `svglib.py` reads them there.
  Nothing lands in a repo, so `check-drift.sh` sees no drift either.
- `render_png.py` finds no renderer in the web container: no cairosvg,
  rsvg-convert or Inkscape, and `/opt/pw-browsers` is not on PATH.
  topics/environment.md has the Chromium details; setup.sh writes the
  wrapper.
- The founder-brand addendum hands the logo brief to logo-design where
  both are installed. impeccable has no logo work.
- First use, three rounds in one session [2026-10-27]: round 1 took the
  fast track (no questions) and put a message bubble in every concept,
  rejected as kitsch; round 2 drew the letters from primitives with round
  caps, rejected as a toy. Round 3 outlined real OFL faces (Fraunces,
  Instrument Serif, Instrument Sans) with fontTools + uharfbuzz, both
  pip-installable in the web container. The addendum now says so. Ask
  the five questions when the founder is in the chat.
