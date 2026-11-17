# 06 · Delivery, hand-over and rollout

Trains the last mile: the kit, the file matrix, guidelines people use, tokens, fonts, print
honesty, the hand-over to site and app, and governance. Produces `brand/<slug>/rollout.md`.
Tags: `[fetched]` read at the URL given, `[secondary]` seen through write-ups, `[house rule]` a
working rule of this skill, `[unverified]` looked for and not confirmed.

## What the best do

- A competent professional hands over a tidy folder and a launch checklist. The best generate
  the whole matrix from one source and label every file with its use.
- They put downloads and a one-page quick start before any doctrine.
- They state each rule as a number or a yes/no and show it drawn beside its counter-example.
- They inventory every place the old identity lives before the design ends, and give each row
  an owner.
- They make the right asset the easiest one to reach, and name what they could not verify.

## Rules

1. **The kit comes from one command.** `brand.py kit` writes the guidelines PDF, the logo
   matrix, the tokens and `fonts.md`. Pages, anatomy and the misuse page:
   `<skill>/identity/references/kit.md`.
2. **The matrix is lockups × colour variants × formats.** The kit's `logo/` holds five masters
   (symbol, primary, horizontal lockup, stacked lockup, wordmark), full-colour and one-colour
   variants for light and dark grounds, `symbol-only.svg`, favicons and `app-icon-512`. Every
   variant comes from a master by swapping roles; nobody redraws. `[house rule]`
3. **The kit stops short of a web icon set.** It has no `favicon.ico`, apple-touch icon, maskable
   icon, manifest or head snippet. The mark engine makes them from the kit's symbol (Procedure,
   step 3).
4. **Every delivered file carries a use label and a nominal size.** `[house rule]`

   | Use | File kind | Nominal size |
   |---|---|---|
   | Site or app header | horizontal lockup, SVG | height set per breakpoint |
   | Narrow or square space | stacked lockup, SVG | at or above the kit minimum |
   | Space too small for the name | `symbol-only.svg` | at or above the symbol minimum |
   | Dark ground | on-dark or one-colour light variant | same as its light twin |
   | Fax, stamp, engraving, embroidery | one-colour variant | printer's call |
   | Browser tab | `favicon.ico`, `favicon.svg` | 16 and 32 px |
   | Home screen | `apple-touch-icon.png`, `icon-192`, `icon-512` | 180, 192, 512 px |
   | Masked launcher | `maskable-512.png` | 512 px, content in 80 % circle |
   | Editing, new lockups | `master-*.svg` | source, never placed |

   Quote file names from a listing of `kit/X/logo/` and `kit/X/web/`, never from memory.
5. **An SVG speaks to assistive technology.** Give each placed SVG a short title (the brand
   name plus "logo") and a longer description of what the mark shows, and make the root element
   reference both ids as its label, with an image role. The bridge's `--title` writes the title;
   the designer adds the description to the copy that goes inline. A decorative repeat gets
   `aria-hidden`. `[house rule]`
6. **Three lines of web-embedding notes go in `rollout.md`.** `[house rule]`
   - Inline SVG where the mark must follow the theme, animate or take focus styles.
   - An image tag with alt text and explicit width and height everywhere else.
   - A CSS background for decoration alone, since assistive technology skips it.
   Add a width rule per breakpoint: a pixel width for the lockup at each, never under the kit's
   minimum size, with the switch to the symbol stated as a width.
7. **Guidelines that get used.** `[house rule]` built on the fetched examples below:
   - Downloads first. GitHub's logo page offers the files before its first rule. (`[fetched]`
     https://brand.github.com/foundations/logo)
   - Clear space in units of the mark. Spotify uses half the icon's height. (`[fetched]`
     https://developer.spotify.com/documentation/design)
   - Minimum size per medium in real units. Spotify: full logo 70 px on screen and 20 mm in
     print; icon 21 px and 6 mm. (`[fetched]`, same URL)
   - Colour rules as closed lists. GitHub: white, black, and grey or green in a few cases.
     Spotify: the green logo on black, white or untreated photos. (`[fetched]`, both URLs)
   - A say-when per variant. GitHub: lockup in most places, mark alone on owned surfaces.
   - A drawn misuse page of 4 to 6 cases from the real mark, one or two that this mark alone can
     suffer: `<skill>/identity/references/kit.md`, "Misuse page".
   - Every rule a number or a yes/no. "Generous clear space" fails.
8. **Tokens are the single source.** `palette.json` feeds every generated file; hand edits to
   generated files are forbidden. Names, files and wiring:
   `<skill>/identity/references/tokens-export.md`.
9. **DTCG facts.** Format Module 2025.10 is the first stable version, a Final Community Group
   Report and no W3C Standard. A token is an object with `$value`; `$type` sits on the token or
   its group. An alias reads `{group.token}`. A colour value is an object with `colorSpace`,
   `components`, optional `alpha` and an optional six-digit `hex` fallback. (`[fetched]`
   https://www.designtokens.org/tr/2025.10/format/ and
   https://www.designtokens.org/tr/2025.10/color/)
10. **The kit's tokens stay a proposal inside `brand/`.** No colour enters a product repo's
    `tokens.css` until the design source settles it: the `impeccable` skill where the ops repo
    installed it, else the founder, through `docs/design-system.md`. This mainBrain rule
    overrides the engine's hand-off note.
11. **Fonts are licences first.** Record family, source, licence and who must buy. The kit's
    `fonts.md` lists sources and links and ships no font file. Policy per source:
    `<skill>/identity/references/type.md`, "Licences and rendering".
12. **Print honesty.** The designer never writes a Pantone or CMYK value. Print values come
    "from your printer, to be proofed". Lab D50, materials and the proof flow:
    `<skill>/identity/references/reproduction.md`.
13. **Words follow `BRAND.md`.** The brand designer writes no voice chapter.
14. **Inventory before launch.** One row per place the identity lives, with an owner, the new
    asset and a status. `[house rule]` Wheeler names managing assets as a phase. `[secondary]`
15. **Sequence.** Internal first, then owned digital surfaces in one switch on one day, then
    physical items by attrition. `[house rule]`
16. **Audit dates.** 30 and 90 days after launch, then twice a year. `[house rule]`
17. **Refresh or rebrand follows the business.** A changed strategy, name, audience or structure
    calls for a rebrand. A sound strategy with an execution problem calls for a refresh. Slack's
    change had a functional reason: eleven colours and a mark with poor reproduction. (Pentagram
    `[fetched]` https://www.pentagram.com/work/slack) Decision and equity audit:
    `<skill>/mark/references/redesign.md` §1 to §3.
18. **Protect what people recognise.** Gap's 2010 logo and Tropicana's 2009 packaging both
    dropped known assets with no strategic change behind them, and both companies reversed
    within weeks. `[secondary]`
19. **Measure with honesty.** Usable signals: share of surfaces on the new assets, audit
    findings, time for a newcomer to make an on-brand piece, unprompted attribution in customer
    tests the founder runs. A visual identity's effect on sales resists isolation; promise none.
    `[house rule]`

## Procedure

1. Confirm the founder's pick in writing. Build the kit:
   ```bash
   python3 <skill>/identity/scripts/brand.py kit brand/<slug>/sets/X --full
   ```
   It writes `brand/<slug>/kit/X/`: `<brand>-guidelines.pdf` (8 pages, 13 with `--full`),
   `pages/*.png`, `logo/`, `tokens/` and `fonts.md`.
2. Read every page PNG. Fix the source and rebuild on any broken render. Add the one or two
   mark-specific misuse drawings (`kit.md`).
3. Make the web icons. `bash <skill>/scripts/setup.sh` must have run once in the container.
   ```bash
   PATH="$HOME/.cache/logo-design/bin:$PATH" python3 <skill>/mark/scripts/export_variants.py \
     brand/<slug>/kit/X/logo/symbol-only.svg --web-icons --icon-bg "<hex>" --title "<Brand>" \
     --out-dir brand/<slug>/kit/X/web
   ```
   Add `--favicon-source <small cut svg>` when the set has a small cut. Output: `favicon.ico`,
   `favicon.svg`, `favicon-16/32/48.png`, `apple-touch-icon.png` (180), `icon-192.png`,
   `icon-512.png`, `maskable-512.png`, `site.webmanifest`, `head-snippet.html`.
4. Look at the 16 px favicon on light and dark tab colours and at the maskable icon under a
   circle. Specs: card 05, rule 17. The engine has no tool for Apple layers, Android adaptive
   layers or link-preview templates; card 05 covers those by hand.
5. List `kit/X/logo/` and `kit/X/web/`. Write the use table with real names.
6. Open each token file once. Check that every colour on the guideline pages equals its token.
7. Launch a fresh subagent with no context. Give it the PDF pages, the use table and the kit
   folder, and ask it to make one social card. Each question it asks or guess it makes marks a
   gap in the guidelines; fix the gap and note it.
8. Hand over by pull request, one per product repo, opened by the session:
   - Site: icons into `public/`, the head snippet's lines into `Base.astro`'s head.
   - App: icons into `public/`, the same lines into `index.html`.
   - Colours and fonts: a proposal in the ops repo for `docs/design-system.md`. No token file
     travels until the design source accepts it.
9. Write `brand/<slug>/rollout.md`:
   1. Quick start: file locations, palette values, fonts and sources, five do's, five don'ts
   2. Which file for which use (the table)
   3. Web embedding (three lines and the width rule)
   4. Hand-over: pull requests opened, token proposal status
   5. Touchpoint inventory: place, current state, new asset, owner, status
   6. Sequence and launch checklist
   7. Owner, audit dates, change rule (who may add a colour, a lockup, a sub-brand)
   8. Refresh-versus-rebrand rule and the assets to protect
   9. Measurement
   10. The founder's list: trademark clearance, print proofs, font purchases, customer tests
10. Launch checklist, digital-first `[house rule]`: favicon set live on every domain;
    link-preview default on every template; app icons submitted; avatars and covers changed the
    same day; email signature and header; templates; old files removed; the 30-day audit date.

## Gate

A script or a count can check:
- [ ] `kit/X/` holds the PDF, `pages/`, `logo/` with five masters, `tokens/` and `fonts.md`.
- [ ] `kit/X/web/` holds the eleven files of step 3; apple-touch has no transparent pixel.
- [ ] No SVG in `logo/` or `web/` contains `<text>`, `<image>`, a script or an external URL.
- [ ] Every name in the use table exists on disk, and every file on disk has a row.
- [ ] Every colour value on the guideline pages equals its token; zero mismatches.
- [ ] Clear space and minimum size carry numbers with units; the misuse page draws 4 to 6 cases.
- [ ] No Pantone or CMYK value appears that the founder or a printer did not supply.
- [ ] No product repo's `tokens.css` changed; every inventory row has an owner and a status.
- [ ] `rollout.md` has the ten sections and two audit dates.

Judgement:
- [ ] A person in a hurry finds the right file within the first screen of `rollout.md`.
- [ ] The blind subagent made its card with no question, and the card obeys the rules.
- [ ] The misuse page shows mistakes people will make with this mark.
- [ ] The founder's list names each open risk in plain words.

## Drill

Deliver the package for a mark with three lockups. Pass when: the use table and the disk listing
match one to one; the web set has the right pixel sizes; a second agent, given the guidelines
alone, makes a social card that respects palette, clear space and minimum size with no question.

## Failure modes

- A PDF with forty pages of mission before the first download.
- Hex values typed by hand that disagree with the files.
- A white logo on a white artboard with no hint in its name; `Logo_FINAL_v2 (1).png`.
- No dark-ground version, so a boxed screenshot of the logo appears within a week.
- The homepage launches while tab icon, link preview and store icon stay old.
- No owner, so each team adds one more colour. A rebrand because someone grew bored.
- The model's own defaults: it invents a plausible Pantone number; it copies the kit's
  `tokens.css` into a product repo because the engine's note says so; it swaps a free font for a
  commercial one in silence; it writes a voice chapter; it claims the new identity lifts sales;
  it reports the kit as delivered without opening one page render.
