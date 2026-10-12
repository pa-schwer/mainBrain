# The product board

Specs live in Notion, on one board shared by every project. Claude Design
writes a spec as a card; Claude Code sessions read the card, build, and
move it. The founder reads the board and decides two things: what gets
specced, and go prod.

This file is the board's structure. Each founder account holds one copy
of it, created once from the recipe below. Each project's ops repo holds
the links to its own part of it, in `CLAUDE.md`, section "Product board".
No link, page id or data source id goes into this repo: it is public, and
those identify an account.

The protocol a session follows is `library/skills/product-board/SKILL.md`,
installed in every ops repo and loaded at session start.

## Layout

```
Product Dev                 hub page: the stage table, the global board
├── Projects                database, one row per project
│   └── <project page>      that project's own board (a filtered view of Specs)
└── Specs                   database, one card per spec, every project
```

## Stages

| Stage | Meaning | Who moves the card on |
|---|---|---|
| Idea | a line worth speccing one day | founder, to Spec |
| Spec | Claude Design writes the page and the mockup with the founder | Claude Design or founder, to Ready, once the page is complete and Design is set |
| Ready | a complete spec waiting for a dev session | Claude Code, to Questions or Building, on pick-up |
| Questions | the session's one batch of questions sits under Dev notes | founder answers on the card and moves it back to Ready |
| Building | branch and pull requests open, listed on the card | Claude Code, to Staging, when the staging deploy is green and the journal is on `main` |
| Staging | on staging with its acceptance journal; the founder tests | Claude Code: to Building on a blocking ko, to Live on go prod |
| Live | promoted to prod, Shipped set | nobody; a change to a live feature is a new card |
| Dropped | abandoned, kept for the record | nobody; only the founder drops a card |

A feature with several screens is one global card and one sub-card per
screen, linked by Parent spec. Sessions build the sub-cards; the global
card's Stage follows them (the skill, "Global cards and sub-cards").
`library/skills/write-spec/SKILL.md` writes a spec that way.

The stages map onto `skeleton/ops/docs/workflow.md`, "A feature, start to
finish": Ready is step 1, Questions step 2, Building step 3, Staging
steps 4 and 5, Live step 6.

## The recipe

A session with the Notion connector runs these once per founder account.
`spawn-project` step 2b checks for the hub first and runs the recipe only
when the search finds no "Product Dev" page.

1. A private page "Product Dev" at the workspace root.
2. Under it, the Projects database:

   ```sql
   CREATE TABLE ("Name" TITLE, "Slug" RICH_TEXT, "Phase" SELECT('Scaffolding':gray, 'Building':blue, 'Live':green, 'Paused':brown),
     "Description" RICH_TEXT, "Ops repo" URL, "Staging URL" URL, "Prod URL" URL)
   ```

3. Under it, the Specs database, with Projects' data source id in the
   relation:

   ```sql
   CREATE TABLE ("Name" TITLE, "ID" UNIQUE_ID PREFIX 'SPEC',
     "Stage" SELECT('Idea':gray, 'Spec':purple, 'Ready':blue, 'Questions':yellow, 'Building':orange, 'Staging':pink, 'Live':green, 'Dropped':red),
     "Project" RELATION('<projects data source id>', DUAL 'Specs'),
     "Type" SELECT('Feature':blue, 'Fix':red, 'Tech':gray), "Priority" SELECT('Now':red, 'Next':yellow, 'Later':gray),
     "Repos" MULTI_SELECT('ops':gray, 'site':blue, 'functions':orange, 'app':purple, 'lib':green),
     "Design" URL, "Pull requests" RICH_TEXT, "Staging URL" URL, "Journal" URL,
     "Last update" RICH_TEXT, "Shipped" DATE, "Updated" LAST_EDITED_TIME)
   ```

   Then the link between a global card and its sub-cards, a relation of
   Specs to itself:

   ```sql
   ADD COLUMN "Parent spec" RELATION('<specs data source id>', DUAL 'Sub-specs' 'sub_specs')
   ```

4. Views on Specs, in the view language of the Notion connector:

   | View | Type | Configuration |
   |---|---|---|
   | All specs | table | `SORT BY "ID" DESC` |
   | Board | board | `GROUP BY "Stage"; FILTER "Stage" != "Dropped"; SORT BY "Priority" ASC; QUICK FILTER "Project", "Priority"; SHOW "Name", "ID", "Project", "Parent spec", "Priority", "Type", "Last update"` |
   | Founder queue | table | `FILTER "Stage" IN ("Idea", "Questions", "Staging"); SORT BY "Priority" ASC` |
   | Dev queue | table | `FILTER "Stage" IN ("Ready", "Building"); SORT BY "Priority" ASC` |
   | By project | table | `GROUP BY "Project"; FILTER "Stage" != "Dropped"; SORT BY "Stage" ASC` |
   | Shipped | table | `FILTER "Stage" = "Live"; SORT BY "Shipped" DESC` |

5. The hub page: the stage table above, a one-line note per view, and the
   Board view again as an inline board at the bottom.
6. The founder adds the App Spec template to Specs (New ▾, New
   template, then Set as default). It holds the user story (I'm / I need
   / To), Description, User flow, Mockup with its Action list, and a Test
   table of the founder's checks. Sessions create cards from it by id and
   read each section as the skill's table says; the Test rows become the
   acceptance journal's checks. The template is the founder's: a session
   reads it and never edits it.

## A project on the board

One row in Projects per project, created by `spawn-project` step 2b
before the generator runs, or by the skill's "Putting a project on the
board" for a project spawned earlier:

- Name = the answers' `title`, Slug = `project`, Phase = Scaffolding,
  Description, Ops repo = `https://github.com/<owner>/<ops repo>`.
- On the row's page, an inline board of Specs: `FILTER "Project" = "<page
  url>"; FILTER "Stage" != "Dropped"; GROUP BY "Stage"; SORT BY "Priority"
  ASC`, named `<title> board`. A card added from it gets the project set.
- The page URL and the Specs data source URL go into the answers under
  `board` (`project`, `specs`), and from there into the ops `CLAUDE.md`.

## Claude Design

Claude Design has no Notion connector. It hands a design to Claude Code
as a bundle or a link, and the session that receives it writes the spec
onto the card from the handoff, in the sections of the App Spec template (the
skill, "A Claude Design handoff"). A founder working in Claude Design can
also paste the spec into the card and set Design to the project link.

## Changing the structure

A property, a stage or a view is structure. Change this file first, in a
pull request here, then the board in Notion, then the skill if a session
has to act differently. A project session never changes the structure on
its own.
