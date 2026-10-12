---
id: 4
title: "An id from an outside service reaches the skeleton through the answers file, fetched before the generator runs"
status: actioned
type: open-source
skill: [spawn-project]
proposes_skill: []
siblings_checked: "none — spawn-project has no sibling skill in this library"
area: "spawn-project step 2b, and any future service whose ids a generated file must carry"
date: 2026-10-12
session_context: "Adding a Notion product board to the kit: each ops CLAUDE.md needs the link to its project's board, the generator talks to no service, and this repo is public"
parked_until:
resolved: 2026-10-12
resolution: "Actioned in the same session: spawn-project step 2b creates the project's row on the board before the generator runs and writes the links into the answers under `board`; spawn.py renders them with a not-linked fallback; docs/board.md holds the structure and no id."
reference:
---

**Issue:** A generated file needed an identifier that only exists once an
outside service has been called (the project's page on the board). The
generator never talks to a service, and the public repo may not hold an
account's ids. Calling the service after the generator ran would have
meant a second commit in every repo and a first commit that lies.

**Suggested improvement:** For each outside service, the skill makes the
call in a step before the generator, writes the result into the answers
file, and the generator renders it with a fallback that names the
procedure for a later session. The answers file lives in the private
project, so the id never reaches the public repo.

**Principle:** Keep the generator offline and complete by giving it every
external value as input: the session fetches, the answers file carries,
the template renders, and the fallback text says how to fill the gap
later.
