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
