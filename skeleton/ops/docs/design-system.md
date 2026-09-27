# Design system

PLACEHOLDER. No palette, no type scale, no spacing rule, no motion token is
settled yet.

Until they are, site and app build with Tailwind's own defaults and no
brand value is invented as a stand-in. `scripts/no-hardcoded-tokens.sh` in
each front-end repo fails CI on a hex value, a color function or a
`font-family` declaration outside `src/styles/tokens.css`.

When the tokens exist (a Claude Design project is the usual source), this
file records them as tables, and each front-end repo transcribes them into
`src/styles/tokens.css` as raw CSS variables mapped by `@theme` to Tailwind
utilities. A value changes here first, then in every `tokens.css`.

## Color

## Type

## Spacing and radius

## Motion

<!-- Durations and easings. Until this section exists, `animate` and
     `review-animations` accept Tailwind's default `duration-*` and
     `ease-*` utilities. -->
