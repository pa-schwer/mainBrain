---
id: 5
title: "A skill that states the size of a list kept in another file drifts with every addition"
status: actioned
type: open-source
skill: [spawn-project]
proposes_skill: []
siblings_checked: "none — spawn-project has no sibling skill in this library"
area: "spawn-project step 1, item 4: the needs questions, whose table lives in docs/questionnaire.md section 4"
date: 2026-10-22
session_context: "Adding a library bundle under a new need: the skill said 'the seven skill questions' while the questionnaire table already held eight, before this session added a ninth"
parked_until:
resolved: 2026-10-22
resolution: "Actioned in the same session: the line now reads 'every skill question', with no count."
reference:
---

**Issue:** The skill restated how many rows a table in another file held.
The table grew when `outbound` joined, and the count stayed at seven; no
check compares the two, so the next session asking the questionnaire had
no signal that one question was missing from its idea of the batch.

**Suggested improvement:** When a skill points at a list kept elsewhere,
it names the list and says "every item", never a number. A count belongs
only where a check derives it from the list.

**Principle:** One source per fact: a number that mirrors another file is
a second source, and nothing keeps it true.
