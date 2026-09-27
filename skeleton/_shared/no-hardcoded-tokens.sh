#!/usr/bin/env bash
# Fail on a hardcoded design token.
#
# The rule: color and type come from the design system, which is
# {{PROJECT}}-ops/docs/design-system.md, reaching this repo through
# src/styles/tokens.css. A hex value or a font stack written into a
# component means swapping the real tokens becomes a search across repos
# instead of an edit to one file.
#
# While docs/design-system.md is a placeholder, the correct thing to write
# is a Tailwind default class. This check is what stops a stand-in palette
# from being invented while we wait.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SEARCH="$ROOT/src"

# tokens.css is where real values are allowed to land.
EXCLUDE='src/styles/tokens.css'

hits=0

scan() {
  local label="$1" pattern="$2"
  local found
  found="$(grep -rnE --binary-files=without-match \
    --exclude-dir=node_modules "$pattern" "$SEARCH" 2>/dev/null \
    | grep -v "$EXCLUDE")" || true
  if [ -n "$found" ]; then
    echo "FAIL: $label"
    echo "$found" | sed 's/^/      /'
    echo
    hits=$((hits + 1))
  fi
}

scan "hardcoded hex color" '#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?\b'
scan "hardcoded color function" '\b(rgba?|hsla?|oklch|oklab)\('
scan "hardcoded font stack" 'font-family[[:space:]]*:'

if [ "$hits" -gt 0 ]; then
  echo "$hits kind(s) of hardcoded design token found."
  echo "Use a Tailwind default class, or add the value to"
  echo "src/styles/tokens.css once {{PROJECT}}-ops/docs/design-system.md defines it."
  exit 1
fi

echo "No hardcoded design tokens."
exit 0
