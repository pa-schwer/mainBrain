# Mark and type craft

Trains the drawing: mark type, construction, optical corrections, small cut, wordmark, brand
type, lockups, tests. It writes `brand/<slug>/marks.md`: per mark the type, the reason, the 16 px
reduction and the constants, then the results table. The rest of its evidence is the contact
sheet, the audits and the build gates. Tags: `[fetched]` `[secondary]` `[house start value]`
`[unverified]`.

## What the best do

- They argue the mark type before drawing, often recommend no symbol, and design the 16 px
  reduction with the full mark. A competent professional picks the type from habit and shrinks
  the master later.
- They declare module, weights, radii and angles, draw inside them, then break the grid where
  the eye disagrees and say which rule each break serves. A professional stops at the grid.
- They start letters from a real face and make one move that comes from the name. A
  professional types the name, tracks it out and ships.
- They draw the reversed version and the small cut as their own drawings.
- They run a fixed battery on several candidates and kill candidates on the results. A
  professional tests the favourite, in colour, at full size, in a mockup.

## Rules

1. Choose the type before drawing. Write one sentence of why (name length, name distinctiveness,
   a real touchpoint) and one sentence on the 16 px reduction. Defaults below are a `[house
   start value]`; `<skill>/mark/references/mark-types.md` §12 has the full guide and governs.

   | Situation | Default type |
   |---|---|
   | Short, unusual name (6 to 7 letters) | Wordmark, with a letterform cut for the icon |
   | Long name or several words | Symbol plus wordmark, or monogram |
   | App-first product | Symbol or letterform, drawn inside the icon tile first |
   | Many sub-brands | System mark: one constant container or module, typed names |
   | Product stamp, food, craft, sport | Emblem plus a simplified small cut |
   | Name is a concrete noun | Pictorial mark of that noun, unlike the stock drawing |
2. A logo identifies. It needs to work in one colour and at very small sizes (Rand,
   https://www.paulrand.design/writing/articles/1991-logos-flags-and-escutcheons.html
   `[fetched]`). "Wordmark only" is a legitimate answer.
3. Draw symbols the identity engine's way: `viewBox="0 0 100 100"`, filled primitives, real
   booleans with `data-op`, colour roles with `data-color`, no `<text>`
   (`<skill>/identity/references/logo.md`, "SVG construction", governs). For path-writing
   technique alone, read `<skill>/mark/references/svg-construction.md` §3.
4. Declare the constants in words before the first shape: module `u` (3 or 4 units on the 100
   grid), stroke weights, up to three radii, and one angle family beside 0 and 90. A fourth
   non-orthogonal angle needs a written reason (`[house start value]`). Concentric corners
   share a centre: inner radius equals outer radius minus stroke.
5. The grid guides and the eye decides last (Logo Geek, https://logogeek.uk/?p=2617; Typographica,
   https://typographica.org/on-typography/is-what-i-see-what-i-get-math-and-optics-in-type-design;
   both `[fetched]`). Show no construction circles that the final paths do not obey.
6. Primitives are for symbols. Letterforms come from a real open-license face, outlined. Letters
   built from circles and rectangles read as a toy: no overshoot, clogged joins, uniform weight.
   A founder who names Notion or Apple as a reference rejects them on sight.

Optical corrections, rules 7 to 12: the numbers are start values and flags. The amounts come
from the set's display font at kit stage, its O/H ratio for overshoot and its crossbar/stem
ratio for horizontals (`<skill>/identity/references/logo.md`, "Optical corrections"). Read the
why in `<skill>/mark/references/visual-techniques.md` §3; against its percentages the font wins.

7. Overshoot: rounds pass flat heights by 1 to 3 %; Karow gives 3 % for O and 5 % for the apex
   of A (https://en.wikipedia.org/wiki/Overshoot_(typography), citing Karow `[fetched]`).
   Points need more than rounds, flat curves less (Frere-Jones, Typeface Mechanics 001, mirror
   https://stockholmstypografiskagille.se/typonyheter/typeface-mechanics-001/ `[fetched]`).
8. Horizontals thinner than verticals. Hoefler's even-looking square has verticals close to 7 %
   thicker (`[secondary]`); other tests report less, so flag anything outside 2 to 7 %
   (Typeface Mechanics 002, mirror
   https://stockholmstypografiskagille.se/typonyheter/typeface-mechanics-002/; Edmondson,
   https://ohnotype.co/blog/ohno-type-school-h; both `[fetched]`).
9. Junctions: taper strokes into a join, more for an acute angle (Typeface Mechanics 002).
   Start at 8 to 20 % thinner (`[house start value]`) and cut a notch in the small cut.
10. The optical centre sits above the geometric one (Typographica `[fetched]`). Raise midlines
    1 to 3 % of height (`[house start value]`); centre lopsided shapes by mass (`[unverified]`).
11. A circle beside a square of equal height looks small. Material's keylines pair a 152 dp
    square with a 176 dp circle (`[secondary]`). Start 13 to 16 % larger (`[house start value]`).
12. Irradiation: white on dark looks heavier (Logo Geek `[fetched]`, no number given). Before
    the pick the engine reuses the positive paths: judge the reversed row of the contact sheet
    at 32 px and name the defect when it looks heavier. The lighter drawing is kit-stage work,
    an inset of 1 to 2 % of the stroke width to start (`[house start value]`).
13. Gaps are strokes. The narrowest gap measures 0.8 of the narrowest stroke or more (`[house
    start value]`). Design each counter as a shape. A second reading is a bonus: the mark works
    when a viewer misses it (`[unverified]`).
14. The small cut is a separate drawing in `symbol_small_svg` or `logo.monogram`: heavier, more
    open, fewer parts. At 16 px, main strokes cover 2 px or more (12.5 units on the 100 grid),
    gaps 1 px or more (`[house start value]`). The engine refits the small cut to its ink box, so
    pixel alignment set on the grid does not survive: the 16 px render is the judge. Thin lines
    and text die in small icons (Apple HIG,
    https://developer.apple.com/design/human-interface-guidelines/app-icons.md `[fetched]`).
15. The pipeline outlines the wordmark from the set's display face. You add one ownable detail
    in `wordmark_detail_svg`, taken from the name: a ligature across a real problem pair, a cut
    that repeats, one customised letter, a counter that carries the idea (`[unverified]`
    pattern). Then re-correct every weight and space the move touched.
16. Space by equal white. The gap between two stems echoes the counter of n or H; check letters
    three at a time (Edmondson, https://ohnotype.co/blog/ohno-type-school-n `[fetched]`). Flag
    white areas more than 10 % off the mean (`[house start value]`).
17. Caps get 5 to 12 % letterspacing (Butterick,
    https://practicaltypography.com/summary-of-key-rules.html `[fetched]`): `tracking` 50 to
    120 in the engine's 1/1000 em. Lowercase sits near zero (`[unverified]`).
18. Check the problem pairs by eye: AV, AT, AY, LT, LY, TA, To, Ty, Va, Wa, Yo, ry, rt, and
    any pair with an open side (`[unverified]` list).
19. Case is a shape decision. Set the name in caps and in lowercase and compare silhouettes
    before choosing `case` (`[unverified]`).
20. OFL fonts: the FAQ allows logos with no extra permission (1.1), gives you the derived
    artwork (1.1.1) and keeps it outside the licence (1.13) (https://openfontlicense.org/ofl-faq/
    `[fetched]`). Other licences go through the gate in `<skill>/identity/references/type.md`.
21. Brand type in five lines; `<skill>/identity/references/type.md` governs selection, pairing,
    coverage and licences.
    - Constraints first: languages, sizes, weights, licence, web budget. Taste comes after.
    - Text face first, display second. One family with axes before a second face.
    - Body 15 to 25 px, line spacing 120 to 145 %, 45 to 90 characters (Butterick `[fetched]`).
    - Tabular figures wherever numbers align.
    - The wordmark beside the text face is related or in clear contrast. A near-miss fails.
22. Lockups derive from one named unit, the cap height. Align the symbol to the cap-height band
    with overshoot; bounding boxes mislead. The pipeline computes this
    (`<skill>/identity/references/logo.md`, "Lockups and system").
23. One colour first. Run the full battery on each candidate before polishing one. One named
    defect per mark per round, two rounds at most. No overall score.

## Procedure

1. Once per container: `bash <skill>/scripts/setup.sh`. Mark-engine commands below take
   `PATH="$HOME/.cache/logo-design/bin:$PATH"` in front.
2. For each of the three routes from `brand/<slug>/concepts.md`, list the three smallest and
   three largest real uses, then write the type, the reason and the 16 px reduction.
3. Study how real marks solved the same problem: `python3
   <skill>/mark/scripts/search_library.py --type … --technique … --subject … --industry …`.
4. Write the constants, then the symbol, into the set (`symbol_svg`). Set `case` and
   `tracking`, add the one detail, add the small cut.
5. `python3 <skill>/identity/scripts/brand.py logos brand/<slug>`. Look at the contact sheet:
   large, 32 px, 16 px, one colour, reversed. Judge the one-colour row first. For the 1-bit
   row of the table, a feature that survives at 32 px as grey pixels alone fails.
6. Run the eye tests of `<skill>/mark/references/testing-checklist.md` §3 on each mark: mirror,
   rotation, unintended readings, letter test, junction check. For the sheet with blur, mirror
   and the shelf: `python3 <skill>/mark/scripts/preview_sheet.py <svg> --refs-industry X -o
   preview.html`, then look at it.
7. `python3 <skill>/mark/scripts/svg_audit.py <svg>`. Its findings are advice; on canvas size
   and colour on elements the identity engine's convention wins.
8. Blind recall: launch a fresh subagent with no context, show it the rendered mark and ask
   "what do you see?" and "describe it in one sentence". Give that sentence to a second fresh
   subagent with the three candidates and ask which one it describes. For a wordmark, also
   ask "is this just typed in a font?".
9. Fill the results table. Name one defect per mark in `logo.defect`, fix it, run `logos`
   again, look again. Stop after two rounds; a third clears a gate or a cliché reading.
10. `python3 <skill>/identity/scripts/brand.py build brand/<slug>` and fix the failing gates.
11. After the founder's pick, make the optical corrections at kit stage with the font's
    ratios; rules 7 to 12 flag a zero or an out-of-range amount.

Results table, one column per candidate, pass or fail with the evidence in a few words:

| Test | A | B | C |
|---|---|---|---|
| One colour, black on white | | | |
| Reversed: same weight as the positive at 32 px | | | |
| 16 px and 32 px (small cut) | | | |
| Blur: silhouette holds | | | |
| Mirror | | | |
| Rotation 90 and 180 | | | |
| 1-bit at 32 px: parts keep their count | | | |
| Shelf line-up | | | |
| Blind recall | | | |

## Gate

A script or a count can check:

- [ ] Each mark has a written type, reason and 16 px reduction.
- [ ] The symbol uses the 100-unit canvas, `data-op`, `data-color`, and holds no `<text>`.
- [ ] The declared radii, weights and angles match the ones in the file.
- [ ] Each set has a small cut; its main strokes measure 12.5 units or more.
- [ ] The narrowest gap is 0.8 of the narrowest stroke or more.
- [ ] A wordmark-only set has one detail, no more, and a designed small mark.
- [ ] The font's licence is on record and covers a logo outline.
- [ ] `brand.py logos` rendered, `svg_audit.py` ran, `brand.py build` passes its gates.
- [ ] The results table has a cell filled for each test and each candidate.
- [ ] Each mark went through two rounds at most, one named defect per round.

Judgement:

- [ ] The mark reads in one colour before any palette touches it.
- [ ] The small cut is clearer at 16 px than the master scaled down, and is the same mark.
- [ ] The reversed version looks the same weight as the positive one at 32 px.
- [ ] No letter reads as another letter; no join clogs.
- [ ] On the shelf, a glance finds the mark and confuses it with no neighbour.
- [ ] The blind subagent's sentence picks the right candidate, and for a wordmark it points to
      the custom move.
- [ ] You can say why each untouched letter stayed untouched.

The work does not proceed while a line fails.

## Drill

Invented name "Tavory" (six letters, with the pairs Ta and av). Build three candidates of
three types: a wordmark with one detail, a letterform, a symbol. Run the procedure through
step 9. Pass when: the table holds a result in each cell; the evidence eliminates one
candidate; no file holds `<text>`; the blind subagent points to the wordmark's custom move;
the recall test picks the survivor; the survivor's small cut keeps 2 px strokes at 16 px.

## Failure modes

- A symbol added because "logos have symbols". The model pairs symbol and wordmark in 97 to
  100 % of its answers (`<skill>/identity/references/ai-defaults.md`, A7).
- The model's defaults: an initial in a rounded square, a hexagon, a speech bubble, a spark,
  a swoosh, a gradient blob, the literal pictogram of the sector.
- Letters assembled from `<circle>` and `<rect>`, or the name typed in a popular geometric
  sans, tracked out, untouched.
- Five corner radii and near-equal angles from nudging; golden-ratio circles drawn afterwards.
- Bounding-box alignment of a round symbol: it looks small and high.
- One SVG for all sizes, the lockup squeezed into a favicon, the positive paths reused for
  white on dark.
- A correction strong enough to see, or absent. A third round that breaks a part that worked.
- Testing the favourite alone, or showing a mockup in place of a test.
- Claiming the mark is unique with no search run. Say the trademark search is the founder's.
