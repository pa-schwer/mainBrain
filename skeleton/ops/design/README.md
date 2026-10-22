# Mockups

Screens are drawn here before a front end builds them. The founder
mocks up with Claude in this folder, and the card on the product board
links the result. A mockup is not product code: no product repo imports
it, and nothing deploys it.

`impeccable` is the design director, read from
`.claude/skills/impeccable/SKILL.md`, addendum first. Its craft floor
applies to every page here. This file adds what the project checks.

## Folders

```
design/
├── README.md     this protocol
├── check.sh      the gate: tokens identical, no raw value, detector clean
├── tokens.css    byte-identical to src/styles/tokens.css in every front end
├── fonts/        woff2 files with their licenses, served at /fonts/
├── reference/    what the founder supplies; read, never edited
└── mockups/      one folder per card; _template/ is the starting page
```

## What a mockup is

- One folder per screen, named after its card: `mockups/SPEC-12-cohort-view/`.
  A global card with sub-cards gets one folder per sub-card.
- `index.html` is a static page: HTML and CSS, no build, no framework, no
  network request. The one script it carries switches between states.
- It links `/tokens.css` and draws every color, font, size, radius, shadow
  and duration with `var(--…)`. `check.sh` fails on a raw value.
- Fonts load from `fonts/`, never from a CDN, so a screenshot renders the
  same in every container. The app serves the same files from
  `public/fonts/`, so `/fonts/` resolves in both.
- `NOTES.md` in the folder records the choices the founder made and the
  findings kept on purpose, each with its reason.
- Screenshots sit next to the page, `shot-<width>-<theme>[-<state>].png`.
  They are what the founder reads on a phone.

## The rules a mockup obeys

Content:

1. Real words in {{COPY_LANGUAGE}}, by `BRAND.md`. No lorem ipsum, no
   "Feature one", no placeholder name.
2. Real data, and its worst case: the longest name, zero items, one item,
   the largest count, a missing optional field.
3. Every state the screen has: ready, empty, loading, error, and any
   other the card names (no permission, partial, done). `?state=empty`
   shows one; the template carries the switch.
4. Every width it ships at: 390, 768 and 1280 for an app screen; light
   and dark when the front end follows the system preference.

Craft, on top of impeccable's floor:

5. Tokens only. A value missing from `tokens.css` goes into
   `docs/design-system.md` first, then into every `tokens.css`.
6. Contrast measured on the real token pair: 4.5:1 for body text, 3:1
   for large text and UI parts.
7. Focus visible on every interactive element; touch targets of 44px at
   least at 390 wide.
8. One type scale, one spacing scale, one radius set, all from the
   design system. An off-scale value is a finding.
9. No motion unless the card is about motion; then it follows `animate`
   and the Motion section of the design system.

## How a mockup is made

1. Read the card (the `product-board` skill), then `docs/product.md`,
   `BRAND.md` and `docs/design-system.md`.
2. Run impeccable's `context`, then work in the mode of the surface:
   Operate for an app screen, Persuade for a public page.
3. Copy `mockups/_template/` to the card's folder and draw.
4. Serve and look: `python3 -m http.server 4173 -d design`, then
   `http://localhost:4173/mockups/<folder>/` at each width, with
   `playwright-cli` when it is installed. Save the screenshots.
5. `bash design/check.sh` until it is green.
6. impeccable's `critique` and `audit` on the page. Fix each finding, or
   write it in `NOTES.md` with the reason it stays.
7. Pull request, merged on green like any change here. Then set the
   card's Design to the folder:
   `https://github.com/{{OWNER}}/{{PROJECT}}-ops/tree/main/design/mockups/<folder>`.

Variants go in `v1/`, `v2/` inside the folder. The founder picks; the
pull request that records the pick in `NOTES.md` deletes the others.

## From mockup to screen

- The session that builds the screen reads the folder by path: the page
  for structure and states, `NOTES.md` for decisions, the screenshots
  for the target. It rebuilds with the front end's components and the
  same tokens, and never copies the HTML into a product repo.
- A difference between the built screen and its mockup is a bug, or a
  line in `docs/decisions.md`.
- A token changes in `docs/design-system.md` first, then here and in
  every front end's `src/styles/tokens.css` in the same cycle. `check.sh`
  stays red until the copies match.
