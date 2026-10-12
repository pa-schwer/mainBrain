---
name: write-spec
description: Write a product spec and put it on the Notion product board the way the board expects it - one global card and one sub-card per screen, the right Project, Stage Ready, the App Spec template, every behaviour spelled out, a capture of each screen. Use whenever the user asks for "une spec", "des specs", "spécifie", "fais la spec de ...", "mets ça dans le board", "crée la carte Notion", "ajoute ça au board", "write a spec", "spec this", "put it on the board", or wants a Claude Design mockup, prototype or handoff turned into cards.
---

# Write a spec

You turn a feature, a mockup or a Claude Design handoff into cards on the
product board, ready for a dev session to build. The board is the Specs
database in Notion; `product-board` is the protocol the dev sessions
follow once the cards exist, and its tables of properties and template
sections are the contract this skill writes to.

## 1. Find the board and the project

- In a project's ops repo: `CLAUDE.md`, section "Product board", holds
  the project's page and the Specs data source. Use them.
- Anywhere else (a chat, mainBrain): search Notion for the page titled
  "Product Dev", fetch it, and take the Projects and Specs data sources
  from its child databases. Find the project in Projects by name or Slug.
- A project missing from Projects is a question for the user, not a row
  to invent: `product-board`, "Putting a project on the board", adds it.

Fetch the Specs data source once. Keep the App Spec template's id from
its `<templates>` list (with several, the one named App Spec).

## 2. Read before asking

Read everything the user gave first: the mockup, the Claude Design link
or handoff bundle, screenshots, the description in the chat. In a
project repo, read `BRAND.md` and `docs/product.md` too.

Then ask, in one batch, only what would change the cards: who the user
is if the mockup does not say, the outcome that proves the feature works,
a rule or a number the screens cannot show (a limit, a delay, a price),
the priority. Never ask what the mockup already shows. A request with
nothing open gets no questions.

## 3. Cut it into cards

| Card | Holds | Template sections |
|---|---|---|
| Global card | the feature end to end, as the user lives it | user story, Description, the full User flow, the list of its sub-cards, end-to-end Test rows |
| Sub-card, one per screen | that screen and everything the user can do on it | its own user story, a short Description, its slice of the flow, Mockup with the capture, the full Action list, its Test rows |

- A feature with one screen is one card, no sub-card.
- A screen whose states differ in kind (an empty first run, an error
  wall, a paywall) may take a sub-card per state; a state that changes
  one label stays a line in its screen's Action list.
- A back-end piece with no screen (a webhook, a scheduled job, an email)
  is a sub-card of Type Tech, with its trigger, its inputs, its output
  and its failure cases in place of the Mockup.

## 4. Write the functional detail

Every sub-card's Action list covers, in product terms:

- each action: `I can <action>` → what happens, what the user sees, how
  long it takes when the time matters;
- each state of the screen: first use and empty, loading, success,
  error, no network, no permission;
- each rule with its number: limits, lengths, delays, prices, rounding,
  time zones;
- each field: required or optional, format, what an invalid value shows;
- what is out of scope, in one line, so a session does not build it.

Test rows are checks a person runs on staging: what to do, what to see.
At least one per action, one per error state, and one per rule with a
number. These rows become the acceptance journal's checks.

Write the spec in the language the user wrote the request in. Quote
every text the user of the product will read in the product's copy
language, as `BRAND.md` sets it. No stack, no file names, no code: the
dev session decides how. No secret, no real customer's data, ever.

## 5. Create the cards

1. Create the global card in Specs with the App Spec template id and its
   properties: Name (the feature, as the user would say it), Project,
   Type Feature, Priority (asked, else Next), Repos (app for logged-in
   screens, site for public pages, functions for data, rules or a third
   party), Design (the Claude Design link), Stage Spec.
2. Notion fills the template in after the page exists. Fetch the page
   until its sections appear, then fill each one with `update_content`,
   replacing the grey hint text and keeping the template's headings,
   button and Test table in place. Never replace the whole page.
3. Create each sub-card the same way, with Parent spec set to the global
   card, then list the sub-cards on the global card as page mentions, in
   flow order.
4. Captures: for each screen, upload the image (the Notion connector's
   file upload, or an attachment from a public URL) and place it in that
   sub-card's Mockup section. A screen with no image gets the Design link
   and a line saying the capture is missing; never draw one.
5. Test rows go into the card's Test table. If the connector cannot reach
   the table inside the page, write the checks as a to-do list right
   under it and say so.

## 6. Hand over

When every card is filled, set Stage to Ready on the global card and all
its sub-cards. A card with something only the user can answer stays at
Spec, and the question goes to the user in the chat.

Reply with one line per card (ID, name, link), the global card first,
then what is missing: a capture, a number, an answer.

## What not to do

- Do not change the template, the board's properties, stages or views.
  They belong to mainBrain's `docs/board.md`.
- Do not move a card past Ready. Questions, Building and the stages after
  them belong to the dev sessions (`product-board`).
- Do not create a card that duplicates one on the board: search Specs by
  name in the project first, and update the card you find while it sits
  at Idea or Spec.
