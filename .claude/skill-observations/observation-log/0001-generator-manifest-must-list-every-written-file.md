---
id: 1
title: "A generator's manifest must list every file every code path writes"
status: open
type: open-source
skill: [spawn-project]
proposes_skill: []
siblings_checked: "none — spawn-project has no sibling skill in this library"
area: "spawn.py: skeleton_owned in .mainbrain/manifest.json"
date: 2026-09-27
session_context: "Building mainBrain: the harness install path wrote files into the ops repo without adding them to the manifest, so upstream.py could not see a changed hook until check-drift.sh caught it"
resolved:
resolution:
reference:
---

**Issue:** The generator had two code paths that write files into a
spawned repo (skeleton render and harness install). Only the first
registered its outputs in the manifest, so the drift detector built on
the manifest was blind to the second path's files. A second, independent
check (check-drift.sh) found the gap by accident.

**Suggested improvement:** In spawn-project's "run the generator" step, add
a verification line: after a spawn, `upstream.py` on the fresh workspace
must report zero owed files, and a deliberate edit to one file from each
install path (a skeleton file, a harness file, a skill file) must show up.
The CI already asserts the zero case; the "each path" case is what caught
this.

**Principle:** A registry of generated files is only as complete as the
least-instrumented writer. Every function that writes into the output must
return what it wrote, and the caller merges it, or the registry silently
under-reports and every tool built on it inherits the blind spot.
