# Decisions

ADR-lite. One line per architectural choice, newest last. A line lands in the
same commit as the change it describes.

Format: `YYYY-MM-DD — decision — because`

---

{{DATE}} — Spawned from mainBrain with {{REPO_LIST}} — the stack, the working agreement and the skills library are inherited; a divergence from mainBrain is a line here and, if it generalizes, a change to mainBrain first.
{{DATE}} — `{{PROJECT}}-ops` guards the schema; `docs/schema/types.ts` is the only editable copy — repos sharing a data shape drift within a week otherwise, and the drift shows up as a runtime bug in production rather than a type error in CI.
{{DATE}} — Siblings, not a monorepo, no submodules — each repo deploys to a different target on its own cadence; a monorepo would couple the release trains for no gain at this size.
{{DATE}} — Timestamps are epoch ms `number`, never a database `Timestamp` — the same type crosses the wire to the dashboard without a converter, and a latency metric is a subtraction.
{{DATE}} — The schema check runs in each product repo's CI by cloning the ops repo with an `OPS_READ_TOKEN` PAT, and fails when the secret is absent — a check that reports success without running is the exact failure this repo exists to prevent, and submodules are ruled out.
{{DATE}} — Schema changes are additive: new fields are optional, nothing is renamed, nothing changes type — a document store will not reject a document that predates a change, so a required new field is a runtime crash on old data.
{{DATE}} — `main` deploys to staging; `prod` is a branch fast-forwarded from `main` on the founder's go — the founder validates the product on staging and never reads code, so the promotion is the one human decision and it has to be a git operation a machine can audit.
{{DATE}} — Claude merges its own pull requests when the automated gates are green — no human reads the diff, so every gate a reviewer would have been is a check in CI or a skill Claude runs before merging; there is no override.
{{DATE}} — Every release to staging ships with an acceptance journal in `docs/acceptance/`, and prod waits for it to be filled — the founder validates without reading code, so what to test and what to break has to be written down by the session that built it.
{{DATE}} — Every step a human must do lives in `HANDOFF.md` with the check that proves it done — a session that cannot verify a manual step will assume it, and the assumption fails in prod.
