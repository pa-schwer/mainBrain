---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

<!-- LOCAL CHANGE (mainBrain): this block is not upstream. Everything below
     the next rule is upstream and unmodified. Strip this block before
     updating from vercel-labs/agent-skills. -->

## Addendum: reviewing in a mainBrain project

Vendored from `vercel-labs/agent-skills` at commit `063bee9`. The rules in
`command.md` next to this file come unmodified from
`vercel-labs/web-interface-guidelines` at commit `e3d624b`. `LICENSE` is
that repo's (MIT, Vercel Labs); agent-skills declares MIT in its README.
This block is the only local change, and it overrides the upstream text
below where they conflict.

**Rules.** Read `command.md`. Do not fetch the source URL: the vendored
copy is the version the project reviews against, and an update goes
through a mainBrain pull request.

**When.** A merge gate. Claude reads this file by path and runs it on every
site or app pull request that touches markup, styles or components, over
the files in the diff. Output follows `command.md`: `file:line`, grouped by
file.

**What blocks.** A finding under Accessibility, Focus States, Forms or
Anti-patterns is red: fix it in the same pull request, or the merge waits.
Fix the other findings in the same pull request when the fix is local, or
list them in its body with the reason they stay.

**Owners.** Where another source owns the question, its answer wins and
this review drops the finding.

- Animation: `review-animations`, when installed. Without it, the
  Animation section applies.
- Content & Copy, and the Typography rules on quotes and ellipses: the ops
  repo's `BRAND.md`, which sets the language. Title Case and English quotes
  do not apply to a product written in another language.
- Style, color, type and layout choices: `ui-ux-pro-max` and the ops repo's
  `docs/design-system.md`. This review checks correctness and leaves taste
  to them.
- Hydration Safety and the React rules apply to the app. The site is static
  Astro.

---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.
