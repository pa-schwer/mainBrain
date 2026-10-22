---
id: 5
title: "check-drift lists every library skill a project lacks as absent, without saying which ones its kinds and needs would get today"
status: open
type: open-source
skill: []
proposes_skill: []
siblings_checked: "scripts/upstream.py covers skeleton-owned files, not library entries; nothing else reads default_for against a spawned project"
area: "scripts/check-drift.sh, the skills section"
date: 2026-10-22
session_context: "The founder asked for the design skills in a project spawned on 2026-09-27; web-design-guidelines and pick-ui-library joined the app defaults on 2026-09-30 and never reached it"
parked_until:
resolved:
resolution:
reference:
---

**Issue:** A library entry added to `default_for` after a project was
spawned never reaches that project. `check-drift.sh` prints it as
`absent ... (not installed in the child)`, in the same list as the
outbound and marketing skills the project never asked for. Nothing told a
session the project was owed two design skills until the founder asked
for them by name.

**Suggested improvement:** `check-drift.sh` reads `repos`, `needs` and
`skills_exclude` from the child's `.mainbrain/manifest.json`, runs
`skills.py select` on them, and splits the absent entries in two: `OWED`
for what the project would get if spawned today, `absent` for the rest.
`OWED` counts as a difference and prints the `skills.py install --only`
line to run.

**Principle:** A drift report says what the project would receive today,
not only what differs: the generator's own selection rule is the measure.
