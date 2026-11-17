# Concepts and readings

Trains idea generation past the obvious, and reading a mark the way strangers will. Produces
`brand/<slug>/concepts.md`: cliché list, word map, 30 or more tagged one-line concepts, routes,
an accident hunt per finalist. Tags: `[fetched]` `[secondary]` `[house start value]`
`[unverified]`.

## What the best do

- They write the obvious answers down first and ban them. A competent professional skips the
  list and lets the first idea survive because nothing else arrived.
- They produce ideas by the dozen across different methods before any drawing. A professional
  sketches a few pages, picks three and refines.
- They present routes: three ideas that differ in what the mark is. A professional presents one
  idea in three weights.
- They judge a black silhouette and add colour last. A professional lets a palette carry a weak
  shape.
- They hunt for the worst reading of their own mark, rotated, mirrored and tiny, report it, and
  state which cultural checks a person did. A professional checks for rude shapes upright at
  full size and trusts the rationale.

## Rules

1. Purge first. Name the ten most obvious images for this sector and this name, and ban them. A
   banned image returns when a written twist makes it this brand's. The measured model
   defaults and the reflex test live in `<skill>/identity/references/ai-defaults.md`, and that
   card governs: a hit needs a concrete `why` in `defaults_used`, or the idea changes.
2. Quantity before refinement. Sketch until the possibilities run out (Haviv, Sixtysix,
   https://sixtysixmag.com/sagi-haviv/ `[fetched]`). The count of ideas before the tool opens
   matters more than drawing skill (Airey, process page `[secondary]`). One account has Saul Bass
   making about a hundred preliminary concepts before cutting to five (Lindon Leader's comment
   on Logo Design Love, read in research, anecdote).
3. The floor: 30 one-sentence concepts, no drawing, from five or more methods (`[house start
   value]`).
4. Methods, each concept tagged with one: `map` word map, `ladder` metaphor ladder, `letter`
   letterform mining, `pun` two-into-one, `limit` constraint round, `opposite` the mark the
   category would never use, `system` a behaviour first (a frame, a cut, a grid) with the mark
   falling out of it. A visual double meaning helps memory (Rand, 1988 interview `[secondary]`).
5. A route is a different idea. A weight, a colour or a rotation of the same idea is a variation
   and counts once.
6. Three routes go forward. They differ in idea and in mark type (wordmark, letterform, symbol:
   `field-notes.md` maps these to the engine's `logo.type` values);
   `<skill>/identity/references/cohesion.md` sets how the sets differ on the axes.
7. Each route becomes one set with its 4 to 6 best lines, and the engine builds one of them
   (`<skill>/identity/references/logo.md`, Process).
8. Silhouette before colour. No colour enters until a distinctive shape exists (Haviv, Logo Geek
   podcast, https://logogeek.uk/podcast/sagi-haviv/ `[fetched]`). A concept line that needs a
   colour, a gradient or an effect to work dies.
9. One-sentence test. Describe the concept in one sentence. Swap in a competitor's name. A
   sentence that still holds describes the category, so the concept goes.
10. Use decides meaning over time. A logo takes its meaning from the thing it stands for, and
    one-to-one symbolism is often impossible, so drop any demand that the symbol depict the
    business (Bierut, https://www.itsnicethat.com/features/michael-bierut-logo-design; Rand,
    https://www.paulrand.design/writing/articles/1991-logos-flags-and-escutcheons.html; both
    `[fetched]`).
11. Split every reading in three: the thing the mark shows, the thing it suggests, the thing it
    resembles by accident. Viewers find the third list, and the designer misses it. The stock
    examples are the word read in a fast-food collar and the belly read in a cola mark
    (`[secondary]`, anecdote).
12. Check translation and offence before commitment. The USPTO advises it for goods sold abroad
    (https://www.uspto.gov/trademarks/basics/strong-trademarks `[fetched]`).
13. No fixed colour-meaning table. Colour and symbol meanings are local, and the research found
    no reliable cross-cultural source (`[unverified]`). A native speaker checks them, or the
    line says "not checked".

## Procedure

Before drawing:

1. Open `brand/<slug>/concepts.md`. Write the ten clichés. Add the three category clichés that
   `<skill>/identity/references/ai-defaults.md` asks for if they are missing from your ten.
2. Run the word map on the one idea and on the name, per
   `<skill>/mark/references/discovery-brief.md` §6. Paste the branches and mark the drawable
   nouns and the intersections.
3. Look at the shelf so you know the category's habits:
   `PATH="$HOME/.cache/logo-design/bin:$PATH" python3 <skill>/mark/scripts/search_library.py
   --industry <industry>` (add `--type`, `--technique` or `--subject` to narrow). Run
   `bash <skill>/scripts/setup.sh` once per container first.
4. Write the long list: 30 lines or more, one sentence each, each with its method tag. Run
   three constraint rounds at least: a single shape, the name with no symbol, a 16 px square.
5. Strike every line that sits on the cliché list, needs colour, or passes for a competitor
   under rule 9. Keep the struck lines visible with the reason.
6. Cluster the survivors into routes and name each route in one sentence. Merge routes that
   share an idea.
7. Pick three routes that differ in idea and in mark type. Under each, list its 4 to 6 best
   lines and mark the one to build. Run the reflex test on each route. Card 04 takes over.

After `python3 <skill>/identity/scripts/brand.py logos brand/<slug>` has rendered the marks:

8. For each built mark, write the three lists of rule 11 before reading your own rationale.
9. Run the accident hunt on the symbol file (`brand/<slug>/sets/<X>/logo/symbol.svg`). The
   contact sheet gives 16 px, one colour and reversed. `python3
   <skill>/mark/scripts/preview_sheet.py <svg> -o preview.html` (same `PATH` prefix) gives blur,
   mirror and the 180 degree turn. For 90 and 270 degrees and the four quadrant crops, render a
   copy of the SVG with a `transform` on a wrapping group or a cropped `viewBox`. On the
   reversed view, read the ground as the figure. Write down every reading, however unfair.
10. Launch a fresh subagent with no context for each view that worries you. Show it the image
    and ask the fixed questions: "what do you see?" and "describe it in one sentence". Record
    the first answer word for word. Do not explain the mark to it.
11. Check each reading against anatomy, religious and political symbols, hate symbols, flags,
    hazard signs and famous logos.
12. Check the name: run together with no spaces, as initials, as a handle and a URL, and for
    meaning, slang and pronunciation in each launch language.
13. Write one line per market and audience group: checked and by whom, or "not checked" and who
    should. Your own reading of a language counts as "not checked by a native speaker".
14. Report the worst reading found per finalist and your verdict: acceptable, fix as the named
    defect of the round, or kill the route.

## Gate

A script or a count can check:

- [ ] `concepts.md` lists ten clichés and a word map.
- [ ] The long list holds 30 lines or more, one sentence each, with five or more distinct
      method tags.
- [ ] No surviving line holds a cliché-list word without a written twist, or names a colour,
      a gradient or an effect.
- [ ] Three routes, three different mark types, 4 to 6 lines under each, one marked to build.
- [ ] Each finalist has three lists: shows, suggests, resembles.
- [ ] Each finalist's hunt table has a cell for 90, 180, 270, mirror, reversed, four crops,
      16 px, blur and ground-as-figure, with five readings or more and one unflattering.
- [ ] The name appears run together, as initials and as a handle, and each market in the brief
      has a line saying checked and by whom, or "not checked".

Judgement:

- [ ] Each route sentence fails with a competitor's name in it and fails for the other routes.
- [ ] The routes differ in idea. Removing weight, colour and rotation leaves three things.
- [ ] Each built mark reads as a black shape at 16 px.
- [ ] The reflex test passes or the `why` is concrete, and one set uses no listed default.
- [ ] The worst reading is in the report with a verdict. Nothing found is the suspect result:
      run step 10 again on another view.

The work does not proceed while a line fails.

## Drill

Brief: a bicycle repair co-operative named "Spoke & Sons" in a town with two launch languages.
Produce `concepts.md` through step 7, build one mark, run steps 8 to 14 on it. Pass when: the
list holds 30 concepts from five methods; no survivor uses a wheel, a gear, a wrench or a chain
without a twist; the three routes have three mark types and three sentences that do not swap;
the hunt lists five readings with one unflattering; the second language has a line that says
who checked it or "not checked".

## Failure modes

- Refining the first idea when nobody wrote the tenth, or counting thirty variations of one
  concept as thirty concepts.
- Decorating a weak idea with a gradient, a shadow or a mockup.
- Believing the rationale: "it represents connection", so viewers will see connection.
- Hunting on the upright, full-size, full-colour view, or reading the SVG code and skipping the
  rendered image.
- Model defaults, by name: the abstract swirl, the hexagon, the four-point spark, the initial in
  a rounded square, the leaf for anything green, the upward arrow for anything financial, the
  blue-to-purple gradient, the rounded geometric sans. A model returns the most probable answer,
  which is the category average (`[secondary]`, qualitative). The measured list is in
  `<skill>/identity/references/ai-defaults.md`.
- The model's logo formula: the name's object plus a hidden letter plus negative space plus a
  circle, as symbol plus wordmark, three times. One may pass, with a reason from the brief.
- Inventing a meaning for each stroke, or stating that a colour or an animal means something in
  a culture with no source and no native check.
