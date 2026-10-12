---
name: product-board
description: Read a spec from the Notion product board and keep its card true while the work moves. Use at the start of any session that builds something the founder will test, when the founder names a card, a spec or a SPEC-n id, when a Claude Design handoff arrives, and at each of these moments - a pull request opens, a staging deploy turns green, the founder answers questions, reports a ko, or says go prod.
---

# Product board

The founder and Claude Design write specs as cards in a Notion database
called Specs. A session builds from the card and moves it. The founder
reads the board, not the repos, so a card that still says Ready while two
pull requests are open sends the founder the wrong signal.

## Where the board is

The ops repo's `CLAUDE.md`, section "Product board", holds two links: the
project's page, which carries this project's board, and the Specs data
source that every project shares. Use them. If the section says the
project is not on the board yet, do "Putting a project on the board"
below before anything else.

Reach Notion through the Notion connector: fetch, query data sources,
create pages, update page. If the session has no Notion tool, say so in
one line, name HANDOFF E4, and work from the repo. Then put the card
changes the session owes in its closing lines, so the next session with
Notion can write them.

## The card

Properties, all of them on the Specs data source:

| Property | Written by | Holds |
|---|---|---|
| Name, Project, Type, Priority, Repos | founder, Claude Design | what it is, for which project, how urgent, which repos it touches |
| Design | Claude Design, founder | the Claude Design project or exported mockup |
| ID | Notion | `SPEC-n`, unique across projects |
| Stage | whoever moves the card, by the table below | where the card is |
| Pull requests | session | one line per repo: the pull request URL |
| Staging URL, Journal | session | where to test, and the acceptance journal on `main` in ops |
| Shipped | session | the date of the go-prod promotion |
| Parent spec, Sub-specs | write-spec, founder | the global card a sub-card belongs to, and a global card's sub-cards |
| Last update | session | one line in product terms: what is true now and who acts next |

The page holds the spec, written from the App Spec template: the
template the Specs data source lists under `<templates>` when you fetch
it (with several, the one named App Spec). Its sections:

| Section | Holds | The session reads it as |
|---|---|---|
| I'm / I need / To | the user story, three lines | who the feature serves and the outcome that proves it works |
| Description | the need, the pain, how this story answers it | the why behind every trade-off |
| User flow | the path through the feature | the order of screens and states to build |
| Mockup, Action list | the screen, and what the user can do on it ("I can ...") | the behaviours to build, one per line |
| Test | a table of the founder's checks | the acceptance criteria: done means every row passes |

Below the template, the page ends with `## Dev notes`, which belongs to
the dev sessions: questions and answers, decisions, what shipped and
when. The template carries no such section, so the first session that
writes to a card appends it at the end of the page. A session adds to
Dev notes and leaves the spec above it alone. A spec that proves wrong
gets a question under Dev notes; the founder or Claude Design changes the
spec.

A card is complete, and may sit at Ready, when the user story, the
Description, the User flow and the Action list are filled and the
Mockup or the Design link shows the screen. A card at Ready that misses
one of them gets a question naming the empty section.

## Stages, and what a session does at each

| Stage | The session |
|---|---|
| Idea, Spec | does nothing; the founder and Claude Design own these. A card here is not ready to build, whatever the chat says: ask the founder whether the spec is done. |
| Ready | picks it up. Reads the whole page, the Test table included, and opens the Design link. If any answer would change the build, writes every question in one batch under Dev notes as `### Questions, <date>`, sets Stage to Questions and Last update to "N questions, waiting on the founder", and stops work on that card. With no question, sets Stage to Building. |
| Questions | waits. The founder answers under each question and moves the card back to Ready. If the founder answers in the chat instead, copy each answer under its question, then set Stage to Building. |
| Building | adds each pull request to Pull requests when it opens, with `SPEC-n` in the title so the pull request points back. Updates Last update when a pull request merges. |
| Staging | arrives here from Building when the staging deploy is green and the journal from `docs/acceptance/TEMPLATE.md` is on `main`, with a check for every row of the card's Test table: set Staging URL, Journal, Stage, and Last update to "On staging, journal ready to walk". Then tell the founder. A blocking ko sends the card back to Building, with the ko under Dev notes. A ko that does not block goes to `docs/bugs.md`, and to a new card of Type Fix at Idea if the founder wants it tracked. |
| Live | on go prod, after the promotion in `docs/workflow.md`: set Stage, Shipped, Last update to "Live, `<prod commit>`", and a Dev notes line saying what shipped. |
| Dropped | nothing. Only the founder drops a card. |

## Global cards and sub-cards

A card with Sub-specs is a global card: the feature end to end. Each
sub-card is one screen or one slice of it, and the sub-cards are what
sessions build, one per session goal, in the order of the global card's
User flow. Questions on a sub-card stay on that sub-card.

The global card's Stage follows its sub-cards, and the session that moves
a sub-card moves the global card when the rule says so:

| Global card goes to | When |
|---|---|
| Building | the first sub-card goes to Building |
| Staging | every sub-card is at Staging or Live |
| Live | every sub-card is Live; Shipped is the date of the last one |

The global card's Test table holds the end-to-end checks. The journal of
the release that brings the last sub-card to staging covers them too.

## A Claude Design handoff

Claude Design hands a design to Claude Code as a bundle or a link. When
one arrives:

- With a card named or findable (its Design link, its name), put the
  handoff link in Design if empty.
- If the card's page holds no spec yet, write the spec from the handoff
  into the sections of the App Spec template, above Dev notes. Then go
  on from Ready.
- With no card at all, follow `.claude/skills/write-spec/SKILL.md` to
  create the global card and its sub-cards, then go on from Ready with
  the first sub-card.

## Every session that builds

- **Start.** Query Specs for this project's cards in Ready, Questions,
  Building and Staging. Name the card the session works on, by ID, in
  its first message. One goal per session means one card per session.
- **Work asked in the chat with no card.** If the founder will test it on
  staging, create the card first (Type from the request, Stage Building,
  the request in the founder's words, Dev notes). Structural work the
  founder never tests (CI, harness, skills, docs) needs no card.
- **End.** The session's three closing lines in `docs/workflow.md` and
  the Last update of every card it touched say the same thing.

## Writing to Notion

- Product terms in Last update and Dev notes: what the founder will see,
  not file names or stack traces. Full URLs. Dates as `YYYY-MM-DD`.
- No secret, token, credential or customer record in a card, ever. Notion
  sits outside every gate this stack runs.
- Read a card before writing it. Change one property or append one Dev
  notes block at a time; never replace the page.
- A new card takes the App Spec template by its id, read from the
  `<templates>` list when you fetch the Specs data source. Notion fills
  the template in after the page exists: fetch the page until the
  sections appear, then write into them.
- Leave the board's structure alone: properties, stage names, views. It
  belongs to mainBrain's `docs/board.md`, and a change there is a
  structural change, made there first.

## Putting a project on the board

For a project spawned before the board existed, or spawned without
Notion access:

1. Search Notion for the page titled "Product Dev" and fetch it. Take the
   Projects and Specs data sources from its child databases. If the page
   does not exist, stop and point at mainBrain's `docs/board.md`, which
   creates it once per founder.
2. Query Projects for a row whose Slug is this project's slug. If none,
   create one: Name = title, Slug, Phase, Description, Ops repo URL.
3. On that row's page, add a board view of Specs: filter Project = the
   page, filter Stage is not Dropped, group by Stage, named
   "<title> board".
4. Write the page URL and the Specs data source URL into the ops
   `CLAUDE.md` section "Product board" and into
   `.mainbrain/answers.json` under `board` (`project`, `specs`), in one
   pull request.
