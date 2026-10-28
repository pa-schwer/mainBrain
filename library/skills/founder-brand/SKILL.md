---
name: founder-brand
description: >-
  Your brand designer. Names the business (with the trademark, domain and handle
  checks to run before falling in love with a name), writes the voice, a one-line
  promise and a tagline, and briefs the look: colours, type, logo and the first
  things a customer sees, so they match the positioning the marketing director
  chose. Use when the user says "name my business", "brand this", "logo", "brand
  identity", "what should it look like", "tagline", or "brand voice".
argument-hint: "[name ideas, if any]"
---

# founder-brand

A brand is the promise a customer remembers. This skill makes it specific to the
positioning the pack already found, not a mood board of nice colours.

## Step 1: read the brief

`founder/idea.md`, `founder/marketing.md` (the positioning line and the first
audience), `founder/competitors.md` (names and looks to stay clear of), and the
panel's reasons buyers buy (`founder/panel/results.md`). If the positioning is
missing, ask for it or run `/founder-marketing` first.

## Step 2: name candidates

Ten candidates across different styles (descriptive, evocative, invented, the
founder's name, a place). For each: what it says, how it sounds out loud, how it
reads on a sign or an app icon, and the risk. Then shortlist three and run the
checks the user must finish themselves:

- **Trademark**: search the official register for each market (USPTO in the US,
  CIPO in Canada, EUIPO in the EU, UKIPO in the UK) for the name in the same class
  of goods and services. Give the search links and the classes to check.
- **Domain**: whether the .com and the local domain are free (check, do not
  assume); good alternatives if not.
- **Handles**: Instagram, TikTok, X, YouTube.
- **Confusion**: no name close to a competitor in `founder/competitors.md`.

Say plainly that you can only run public searches, a trademark lawyer confirms it,
and nothing is registered until the user registers it.

## Step 3: voice and promise

- The one-line promise (what the customer can count on, every time).
- A tagline, three options.
- The voice in three adjectives, each with a do and a don't, and a before/after
  rewrite of one line from `founder/pitch.md`.

## Step 4: the look, as a brief

- **Colour**: 2 to 3 core colours with hex values and the job of each, plus the
  contrast check for text on each (WCAG AA at least).
- **Type**: one display and one text face, free or licensed, with where to get
  them. No font the user does not have a licence for.
- **Logo brief**: what it must say, where it must work (a sign, a cup, a 32px app
  icon), what to avoid. Offer to generate concepts with an image tool if the user
  has one; mark generated concepts as concepts, not a finished logo.
- **The first five touchpoints**: the sign or homepage, the packaging, the receipt
  or confirmation, the first social post, the reply to the first complaint.

## Rules

- Never copy a competitor's name, logo, colours or tagline.
- No fonts, images or icons the user has no right to use.
- Not legal advice on trademarks.

## Output

`founder/brand.md`. Next: `/founder-ops` and `/founder-launch`.

<!-- LOCAL CHANGE (mainBrain): this addendum is not upstream. Strip it before updating from Jakeschincariol/founder-skill. -->

## Addendum: branding in a mainBrain project

Vendored from `Jakeschincariol/founder-skill` at commit `fd9385b`. This
section is the only local change, and it overrides the steps above where
they conflict.

**`founder/brand.md` is a proposal.** `BRAND.md` at the ops repo root
belongs to the founder, and a session never writes it from this file. The
founder reads the proposal and supplies `BRAND.md`, or names in the chat
the parts to copy into it verbatim.

**The look is a brief, not tokens.** Step 4's colours and faces go to the
design source (a Claude Design project, or impeccable's new-work where
ops installed it) as a brief. No value from it enters
`docs/design-system.md` or a `tokens.css` until that source settles the
tokens; site and app keep Tailwind's defaults until then, and the static
UI source (`ui-ux-pro-max`, or `impeccable`) stays the one advisor there.

**The logo brief goes to `logo-design`** where ops installed it, and this
skill draws no concept: that skill owns the mark. Without it, logo
concepts stay in `founder/`, marked as concepts, and none ships in a
product repo.

**The trademark check is a script, run before the shortlist.**
`scripts/tm-screen.py NAME [NAME ...] --json founder/trademark-screen-<date>.json`
queries the USPTO's own trademark index (one JSON request per name, no
key, no browser) and answers BLOCKED, WATCH or OPEN per name: the live
marks that contain the word, the exact-word marks in any class, the
marks in the classes of interest whose goods name the product's field,
and the one-letter neighbours that do. Set `--classes` and `--probe` to
the product (the defaults fit software, answering and legal services).
Run it on every candidate before the shortlist, and again on the pick
before anyone falls in love with it; check nicknames and translations by
hand, since an edit distance misses them. A BLOCKED name leaves the
list. An OPEN name is a candidate for the attorney's search, not a
clearance: the script reads word marks in the federal register only, no
design marks, no state registers, no unregistered use. The records it
saves are the proof the handoff asks for.
