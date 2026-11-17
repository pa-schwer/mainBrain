# 05 · The system beyond the logo

Trains the work after the founder's pick: turning one idea into shapes, sub-systems, architecture,
motion and touchpoints. Produces `brand/<slug>/system.md` and hand-made assets in
`brand/<slug>/system/`. Tags: `[fetched]` read at the URL given, `[secondary]` seen in
write-ups, `[house rule]` a working rule of this skill, `[unverified]` looked for, not confirmed.

## What the best do

- A competent professional adds a kit of parts to the logo. The best find one generative idea,
  most often inside the mark, and make every element a consequence of it.
- They declare which things stay fixed and which may vary, in a table, before drawing anything.
- They write each rule as a generator with numbers, so a stranger or a script can make a new piece.
- They prove the system with the logo removed, then with a competitor's name dropped in.
- They ask the architecture question before the second product exists and write the threshold
  for a new brand in advance.
- They build the hard touchpoints at spec (16 px tab, circle crop, masked icon) and show those
  beside the flattering ones.

## Rules

1. **One idea, many outputs.** MIT Media Lab's identity is a 7 × 7 grid. The grid yields the ML
   monogram and a related glyph for each of 23 research groups; the logos are instances of the
   idea. (Pentagram `[fetched]` https://www.pentagram.com/work/mit-media-lab)
2. **Take the graphic language out of the mark.** Slack's octothorpe uses two shapes, a speech
   bubble and a lozenge. The same two shapes become graphic elements, icons, illustration and
   corner motifs. (Pentagram `[fetched]` https://www.pentagram.com/work/slack)
3. **Other routes to the same result**, all `[secondary]`: a layout device as identity (the
   Whitney's zigzag W that fills the space an artwork leaves; Uber's U-shaped frame), an image
   treatment as identity (Spotify's duotone over photos every rival receives too), a logo detail
   as system seed (Koto's Deezer heartbeat). A treatment written as a function, image in and
   branded image out, is the strongest system asset an agent can ship. `[house rule]`
4. **Constants and variables.** Hold at least two constants among shape, colour, type and
   position. Start with two variables at most. Name the generator for each variable. `[house
   rule]`; the category names in van Nes's *Dynamic Identities* stay `[unverified]`.
5. **Derive from the mark's own geometry.** List its angles, radii, ratios, stroke weights and
   counters, name each as a token in `system.md`, and build 3 to 5 elements from them: a shape
   set, a corner radius, a pattern rule, a framing or cropping device, an icon grid. Assets carry
   zero literal values outside that token list. `[house rule]`
6. **Five numbers and one sentence per sub-system.** `[house rule]` The sentence says how the
   sub-system comes from the idea.
   - Iconography: grid size, stroke width, corner radius, terminal style, optical size range.
   - Illustration: line or fill, palette subset, level of detail, perspective, how people appear.
   - Photography: subject, light, crop, colour grade, what never appears.
   - Data visualisation: categorical order of palette colours, sequential ramp from the tone
     scale, gridline style, label style, emphasis rule.
   - Layout: columns, margin unit, logo position, logo share of the frame, breakpoint behaviour.
7. **Two proofs.** Logo-off: remove the logo from each application and ask a blind reviewer
   which brand it is, among two competitor-style controls. Competitor swap: set a rival's name in
   the system; if the name fits as well, the system is generic. `[house rule]`
8. **Stress tests.** Longest headline, no image, one colour, the smallest format, a tall format
   and a wide one. Cut every element that appears in one application alone. `[house rule]`
9. **Architecture.** Olins's three structures: monolithic (one name and identity across
   everything), endorsed (own brands with a visible parent), branded (separate brands, parent
   unseen). No structure wins in general. `[secondary]` Default to one brand: each separate
   brand must earn its own fame through consistent use. (`[house rule]`, inferred from
   Ehrenberg-Bass `[fetched]` https://marketingscience.info/brands-of-distinction)
10. **Levels and what each may own.** `[house rule]`

    | Level | Own name | Own symbol | Own colour | Form |
    |---|---|---|---|---|
    | Master brand | yes | yes | yes | the kit's masters |
    | Sub-brand | yes | no | one accent from the palette | master plus name lockup |
    | Descriptor | no | no | no | master plus plain words, one type style |
    | Feature | text | never | no | a word in the interface |

11. **The test for a new brand.** An offer earns its own identity when it sells to a different
    audience, must stand or leave the company on its own, and gains nothing from the parent's
    name. All three, written down before anyone asks. A feature never gets a symbol. `[house
    rule]`
12. **Motion has two registers.** Carbon names them productive (task interface) and expressive
    (significant moments). Productive curves: standard `cubic-bezier(0.2, 0, 0.38, 0.9)`,
    entrance `(0, 0, 0.38, 0.9)`, exit `(0.2, 0, 1, 0.9)`. Expressive: standard
    `(0.4, 0.14, 0.3, 1)`, entrance `(0, 0, 0.3, 1)`, exit `(0.4, 0.14, 1, 1)`. Duration scale:
    70, 110, 150, 240, 400, 700 ms, longer for longer travel. Entering elements decelerate,
    leaving ones accelerate. When people keep noticing the motion, reduce it. (Carbon `[fetched]`
    https://carbondesignsystem.com/elements/motion/overview/)
13. **Three tokens are enough before there is a product.** Fast, base and slow from the scale
    above, plus one curve, plus one sentence on how the brand moves. `[house rule]`
14. **Logo animation.** It resolves to the static master; it builds from the mark's construction;
    1 to 2 s for an intro, under 0.5 s for a loader loop; it works silent; it has a one-colour
    version; the last frame holds; it plays once per page view. Animate `transform` and `opacity`
    (stroke-dash for line draws). `[house rule]`
15. **Reduced motion is mandatory.** Honour `prefers-reduced-motion` with a static or cross-fade
    alternative; ship a static fallback for every animated asset. (Carbon `[fetched]`, same URL)
16. **Touchpoints in priority order for a digital-first project.** `[house rule]` Favicon and
    tab; app or PWA icon with maskable and dark variants; social avatar and cover; link-preview
    image as a template; site header and hero, light and dark; product chrome (login, empty
    state, loader); pitch deck; email; document templates; physical items when the business
    needs them.
17. **Verified specs.**
    - Favicon set: `favicon.ico` 32 × 32, an SVG icon, apple-touch 180 × 180 opaque with the mark
      near 140 px, 192 and 512 PNG, a 512 maskable, a web manifest. (Evil Martians `[fetched]`
      https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs)
    - Maskable icon: content inside a centred circle of radius 40 % of the width; a separate
      manifest entry, never `"any maskable"`. (`[fetched]` https://web.dev/articles/maskable-icon)
    - Android adaptive icon: foreground and background layers of 108 × 108 dp; the inner
      66 × 66 dp never clips; logo between 48 and 66 dp; optional monochrome layer. (`[fetched]`
      https://developer.android.com/develop/ui/views/launch/icon_design_adaptive)
    - Google Play icon: 512 × 512, 32-bit PNG, sRGB, full square, no rounded corners, no shadow.
      (`[fetched]` https://developer.android.com/google-play/resources/icon-design-specifications)
    - Apple app icon: 1024 × 1024, square, unmasked layers; the system applies the mask and the
      dark, clear and tinted appearances. No baked corners, shadows or highlights. (`[fetched]`
      https://developer.apple.com/design/human-interface-guidelines/app-icons.md)
    - Open Graph: the protocol names no pixel size (`[fetched]` https://ogp.me/). 1200 × 630 is a
      convention `[secondary]`. Keep text and logo inside a centred 1200 × 600 area with 60 px
      margins, and nothing essential in a corner. `[house rule]`
    - Avatar: one master of 1024 × 1024, opaque ground, content inside the central circle of
      80 % diameter. Platform upload sizes disagree across guides. `[house rule]`
18. **A tab icon must read on light and dark tab bars with no media query.** Safari's handling
    of the query inside an SVG icon stays `[unverified]`. `[house rule]`

Sub-brand lockups, patterns and device proportions: `<skill>/mark/references/identity-system.md`
§3 to §6. Its §8 holds rollout prose; card 06 holds the rollout file.

## Procedure

1. Start after the pick. `brand/<slug>/kit/X/` exists; read `logo/master-symbol.svg` and the
   set's mechanism sentence. The identity engine's `--full` pages for iconography and imagery
   are placeholders; this card fills them.
2. Write the idea in one sentence. Measure the mark and list its geometry as named tokens.
3. Derive 3 to 5 elements from those tokens. Write the constants and variables table.
4. Write each sub-system: five numbers, one sentence. Draw six icons on the grid as a proof.
5. Decide the architecture: list every entity that needs a name now or within three years,
   assign each to one level, name the structure with two business reasons, write the test for
   promotion. Place three invented future offers; a new rule means the scheme failed.
6. Write the motion sentence and three tokens. Build a logo reveal as SVG plus CSS when the
   product has a splash, loader or video use; else stop at tokens.
7. Hand-write the pieces no engine makes, as SVG or HTML in `brand/<slug>/system/`: avatar
   master, link-preview template, Android foreground, background and monochrome layers, Apple
   background and foreground layers, a pattern. Start icon layers on a 1024 canvas with groups
   `bg` and `fg`, no corner radius, no shadow. Card 06 makes the web icon set with the bridge.
8. Render each piece and look at it:
   ```bash
   PATH="$HOME/.cache/logo-design/bin:$PATH" python3 <skill>/mark/scripts/render_png.py \
     brand/<slug>/system/og.html -o brand/<slug>/system/og.png --width 1200 --height 630
   ```
9. Check by hand what no script here checks: foreground inside 66/108 of the Android canvas;
   maskable and avatar content inside the 80 % circle; filled corner pixels on every icon; no
   transparency on apple-touch, Play and avatar; link-preview title legible at 300 px wide; the
   reveal's last frame equal to the static master; nothing moving under reduced motion.
10. Build six applications from the priority list using system tokens alone. Run the stress
    tests. Render logo-off versions.
11. Launch a fresh subagent with no context. Show it the logo-off renders mixed with two
    competitor-style controls and ask which belong together and to whom. Then show the system
    carrying a rival's name and ask whether anything looks wrong. Record its words.
12. Cut what one application alone uses. Write `brand/<slug>/system.md`:
    1. The idea (one sentence) and the mark's geometry tokens
    2. Constants and variables
    3. Derived elements and their generators
    4. Sub-systems: iconography, illustration, photography, data visualisation, layout
    5. Architecture: structure, levels table, promotion test, three placed offers
    6. Motion: sentence, tokens, logo animation spec, reduced-motion behaviour
    7. Touchpoints: priority list, files in `system/`, spec check results
    8. Proofs: logo-off, competitor swap, stress tests, what failed and what changed

## Gate

A script or a count can check:
- [ ] `system.md` has the eight sections in order.
- [ ] The constants table lists two or more constants and two or fewer variables.
- [ ] Each of the five sub-systems has five numbers and one sentence.
- [ ] Every radius, angle and stroke in `system/` files matches a geometry token.
- [ ] Every entity sits on one level; the count of symbols equals the count the structure allows.
- [ ] Motion: three or more duration tokens, each curve named, reveal at 2000 ms or less.
- [ ] Each file in `system/` has the pixel size its spec names and a rendered PNG beside it.
- [ ] No Pantone or CMYK value appears anywhere.

Judgement:
- [ ] A competitor could not use the idea sentence.
- [ ] Each derived element follows from the mark; none arrived as decoration.
- [ ] The blind reviewer grouped the logo-off renders and rejected the controls.
- [ ] The competitor's name looked wrong in the system, and the record says why.
- [ ] The weakest of the six applications is fit to ship, or gone.

## Drill

From a finished mark, write in code a pattern, six icons and a social template. Pass when: every
radius, angle and stroke comes from a geometry token; the six icons share grid, stroke and
radius; a blind subagent picks the three logo-off renders out of a mix with two controls.

## Failure modes

- Every application shows the logo centred on a colour. No system exists.
- The pattern repeats the logo at low opacity.
- Decoration with no link to the mark: blobs, mesh gradients, isometric stock scenes, glass shapes.
- An icon set from a public library whose stroke and radius differ from the mark's.
- Photography written as "authentic, natural light" with no number.
- A system with no constants, or one so rigid that the first tall banner breaks it.
- A symbol for every feature; a master mark too wide to take a descriptor.
- Bounce on everything, default `ease`, a fade-and-scale reveal unrelated to the mark's shape.
- A whole lockup inside an icon; rounded corners or shadows baked in; one file as `any maskable`.
- Tote bags and billboards for a company that sells an API.
- The model's own defaults: it treats the request as one isolated logo and asks nothing about
  other products; it invents sub-brand marks unprompted; it reaches for a letter on a gradient
  rounded square with a glow; it writes a motion chapter of adjectives; it calls the logo-off
  test passed after reading its own rationale.
