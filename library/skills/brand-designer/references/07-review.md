# 07 · Presentation, critique and the final exam

Trains how the designer shows options, reads feedback, critiques its own work and closes a job.
Produces `brand/<slug>/review.md`. Tags: `[fetched]` read at the URL given, `[secondary]` seen
through write-ups, `[anecdote]` reported by a third party, `[house rule]` a working rule of this
skill, `[unverified]` looked for and not confirmed.

## What the best do

- A competent professional shows two or three options with a rationale each. The best restate
  the brief and the criteria before any design appears.
- They warn that a new mark feels strange and that meaning arrives with use.
- They show every option at the same fidelity in the same real contexts, the smallest included.
- They recommend one option in the founder's terms, state what each option gives up, and leave
  the choice to the founder.
- They judge the idea before the craft, and the system in use before the mark alone.
- They test their own work with a reviewer who never saw the rationale, and they list what a
  human must still verify.

## Rules

1. **Frame before reveal.** Open with the brief and the criteria. Haviv opens by saying that
   love at first sight never happens with a new mark, and asks clients to set taste aside.
   (Logo Geek `[fetched]` https://logogeek.uk/podcast/sagi-haviv/)
2. **Few options, each a different idea, each one the designer would defend.** Rand presented
   one solution in a booklet. (`[fetched]`
   https://www.logodesignlove.com/paul-rand-logo-presentations) Two or three is the common
   professional range. (`[fetched]` https://www.logodesignlove.com/how-many-options) Bass
   explored about a hundred and showed around five `[anecdote]`. Johnson Banks offers a safe, an
   adventurous and a scary route `[secondary]`. The identity engine builds one to four sets,
   three by default. Never pad with a filler.
3. **Identical real contexts for every option.** Haviv shows finished designs in real
   applications, never sketches, and won approval for a rejected mark by returning with its full
   set of applications. (`[fetched]`, Logo Geek) Same contexts and same fidelity for each
   option keep the mock-up from deciding. `[house rule]`
4. **A trade-off for each option.** One sentence on what it gives up. `[house rule]`
5. **One recommendation, in the founder's terms.** Longevity, cost of change, fit with the
   brief; no design vocabulary. The firm argues its view and the client decides. (Haviv
   `[fetched]`, Logo Geek) The founder picks the set. The designer recommends one and never
   picks for them. No standing autonomy rule skips that checkpoint.
6. **Feedback is data about the goal.** Animal Planet asked for no blue and no elephant and
   accepted a blue elephant, because it met the stated aims. (Haviv `[fetched]`
   https://sixtysixmag.com/sagi-haviv/) Ask what a disliked element fails to do before changing
   it. Committees and relayed feedback: `<skill>/mark/references/presentation-delivery.md` §4.
7. **No merging on the designer's initiative.** `brand.py mix` runs on the founder's request
   alone: `<skill>/identity/references/cohesion.md`, "Mixing".
8. **Persuasion takes longer than drawing.** Scher sketched the Citi mark in the first meeting;
   accounts of the months spent convincing the client disagree. `[secondary]`
9. **Critique order.** The brief's idea first. Then Haviv's three questions in order: appropriate
   in feeling, distinctive enough to describe or doodle, simple enough for every size and
   medium. A failure on one disqualifies. (`[fetched]`, Logo Geek)
10. **Two hard gates.** The mark works in one colour and reads at a very small size. Rand names
    these, with attractiveness, as the firm requirements. He adds that literal fit to the
    business counts for less than people think. (`[fetched]`
    https://www.paulrand.design/writing/articles/1991-logos-flags-and-escutcheons.html)
11. **Every note carries a tag: idea or execution.** The remedies differ: a wrong idea returns
    to concept, a poor execution returns to the drawing. `[house rule]`
12. **First reactions are weak evidence**, the designer's own included. (Rand; Haviv `[fetched]`)
13. **Format.** Gates, findings, three fixes with measured effect and cost, no overall score:
    `<skill>/identity/references/critique.md`. Logo diagnoses:
    `<skill>/mark/references/critique.md`, "Common diagnoses and fixes". A rubric line reads
    "met / partly / not met" with its evidence. The lines never sum.
14. **A clean audit proves the absence of measured defects.** Scripts catch breakage; mediocrity
    passes them. `[house rule]`

## Procedure

Part A, at the board, before the pick:

1. Run `python3 <skill>/identity/scripts/brand.py build brand/<slug>`. Open `board.png`,
   `review.png` and `table.md`. Look before showing: `<skill>/identity/references/site-preview.md`,
   "Before showing the board".
2. Critique each set in the order of rules 9 to 11. Drop any set that fails a hard gate or that
   the designer would not defend; rebuild if fewer than two remain and the brief asked for a
   choice.
3. Write the message. Three lines of brief (problem, audience, the one idea), the criteria, the
   sentence on strangeness. Then the board path and one block per set in the shape of
   `<skill>/identity/ENGINE.md` §5, with a trade-off line added. Mark one set as recommended,
   give two reasons tied to criteria, name the runner-up and what would make it the better pick.
4. Stop. Wait for the founder. One checkpoint per job.
5. On feedback: restate it as a problem against the criteria, tag it idea or execution, answer
   with one change. Mix sets when the founder asks, and show the cohesion warning.

Part B, after delivery (cards 05 and 06 done):

6. Run every gate of cards 05 and 06 again. A failing line stops the review.
7. Fill the rubric. Each line gets a verdict and one piece of evidence: a file, a number, a
   render.

   | # | Line | Evidence to cite |
   |---|---|---|
   | 1 | One idea, visible in every element | the sentence; three elements that show it |
   | 2 | Different from the category | competitor map; logo-off result |
   | 3 | Colour has roles, pairs, both modes | palette audit, `tokens/swatches.html` |
   | 4 | Accessible | contrast and colour-vision gates, pair list |
   | 5 | System derives from the mark | geometry tokens in `system.md` |
   | 6 | Flexible | stress-test renders |
   | 7 | Real touchpoints at spec | `system/` and `kit/X/web/` listings |
   | 8 | Guidelines usable alone | the blind card from card 06 |
   | 9 | Delivery complete and labelled | use table against disk |
   | 10 | Governed | `rollout.md` inventory, owner, dates |

8. Run three blind tests. Launch a fresh subagent with no context for each, show rendered
   images, ask fixed questions, record the answers word for word.
   - Logo-off: "Which of these pieces come from the same brand?" among two controls.
   - Competitor swap: the system carrying a rival's name. "Does anything look out of place?"
   - One sentence: "Say in one sentence what this brand is about." Compare with the idea.
9. Name the three weakest applications. Fix or cut each.
10. Write the three fixes that matter most, each with what, measured effect, why and cost.
11. Write `brand/<slug>/review.md`:
    1. The brief's idea, one sentence
    2. Gates: passed, failed, not checked and why
    3. Self-critique: findings per component, each tagged idea or execution
    4. Rubric: ten lines, verdict and evidence, no total
    5. Blind tests: questions, answers, verdict
    6. Three fixes, most important first
    7. What a human must still verify

What a human must still verify, listed in section 7 of the file every time:
- Trademark clearance of name and mark.
- A print proof on the real stock; any Pantone or CMYK value, from the printer.
- Font licences bought for the uses the kit names.
- Cultural reading in each market and language.
- Recognition and preference with real customers.
- Store icon acceptance on each platform.
- The founder's own judgement of fit.

## Gate

A script or a count can check:
- [ ] The checkpoint message puts brief and criteria before the first set.
- [ ] Between one and four sets; each has an idea sentence, a trade-off and its checks.
- [ ] One set carries "recommended"; two or more reasons cite a criterion.
- [ ] The message and the review contain none of: like, love, nice, clean, modern, off.
- [ ] Every critique note carries an idea or execution tag.
- [ ] Ten rubric lines, each with a verdict and a cited artefact; no sum, no average, no grade.
- [ ] Three blind tests recorded with question and answer.
- [ ] `review.md` has the seven sections; section 7 has the seven items.

Judgement:
- [ ] No idea sentence could describe another set.
- [ ] The recommendation would survive the founder asking "why not the other one?".
- [ ] The competitor-swap result appears as the reviewer gave it, flattering or not.
- [ ] Each "partly" or "not met" line names its fix or its place on the human list.
- [ ] The review tests the output; it does not restate the intent.

## Drill

Write the checkpoint message for three sets, then critique a published identity in under 300
words. Pass when: brief and criteria precede any design; each idea sentence fits one set alone;
each set states a trade-off; one recommendation carries two criterion-based reasons; each
critique note names an element, a consequence and an idea or execution tag; no taste word
appears; a verdict and the most important change close the critique.

## Failure modes

- "Which do you prefer?" with no criteria.
- A filler option that the founder then chooses.
- Better mock-ups for the favoured option.
- A rationale built from symbolism nobody will perceive.
- Craft notes on a wrong idea; a checklist passed and the brief failed.
- Judging the hero render and skipping the 16 px tab.
- The model's own defaults: it presents near-identical options; it says all three are strong and
  recommends none; it writes flattering rationale with no trade-off; it changes direction at the
  first mild objection, or picks for the founder; it merges two sets unasked; it gives its own
  work uniform praise; it writes remarks that fit any logo; it scores every line the same; it
  critiques the code and never opens the render; it attributes a presenting method to a
  designer with no source for it.
