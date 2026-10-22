---
id: 6
title: "A note that a host is blocked goes stale; probe it before routing around it"
status: actioned
type: open-source
skill: [find-skills]
proposes_skill: []
siblings_checked: "none — find-skills is the only discovery skill in this library"
area: "the find-skills catalog summary and memory/topics/library.md"
date: 2026-10-22
session_context: "A founder asked for the best design skill, through find-skills; the catalog said skills.sh was blocked from the web container"
parked_until:
resolved: 2026-10-22
resolution: "Actioned in the same session: `npx skills find` answered with install counts, the catalog summary now gives the date it worked and keeps GitHub as the fallback."
reference:
---

**Issue:** The catalog told every session that skills.sh was blocked, so a
session would have searched GitHub by hand and lost the install counts the
skill uses to rank candidates. One `npx skills find` showed the claim was
no longer true.

**Suggested improvement:** A statement about what the network allows
carries the date it was observed, and a session spends one probe before
taking the workaround.

**Principle:** Environment facts expire; date them and test them before
acting on them.
