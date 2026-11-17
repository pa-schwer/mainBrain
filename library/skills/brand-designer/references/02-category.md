# Category: the shelf, the codes and the look-alike screen

This card trains the category audit and distinctiveness. It produces `brand/<slug>/audit.md`,
including its "Look-alike screen" section. Source tags: `[fetched]` the page was opened and the
claim is on it; `[secondary]` known through summaries of the source; `[house rule]` this skill's
own rule.

## What the best do

- A competent designer pins a few rivals' logos on a board. The best map the whole set: direct
  rivals, substitutes, the leader, and brands the audience admires outside the category.
- A competent designer notes "lots of blue". The best count, name each code, and split codes
  that tell a buyer what kind of thing this is from codes that are habit.
- A competent designer aims to differ. The best write the decision per code (keep, break, avoid)
  with a reason, then one white-space sentence the table can prove false.
- A competent designer checks that a mark looks new to them. The best describe its dominant
  element in five words and search for it before the founder sees the mark.
- A competent designer redesigns what bores the team. The best inventory the assets buyers may
  know and keep them unless evidence shows them weak.
- The best say in plain words that their screen is not legal clearance.

## Rules

1. Audit the set. One rival tells you nothing about the category's shared look.
   (Brand-semiotics practitioner articles `[secondary]`)
2. Label each code residual (the past), dominant (the mainstream) or emergent (new). Aim near
   emergent; use residual when heritage is the idea. (Practitioner articles after Raymond
   Williams `[secondary]`; the primary text was not checked)
3. When the set goes one way, go the other, provided buyers value the difference.
   (Marty Neumeier, Zag `[secondary]`)
4. Uniqueness comes before fame. An element that evokes several brands works for the rivals,
   however well known it is. (Ehrenberg-Bass Institute, "Brands of Distinction",
   https://marketingscience.info/brands-of-distinction `[fetched]`)
5. A new asset starts with no fame and no uniqueness. Design can make it unique and easy to link
   to the name; consistent use over years builds the rest. Tell the founder so.
   (Ehrenberg-Bass, same URL `[fetched]`)
6. Inventory existing and retired assets before changing anything. The same source reports
   Tropicana reversing its 2009 packaging within a month, after an estimated $26.3m sales loss.
   (Ehrenberg-Bass, same URL `[fetched]`)
7. Trademark strength runs from fanciful (invented) through arbitrary and suggestive to
   descriptive (weak) and generic (no protection). Prefer ideas from the strong end.
   (USPTO, "Strong trademarks",
   https://www.uspto.gov/trademarks/basics/strong-trademarks `[fetched]`)
8. Confusion turns on two things: similarity of the marks and relatedness of the goods or
   services. Marks can conflict by sound, appearance, meaning or overall impression; two marks
   with the same dominant design element can conflict even when one adds words. Compare by
   dominant element and overall impression. (USPTO, "Likelihood of confusion",
   https://www.uspto.gov/trademarks/search/likelihood-confusion `[fetched]`)
9. Screen each shortlisted mark before the person who decides sees it, so nobody falls for a
   mark they cannot own. Final clearance stays with a trademark professional.
   (Sagi Haviv, Logo Geek podcast, https://logogeek.uk/podcast/sagi-haviv/ `[fetched]`)
10. Keep the cues that let a buyer recognise the kind of product; break the cues that make
    brands interchangeable. High customer risk argues for staying near the code: see "Worth
    asking" in `<skill>/identity/references/discovery-brief.md`. (`[house rule]`)

## Procedure

1. List 8 to 15 brands in four roles: direct competitors, substitutes (including the habit the
   buyer has today), the category leader, one or two admired outsiders. Start from `brief.md`
   and the intake answers; fill gaps with web search.
2. Collect each brand's real mark with web fetch, from its own site. Look at it. Record the URL;
   describing a mark from memory does not count.
3. Read the sector's conventions in the reference library (run `bash <skill>/scripts/setup.sh`
   once per container):
   `python3 <skill>/mark/scripts/search_library.py --industry X --summary`. The library leans
   toward technology brands (`<skill>/mark/references/library-guide.md`); for other sectors
   the marks you collected carry the audit.
4. Fill the marks table, one row per brand: mark type, dominant hue, type class, symbol subject,
   container shape, tone, dominant element in five words.
5. Count each column. A value shared by more than about a third of the set is a category code
   (`[house rule]`). Name each code and label it per rule 2.
6. Decide per code: keep (it signals the category), break (habit), avoid (one rival owns it).
   Write the reason in one line.
7. Write the white space in one sentence: "No one in this set is ___." The table must be able to
   prove it false.
8. Inventory the brand's own assets: name, colours, symbol, type, shapes, tagline. For each,
   note years in use and consistency. Mark each "keep unless proven weak" or "free to change".
   Fame and uniqueness need a survey of category buyers; you cannot compute them, so say which
   claims are untested.
9. Place the name and each symbol idea on the strength spectrum (rule 7). A descriptive or
   generic result goes in the audit as a weakness. You do not rename: BRAND.md owns the name,
   and `founder-brand` ships the USPTO name screen (`tm-screen.py`).
10. Colour and type maps belong to the engine. Run
    `python3 <skill>/identity/scripts/brand.py site competitors WORK url…` (up to 8 rivals) and
    `python3 <skill>/identity/scripts/search_library.py --industry X --summary`, then follow
    "Competitor map" and "Near colour = same colour" in `<skill>/identity/references/color.md`
    and "Competitor type map" in `<skill>/identity/references/type.md`. That library holds
    colours; do not query it for marks. Link the results from `audit.md`.
11. Later, when marks exist, run the shelf test on each shortlisted one:
    `python3 <skill>/mark/scripts/preview_sheet.py … --refs-industry X -o preview.html`.
12. Run the look-alike screen on each shortlisted mark, before the founder sees it:
    - Write the dominant element in five words ("circle split by diagonal bar").
    - Search that description and the symbol subject in four places: the marks table; the
      library, `python3 <skill>/mark/scripts/search_library.py --subject X`; the web, with the
      sector added to the query; the public registers by hand (USPTO, EUIPO, WIPO Global Brand
      Database) for the classes and countries the brand trades in.
    - Log each search: date, source, query, nearest match, its sector. A source you could not
      reach goes in the log as "not searched".
    - Decide. Same sector plus same dominant element: drop the mark or redraw it. Different
      sector: note it and go on.
13. Write `brand/<slug>/audit.md` with these sections, in this order:

```
# Category audit: <name>
## 1. Set                 (table: brand | role | site | mark URL)
## 2. Marks               (table: brand | mark type | hue | type class | subject | container |
                           tone | dominant element)
## 3. Counts              (each column's values with their counts, out of N)
## 4. Codes               (table: code | count | residual/dominant/emergent | keep/break/avoid |
                           reason)
## 5. White space         (one sentence)
## 6. Existing assets     (table: asset | in use since | consistency | decision | tested?)
## 7. Strength            (name and each symbol idea on the spectrum)
## 8. Colour and type     (links to the engine's competitor maps; no copy of them)
## Look-alike screen      (per shortlisted mark: dominant element, search log, near matches
                           with sector, verdict)
## Limits
```

"Limits" carries this sentence, word for word: "This is a designer's knockout screen. It is not
legal clearance. A trademark professional clears the name and the mark before filing or launch."
Repeat it in the message that shows marks to the founder.

## Gate

The work does not proceed while a line fails.

A script or a count can check:
- [ ] The set holds 8 to 15 brands, with one or more in each of the four roles.
- [ ] Each brand has a mark URL and a full row in the marks table.
- [ ] Three or more codes carry a count, a label and a keep, break or avoid decision with reason.
- [ ] The white-space sentence exists and names a value absent from the marks table.
- [ ] Each existing asset has a decision; untested claims carry the word "untested".
- [ ] Each shortlisted mark has a five-word dominant element and a log with four sources.
- [ ] No shortlisted mark shares sector and dominant element with a logged match.
- [ ] The Limits sentence is present; section 8 links to the engine's maps and copies no table.

Judgement:
- [ ] The substitute in the set is the one buyers compare against.
- [ ] Each "keep" code carries information a buyer needs; each "break" code is habit.
- [ ] Buyers would value the white space.
- [ ] Overall impression, viewed at equal size in black, separates the mark from its neighbours.
- [ ] No symbol idea is the sector's generic object.

## Drill

Fictional business: a subscription that delivers refill pouches of household cleaning products
in one country. Audit the category from public sources, then screen one invented mark: a drop
inside a square with one cut corner.

Pass when: (a) `audit.md` tabulates eight brands or more across the four roles; (b) three codes
or more carry counts and decisions; (c) the white-space sentence fails if you add a brand that
contradicts it; (d) the screen lists the five closest marks found, each with sector and one line
on why it is or is not a problem; (e) the log shows queries and sources; (f) the Limits sentence
is there. A drop is that sector's generic object: a passing answer says so and redraws.

## Failure modes

- Auditing direct rivals and missing the substitute buyers weigh against.
- Differing on a trait buyers ignore; breaking a code that carries real information.
- Using the audit as a mood board and copying the leader. Sectors where each brand audits and
  conforms converge on one sans-serif wordmark ("blanding", a term attributed to Thierry
  Brunfaut `[secondary]`).
- Treating distinctive as "different for its own sake" or as "meaningful".
- Redesigning recognised assets because the team is bored.
- Searching by picture and skipping sound and meaning; showing a favourite before the screen.
- The model's own defaults: describing the category from memory; choosing the dominant code
  because it is the most probable output; claiming white space with no table; drawing the modal
  symbol of the sector, the least ownable one; asserting uniqueness without a search; redrawing
  a mark seen in training without knowing it; giving an opinion on registrability as advice.
