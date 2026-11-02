---
id: 9
title: "The pull-down direction has no renderer, so a skeleton change reaches a project by hand"
status: open
type: open-source
skill: []
proposes_skill: []
siblings_checked: "none — the finding is about scripts/upstream.py, which belongs to no skill family"
area: "scripts/upstream.py, the pull-down side"
date: 2026-11-02
session_context: "A founder asked for one interface method in every repo; the same wiring went into skeleton/ and into a project's ops and app repos in one session"
parked_until:
resolved:
resolution:
reference:
---

**Issue:** `upstream.py --patch` turns a project's files into diffs against
the skeleton, with the placeholders restored. Nothing goes the other way.
Five skeleton files (the design protocol, the acceptance template, the
workflow, the app CLAUDE.md, the ops CLAUDE.md Mockups section) had to be
edited twice, once in `skeleton/` and once in the project, by replaying
the same string replacements. The proof that the two agreed was a
hand-written `sed` that mapped the project's values back to placeholders,
a different mapping for each file.

**Suggested improvement:** `upstream.py --render <file>` renders one
skeleton file with the answers in the project's manifest, through the same
substitution `spawn.py` uses, and prints the diff against the project's
copy. Pull-down becomes: render, review the diff, apply. The same render
gives the sync check for free.

**Principle:** A two-way sync tool that automates one direction leaves the
other to hand edits, and hand edits are where the two sides drift. Give
both directions the same renderer.
