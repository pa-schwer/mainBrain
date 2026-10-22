#!/usr/bin/env bash
# The mockup gate. Green before a mockup reaches the founder or a card.
#
# 1. design/tokens.css is byte-identical to src/styles/tokens.css in every
#    front end next to this repo, so a mockup and the screen built from it
#    draw with the same values. A sibling that is not cloned is skipped.
# 2. No mockup carries a raw color, a color function or a font stack:
#    every value comes from tokens.css.
# 3. impeccable's detector finds no design anti-pattern in any mockup.

set -uo pipefail

DESIGN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPS="$(dirname "$DESIGN")"
WORKSPACE="$(dirname "$OPS")"
fails=0

echo "== tokens =="
for repo in {{SIBLINGS}}; do
  front="$WORKSPACE/$repo/src/styles/tokens.css"
  if [ ! -f "$front" ]; then
    echo "  skip  $repo (no src/styles/tokens.css here)"
  elif cmp -s "$DESIGN/tokens.css" "$front"; then
    echo "  ok    $repo"
  else
    echo "FAIL: design/tokens.css differs from $repo/src/styles/tokens.css"
    diff -u "$front" "$DESIGN/tokens.css" | head -40 | sed 's/^/      /'
    fails=$((fails + 1))
  fi
done

echo "== raw values =="
before=$fails
scan() {
  local label="$1" pattern="$2" found
  # An in-page link (href="#members") is not a color.
  found="$(grep -rnE --include='*.html' --include='*.css' "$pattern" "$DESIGN/mockups" 2>/dev/null \
    | grep -vE 'href="#[^"]*"')" || true
  if [ -n "$found" ]; then
    echo "FAIL: $label"
    echo "$found" | sed "s#$DESIGN/##; s/^/      /"
    fails=$((fails + 1))
  fi
}
scan "hex color" '#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?([0-9a-fA-F]{2})?\b'
scan "color function" '\b(rgba?|hsla?|oklch|oklab|lab|lch|color-mix)\('
# A face named through var(--...) comes from tokens.css; any other value is a stack.
scan "font stack" 'font-family[[:space:]]*:[[:space:]]*([^v[:space:]]|v[^a]|va[^r]|var[^(])'
[ "$fails" -eq "$before" ] && echo "  ok    every value comes from tokens.css"

echo "== detector =="
cd "$OPS" || exit 1
IMPECCABLE_NO_TELEMETRY=1 .claude/skills/impeccable/scripts/impeccable detect design/mockups
code=$?
case "$code" in
  0) echo "  ok    no design anti-pattern" ;;
  2) fails=$((fails + 1)) ;;
  *)
    echo "FAIL: the detector did not run (exit $code). It downloads its engine"
    echo "      on first use from github.com: HANDOFF E2, or the network policy."
    fails=$((fails + 1))
    ;;
esac

echo
if [ "$fails" -gt 0 ]; then
  echo "$fails problem(s). Fix them before the mockup reaches the founder."
  exit 1
fi
echo "Mockups pass the gate."
