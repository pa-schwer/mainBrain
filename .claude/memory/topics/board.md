# Product board

## The Notion board, as built [2026-10-12]

One hub page per founder account, titled "Product Dev", found by search;
its ids never enter this repo. Two databases under it: Projects (one row
per project, its page holds a filtered board) and Specs (one card per
spec, `SPEC-n` ids, Stage as a select). `docs/board.md` is the recipe;
each project's ops `CLAUDE.md` holds its two links.

- Claude Design has no Notion connector (checked 2026-10-12); a session
  writes the spec onto the card from the Claude Design handoff.
- Board views made through the connector hide empty groups, so a fresh
  board shows no column until a card exists.
- The founder owns the App spec template, set as the default template of
  Specs; sessions creating a card use the default.

## Pulled down into every project spawned so far [2026-10-12]

The board reached the three earlier projects by one pull request in each
ops repo: the skill, the session directive, the links, the workflow
steps. Manifest commits stayed put, so `upstream.py` still lists what
each project has not taken. Product repos (site, functions, app, lib)
did not get their one-line pointer; they take it with their next
pull-down. One project's board starts with two cards at Staging, seeded
from its open acceptance journals.

## The App Spec template and sub-cards [2026-10-12]

The founder's template holds a user story (I'm / I need / To),
Description, User flow, Mockup with an Action list, a Notion button and
an inline Test table. The connector reads the template page but not the
inline table's schema, so `write-spec` falls back to a to-do list when
it cannot write rows. The template's name changes as the founder edits
it; skills pick it from the `<templates>` list, not by name. Features
with several screens are a global card plus sub-cards (`Parent spec`).
