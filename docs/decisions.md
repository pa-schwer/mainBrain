# Decisions

ADR-lite. One line per architectural choice, newest last. A line lands in the
same commit as the change it describes.

Format: `YYYY-MM-DD — decision — because`

---

2026-09-27 — mainBrain is a generator plus a library, not a template repository to fork — a fork copies the state of one day and never hears about the next improvement; a generator renders the newest skeleton every time, and the manifest it leaves behind is what lets improvements flow back.
2026-09-27 — One skeleton per repo kind (ops, site, functions, app, lib), rendered with `{{PLACEHOLDERS}}` from an answers file — the questionnaire is the interface and the answers file is its record; a project can be re-rendered from it, which is what `upstream.py` relies on.
2026-09-27 — The stack is Astro + Tailwind on Cloudflare Workers for the site, Firebase Cloud Functions v2 + Firestore for the back end, Vite + React on Cloudflare Workers for the app, plain TypeScript for a library — proven on a first project: no-cost quotas cover a solo product for a long time, every deploy is a push, and each repo deploys on its own cadence.
2026-09-27 — Siblings, not a monorepo; the ops repo guards a canonical schema that every product repo copies byte for byte, checked in CI with a read token that fails the job when absent — repos sharing a data shape drift within a week, and a check that passes without running is the failure the check exists to prevent.
2026-09-27 — The generator does everything a session can (render, install, check, commit) and writes `HANDOFF.md` for the rest, each human step with its proof — the goal is minimum human action; the steps that remain are the ones a session has no way to do, and an undocumented manual step is a guess in prod.
2026-09-27 — Standard library only in `scripts/`: python3 for rendering and JSON, bash for checks — the harness already requires python3, and a generator that needs its own install step is one more thing to break before the first project exists.
2026-09-27 — Every spawned ops repo carries `.mainbrain/manifest.json` and a rule that structural changes ship to mainBrain in the same session — the skeleton must never be older than the best project, and a rule enforced by a tool (`upstream.py`) and a review beats a rule remembered.
2026-09-27 — The library holds one source per domain: `ui-ux-pro-max` for static UI, `animate` for motion with `review-animations` as its gate, `security-guidance` for security review — two advisors on one task produce two answers, and a second aesthetic across site and app is the visible symptom.
2026-09-27 — Plugins (`security-guidance`, `ui-ux-pro-max`) are enabled through the generated `settings.json`, not vendored — they ship their own hooks and data; vendoring would fork them.
2026-09-27 — This repo is public; examples use `example-owner` and `acme.example`, and spawned projects are never named here — the skeleton and the library are generic by construction, and keeping them public keeps the generic and the specific apart.
2026-09-27 — `repo_names` in the answers overrides `<project>-<kind>` for one repo, and the manifest records `repo_kinds` — a project that predates the generator cannot rename its repos, and the return path has to work for the first project too.
2026-09-27 — First upstream from the ancestor project: scroll-reveal that respects reduced motion in the site layout, footer legal constants, the green-deploy explanation, webhook-secret rotation, and three script comments — the skeleton was generalized from a project that kept improving; the return path exists so those improvements reach the next project.
2026-09-27 — Repositories are created by a `workflow_dispatch` workflow holding a `REPO_ADMIN_TOKEN` secret, triggered by the session, never by a token in the session — a GitHub App on a personal account cannot create repositories and the session's proxy replaces any token it sends, so the only place a personal token can act is GitHub Actions; the workflow creates empty repos and nothing else, so the credential's reach stays one verb wide.
