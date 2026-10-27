---
id: 7
title: "A bundle's license may not cover every file in it; check before vendoring"
status: open
type: open-source
skill: [find-skills]
proposes_skill: []
siblings_checked: "none: find-skills is the only discovery skill in this library"
area: "find-skills Step 4 (verify quality) and the 'Adding a bundle' paragraph of CLAUDE.md"
date: 2026-10-27
session_context: "The founder asked to install a logo design skill; the best candidate is MIT but ships 1,432 brand logos its license excludes"
parked_until:
resolved:
resolution:
reference:
---

**Issue:** find-skills ranks a candidate by install count, source and
stars, and the library recipe asks for "its LICENSE". Neither asks
whether that license covers every file. `kaankiziltug/logo-design-skill`
is MIT, and its TRADEMARKS.md excludes the 12 MB of reference SVGs from
it. Copying the folder whole would have published real brands' logos in
this public repo.

**Suggested improvement:** Step 4 and the recipe add one check: read the
bundle for a NOTICE, TRADEMARKS or per-folder license, vendor only what
the license covers, and fetch the rest at use time into a cache outside
every repo.

**Principle:** A license file at the root states the default, and a
notice beside it can carve files out.
