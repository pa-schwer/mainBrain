---
id: 10
title: "A shortlist ranked on installs alone gets picked for a job the skill does not do"
status: open
type: open-source
skill: [find-skills]
proposes_skill: []
siblings_checked: "none: find-skills is the only discovery skill in this library"
area: "find-skills Step 4 (verify quality) and Step 5 (present options)"
date: 2026-11-11
session_context: "A founder asked for a LinkedIn expert; the shortlist came from search results, and the skill picked for profile work covered posts only"
parked_until:
resolved:
resolution:
reference:
---

**Issue:** find-skills verifies a candidate on install count, source and
stars, then presents it. None of the three says what the skill covers.
The shortlist for "LinkedIn expert" was ranked that way, unread. The
founder picked the leader for reworking profiles; reading its files
afterwards showed it holds nothing on the profile. One more round trip,
and a wrong bundle one step from the library.

**Suggested improvement:** Step 4 gains a fourth check before a skill is
recommended: fetch it and read `SKILL.md` and its reference list, then
state in the shortlist what it covers and what it leaves out, in the
founder's terms. A candidate nobody read is listed as unread.

**Principle:** Popularity ranks candidates inside a job; only the files
say which job.
