# The exam

Three checks, from cheapest to dearest. Run them after any change to
this bundle.

## 1. Smoke: the engines run and meet

```bash
bash <skill>/evals/smoke.sh
```

Ends with `brand-designer smoke passed`. It builds the identity
engine's example brand, makes a kit, then has the mark engine audit the
kit's symbol and export the web icons from it. One minute, network for
the fonts.

## 2. Drills: one competency at a time

Each card in `references/` closes with a drill and its pass criterion.
Give a fresh subagent the card, the engine files the card points to and
the drill; grade its output against the criterion with a second
subagent that saw neither the card nor the first one's reasoning. A
drill that fails names the line of the card to rewrite.

## 3. The full run: `evals.json`

Four briefs on invented businesses. A fresh subagent gets the skill
folder and one prompt, works in an empty folder, and stops at the
checkpoint. A second subagent, shown the files and the board and none
of the reasoning, checks each expectation and reports it met, partly
met or not met with the file that proves it. No total: one expectation
not met is a finding to fix in a card.

The blind tests of `references/07-review.md` belong to this pass: the
logo-off test, the competitor swap and the one-sentence summary.

Briefs name invented companies. A likeness to a real one is an
accident.
