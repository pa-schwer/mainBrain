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
  worth replacing webapp-testing, never beside it. Runs in the web
  container once `.playwright/cli.config.json` sets
  `browser.launchOptions.executablePath` to `/opt/pw-browsers/chromium`;
  without it, it looks for Chrome at `/opt/google/chrome` and fails. It
  blocks `file://`, so serve pages over http.
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
