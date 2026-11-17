---
id: 12
title: "A renderer check by presence passes a browser that hangs"
status: resolved
type: open-source
skill: [brand-designer]
proposes_skill: []
siblings_checked: "playwright-cli sets its own browser path through environment variables and was not affected"
area: "brand-designer scripts/setup.sh (the former logo-design setup.sh), renderer section"
date: 2026-11-17
session_context: "Web icons failed to export after the container image gained a google-chrome command"
parked_until:
resolved: 2026-11-17
resolution: "setup.sh skips the wrapper only for rsvg-convert or Inkscape, and names the wrapper google-chrome so it wins the lookup; evals/smoke.sh exports the web icon set end to end"
reference: library/skills/brand-designer/scripts/setup.sh
---

**Issue:** `setup.sh` wrote its headless-shell wrapper only when no
browser name was on PATH. The container image later gained
`/usr/bin/google-chrome`, a script over the full Chrome build, which
hangs on `--screenshot`. The check saw a browser, wrote nothing, and
every PNG render of the mark engine failed with "could not render".

**Suggested improvement:** Done. A setup step that provides a tool
proves it by using it, or prefers the one known to work; `evals/smoke.sh`
now renders through it.

**Principle:** "Is it installed" and "does it work here" are two
questions, and an image update can change the second without the first.
