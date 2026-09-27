---
id: 2
title: "The create-repos input must be derived from the answers file, not typed"
status: open
type: open-source
skill: [spawn-project]
proposes_skill: []
siblings_checked: "none — spawn-project has no sibling skill in this library"
area: "spawn-project step 4.1: the repos input of the Create repositories workflow"
date: 2026-09-27
session_context: "A later session was asked to create one missing repo of a spawned project: the first workflow run had received a kind the answers had deferred and had missed a kind the answers listed"
resolved:
resolution:
reference:
---

**Issue:** Step 4.1 tells the session to pass "the comma-separated repo
names from the answers file". The session typed the list by hand after the
answers had changed during the questionnaire. The run created an empty repo
for a deferred kind and skipped a kind the manifest lists. Nothing flagged
it: the workflow is green whatever names it gets, and `push-all.sh` was not
run against the missing repo, so its scaffold sat in a container that was
then reclaimed. Recovery took a regeneration from the manifest's answers.

**Suggested improvement:** Have `spawn.sh` print, and write next to
`push-all.sh`, the exact `repos` and `owner` inputs for the workflow, read
from the same list `push-all.sh` loops over. Step 4.1 copies that line and
never composes it. After the run, step 4.2 checks that the job name
(`create <repos>`) equals that line.

**Principle:** When one step's input is another step's output, the
generator emits it verbatim. A list a session rebuilds from memory drifts
from the list the generator used.
