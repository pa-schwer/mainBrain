#!/usr/bin/env bash
# The bundle's own check: both engines run from this folder, end to end,
# and they meet where the skill says they do. Run it after vendoring or
# updating an engine:
#
#   bash <skill>/evals/smoke.sh
#
# It builds the identity engine's example brand (three sets) in a
# temporary folder, makes the kit for set A, audits the kit's symbol
# with the mark engine and exports the web icon set from it. It needs
# the network once, for the example's open-license fonts. Nothing is
# written inside the skill folder.
set -euo pipefail

SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_ROOT="$(mktemp -d)"
trap 'rm -rf "$WORK_ROOT"' EXIT
cd "$WORK_ROOT"

fail() { echo "FAIL: $*"; exit 1; }
brand() { python3 "$SKILL/identity/scripts/brand.py" "$@"; }
# quiet <label> <command...>: the command's output goes to <label>.log and
# is shown only when the command fails.
quiet() {
  local label="$1"
  shift
  "$@" > "$label.log" 2>&1 || { cat "$label.log"; fail "$label"; }
}

bash "$SKILL/scripts/setup.sh"
MARK_PATH="${XDG_CACHE_HOME:-$HOME/.cache}/logo-design/bin:$PATH"

brand check
brand init "Ferrow" --root brand --sets 3 --langs en --numbers \
  --sector "bicycle repair shop" --audience "city commuters" \
  --attributes steady,quick,local --competitors "none named" \
  --tagline "Fixed while you work" --sentence en='Your bike, ready by five.' \
  --nav Repairs,Prices,Visit --cta "Book a repair" > /dev/null
WORK="brand/ferrow"
[ -f "$WORK/brief.json" ] || fail "init --root brand did not write $WORK/brief.json"
cp "$SKILL/identity/templates/sets.example.json" "$WORK/sets.json"

quiet logos brand logos "$WORK"
quiet build brand build "$WORK"
quiet kit brand kit "$WORK/sets/A"

KIT="$WORK/kit/A"
for f in "$WORK/logo-sheet.png" "$WORK/board.png" "$WORK/review.png" "$KIT/ferrow-guidelines.pdf" \
         "$KIT/logo/symbol-only.svg" "$KIT/logo/master-symbol.svg" "$KIT/tokens/tokens.dtcg.json" "$KIT/fonts.md"; do
  [ -s "$f" ] || fail "identity engine did not write $f"
done

# The palette library and the logo library answer from the cache. The
# count must not be zero: an empty library also prints "0 ... match".
quiet palette-library python3 "$SKILL/identity/scripts/search_library.py" --industry fintech --summary
grep -Eq '^[1-9][0-9]* brands match' palette-library.log || fail "palette library matched no brand"
quiet logo-library python3 "$SKILL/mark/scripts/search_library.py" --industry fintech --summary
grep -Eq '^[1-9][0-9]* logos match' logo-library.log || fail "logo library matched no logo"

# The mark engine reads the identity engine's master and exports the web set from it.
quiet audit python3 "$SKILL/mark/scripts/svg_audit.py" "$KIT/logo/master-symbol.svg"
grep -q "production-readiness" audit.log || fail "svg_audit on the kit master"
quiet web-icons env PATH="$MARK_PATH" python3 "$SKILL/mark/scripts/export_variants.py" "$KIT/logo/symbol-only.svg" \
  --web-icons --icon-bg "#14524a" --title "Ferrow" --out-dir "$KIT/web"
for f in favicon.ico favicon.svg apple-touch-icon.png icon-192.png icon-512.png maskable-512.png \
         site.webmanifest head-snippet.html; do
  [ -s "$KIT/web/$f" ] || { cat web-icons.log; fail "mark engine did not write web/$f"; }
done

echo "brand-designer smoke passed"
