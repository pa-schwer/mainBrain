# Design system

PLACEHOLDER. No palette, no type scale, no spacing rule, no motion token is
settled yet.

Until they are, site and app build with Tailwind's own defaults and no
brand value is invented as a stand-in. `scripts/no-hardcoded-tokens.sh` in
each front-end repo fails CI on a hex value, a color function or a
`font-family` declaration outside `src/styles/tokens.css`.

When the tokens exist (a Claude Design project, or the visual world
impeccable settles with the founder, is the usual source), this file
records them as tables, and each front-end repo transcribes them into
`src/styles/tokens.css` as raw CSS variables mapped by `@theme` to
Tailwind utilities. A value changes here first, then in every `tokens.css`,
`design/tokens.css` included where mockups are drawn.

Each section below says what it holds once filled, so a screen is checked
against this file rather than against taste.

## Color

<!-- Roles, not hues: surface, raised surface, text, muted text, border,
     accent, text on accent, focus ring, and one per status (success,
     warning, danger, info). A light and a dark value per role. Every
     text-on-surface pair the product uses, with its contrast ratio:
     4.5:1 for body text, 3:1 for large text and UI parts. -->

## Type

<!-- Families with their license and where the files live. One scale:
     size, line height, weight and tracking per step. The step each
     element takes (page title, section title, body, label, figure).
     Tabular figures where numbers line up in columns. -->

## Spacing and radius

<!-- One spacing scale: the base unit and its steps. The layout grid per
     width (columns, gutter, max width). The radius set and which element
     takes which. Elevation levels and when each applies. -->

## Components

<!-- The states every interactive element has: default, hover, focus
     visible, active, disabled, loading. The minimum touch target. The
     density of each surface. -->

## Data visualization

<!-- Only when the product shows data: the chart types it uses and what
     each answers, the data palette in order, readable without hue alone,
     axis and label rules, and how an empty or partial series reads. -->

## Motion

<!-- Durations and easings. Until this section exists, `animate` and
     `review-animations` accept Tailwind's default `duration-*` and
     `ease-*` utilities. -->
