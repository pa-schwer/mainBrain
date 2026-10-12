---
name: write-spec
description: Write a product spec the way the Notion product board expects it - one global card and one sub-card per screen, the right Project, Stage Ready, the App Spec template, every behaviour spelled out, a capture of each screen - and put it on the board, or hand it over as paste-ready cards where Notion is out of reach (Claude Design). Use whenever the user asks for "une spec", "des specs", "spécifie", "fais la spec de ...", "mets ça dans le board", "crée la carte Notion", "ajoute ça au board", "write a spec", "spec this", "put it on the board", or wants a Claude Design mockup, prototype or handoff turned into cards.
---

# Write a spec

You turn a feature, a mockup or a Claude Design handoff into cards for
the product board, ready for a dev session to build. The board is the
Specs database in Notion, under the page "Product Dev". Dev sessions
build from the cards with the `product-board` skill; this file holds
everything writing them needs, so it works where that skill is absent.

## 0. Where you run

| Where | How you reach the board | What you deliver |
|---|---|---|
| Claude Code, in a project's ops repo | `CLAUDE.md`, section "Product board": the project's page and the Specs data source | the cards, in Notion |
| A chat or session with the Notion connector (claude.ai, mainBrain) | search Notion for "Product Dev", fetch it, take the Projects and Specs data sources from its child databases | the cards, in Notion |
| No Notion tool (Claude Design, a chat without the connector) | none | the cards as paste-ready text, section 7 |

With Notion, find the project in Projects by name or Slug. A project
missing from Projects is a question for the user, not a row to invent.
Fetch the Specs data source once and keep the App Spec template's id
from its `<templates>` list (with several, the one named App Spec).

## 1. The card, as the board defines it

Properties you set: Name, Project, Type (Feature, Fix, Tech), Priority
(Now, Next, Later), Repos (ops, site, functions, app, lib), Design (the
Claude Design link), Parent spec (on a sub-card: its global card), Stage.
Every other property belongs to the dev sessions.

The page follows the App Spec template, in this order:

| Section | Holds |
|---|---|
| 👤 I'm / 👉 I need / 🎯 To | the user story, three lines |
| 📋 Description | the need, the pain, how this story answers it |
| 🌀 User flow | the path through the feature, step by step |
| 🎨 Mockup, Action list 👇 | the capture of the screen, then every "I can ..." with its expected behaviour |
| ✅ Test | the checks a person runs on staging |

## 2. Read before asking

Read everything the user gave first: the mockup, the Claude Design
project or handoff, screenshots, the description in the chat. In a
project repo, read `BRAND.md` and `docs/product.md` too.

Then ask, in one batch, only what would change the cards: who the user
is if the mockup does not say, the outcome that proves the feature works,
a rule or a number the screens cannot show (a limit, a delay, a price),
the project and the priority if nobody said. Never ask what the mockup
already shows. A request with nothing open gets no questions.

## 3. Cut it into cards

| Card | Holds |
|---|---|
| Global card | the feature end to end: user story, Description, the full User flow, the list of its sub-cards, end-to-end Test rows |
| Sub-card, one per screen | that screen: its own user story, a short Description, its slice of the flow, the Mockup with the capture, the full Action list, its Test rows |

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
number. Dev sessions turn these rows into the acceptance journal.

Write the spec in the language the user wrote the request in. Quote
every text the product's user will read in the product's copy language
(`BRAND.md` in a project repo, else ask). No stack, no file names, no
code: the dev session decides how. No secret, no real customer's data.

## 5. Create the cards (with Notion)

1. Create the global card in Specs with the App Spec template id and its
   properties: Name (the feature, as the user would say it), Project,
   Type Feature, Priority (asked, else Next), Repos (app for logged-in
   screens, site for public pages, functions for data, rules or a third
   party), Design, Stage Spec.
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
6. Search Specs by name in the project before creating: a card that
   already exists at Idea or Spec gets filled, not duplicated.

## 6. Hand over (with Notion)

When every card is filled, set Stage to Ready on the global card and all
its sub-cards. A card with something only the user can answer stays at
Spec, and the question goes to the user in the chat.

Reply with one line per card (ID, name, link), the global card first,
then what is missing: a capture, a number, an answer.

## 7. Paste-ready cards (without Notion)

Deliver one block per card, the global card first, each block in the
template's order so it pastes into a card made from the App Spec
template:

```
# <Feature name>  ·  global card
Project: <project> · Type: Feature · Priority: <Now|Next|Later> · Repos: <...> · Design: <link>
**👤 I'm :** ...
**👉 I need :** ...
**🎯 To :** ...
### 📋 Description :
...
### 🌀 User flow :
1. ...
### 🎨 Mockup :
Capture: <which screen to export>
**Action list 👇**
- I can ... → ...
### ✅ Test :
- [ ] <do this> → <see this>

# <Screen name>  ·  sub-card of <Feature name>
...
```

In Claude Design, name the screen to export for each sub-card's Mockup,
and put these blocks in the handoff to Claude Code: a session that
receives them with Notion creates the cards by sections 5 and 6. End
with the list of what is missing, as in section 6.

## What not to do

- Do not change the template, the board's properties, stages or views.
  They belong to mainBrain's `docs/board.md`.
- Do not move a card past Ready. Questions, Building and the stages after
  them belong to the dev sessions (`product-board`).
