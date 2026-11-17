# Field notes

What the first full run of this skill taught, on a brief with no
founder to answer. Read it once before a run. Each note settles a
point the cards left open or names a quirk of an engine.

## When something the cards ask for cannot be done

- **No founder.** The intake message is not sent. The assumptions go
  at the top of `brief.md`. A gate line that needs the founder's
  reaction reads "not assessed: founder absent".
- **No file to read.** A project with no `docs/product.md`, `BRAND.md`
  or `founder/brand.md` is common at the start. Record the absence in
  `brief.md` §1 and work from the request.
- **No subagent.** The blind tests need a fresh reader. A session that
  cannot launch one writes "not run: no second reader" in `review.md`
  and repeats it in the checkpoint message. The readings stay yours
  and are labelled yours.
- **No register search.** A figurative search of a trademark register
  wants a person. Log "not searched" with the reason and say so at the
  checkpoint. Where `founder-brand` is installed, its `tm-screen.py`
  screens the name.
- **Nothing in the libraries.** Both reference libraries lean to
  technology. A sector they do not hold (the sea, sport, food) returns
  nothing: say so in `audit.md` and rely on the brands you audited.
- **A site that blocks the browser.** Log it as blocked. Audit what is
  visible (an app icon, a store listing) and name the gap.

A step skipped for one of these reasons is reported, never passed in
silence. The checkpoint message carries the list.

## Order of the first steps

The brief and the audit feed each other. Write `brief.md` sections 1
to 9 first; run the audit; then write sections 10 to 12 (ideas, axes,
criteria) and run `brand.py init … --force` with the competitors the
audit named.

## Where files go

- `brand/<slug>/marks.md`: per mark the type, the reason, the 16 px
  reduction, the constants; then the results table of card 04.
- `brand/<slug>/tests/`: sheets you build to look at the marks
  (transforms, small sizes, the shelf).
- Rivals' logo files and screenshots you collect by hand:
  `~/.cache/brand-designer/<slug>/`, outside the repository. The
  screenshots `brand.py site competitors` writes under
  `brand/<slug>/site/` stay where the engine put them; the ops repo is
  private.
- The audit's colour and type maps are tables in `audit.md`, built
  from `brand/<slug>/site/competitors.json`. No command draws them.

## Showing the work

A path inside a container opens nothing for the founder. Send
`board.png` itself with the checkpoint message: attach the file where
the session can, else commit `brand/<slug>/` on a branch of the ops
repo and link the image.

## Seeing a sheet

`preview_sheet.py` writes HTML. To look at it:

```bash
PATH="$HOME/.cache/logo-design/bin:$PATH" python3 <skill>/mark/scripts/render_png.py \
  brand/<slug>/tests/preview.html -o brand/<slug>/tests/preview.png --width 1400 --height 9000
```

A page taller than the height is cut: raise it until the shelf section
shows. Pass the sheet `brand/<slug>/sets/<X>/logo/build/master-symbol.svg`;
a wordmark-only set has `master-primary.svg` and
`master-symbol-small.svg`. For the 90 and 270 degree turns and the
quadrant crops, write one HTML page that shows the mark under CSS
transforms and screenshot it the same way.

`svg_audit.py` prints a score out of 100. Read its findings and leave
the number out of every report.

## Quirks of the identity engine

- **Mark types.** `logo.type` takes `wordmark`, `symbol+wordmark`,
  `symbol` or `monogram`. A letterform route is `symbol+wordmark` or
  `monogram` with a `letterform` tag. It tends to draw the
  `literal-object` and `hidden-letter` flags: answer them in
  `defaults_used` with the reason from the brief.
- **Flag ids.** The build prints a logo flag with a `logo-` prefix
  (`logo-literal-object`); `defaults_used` accepts the tag with or
  without it.
- **Axes.** `brand.py init` has no flag for them. They live in each
  set's `identity.axes` as a name and a position from -2 to 2; the
  names are the six of `identity/references/cohesion.md`. The
  `cohesion.sets-close` warning compares pairs of sets: two sets that
  sit together on every axis fire it, and a further axis on which they
  differ clears it.
- **Rounds.** A round is one look at the contact sheet and one named
  defect fixed. The first `brand.py logos` run that produces
  `wordmark-glyphs.json`, so that a detail can be placed, is round
  zero. A rerun to clear a gate or an info line counts as none.
- **Placing a wordmark detail.** `wordmark-glyphs.json` gives each
  letter's x range and stems. For a y extent (the dot of an i), read
  the paths in `logo/build/master-wordmark.svg`.
- **The role `text` is a tinted neutral.** A wordmark that must carry
  the brand ink takes a brand id (`brand-1`, `brand-2`) in
  `logo.colors`, with `palette_build.neutral_tint` set when the neutral
  should lean the same way.
- **`card.ground`** is `identity.card.ground`. The attributes of a
  small mark built from a glyph (`data-glyphs`, `data-cap`, `data-x`,
  `data-baseline`, `data-anchor`) are shown in
  `identity/templates/sets.example.json`, set B.
- **Case.** No command renders a name in two cases side by side. When
  the choice is open, build once with each `case` and compare the two
  contact sheets; that comparison is no round.
- **"Positioning falls back to the brief"** from `site competitors`
  means the engine could not read a rival's positioning from its page
  and used your brief's sector and attributes in the comparison.
