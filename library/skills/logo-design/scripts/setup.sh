#!/usr/bin/env bash
# LOCAL CHANGE (mainBrain): this file is not upstream. Delete it before
# updating from kaankiziltug/logo-design-skill.
#
# Run once per container. Fetches the reference logos this bundle leaves
# out (trademarks of their owners, outside the MIT license: TRADEMARKS.md)
# into the cache, where scripts/svglib.py looks when the bundle has no
# svg/ of its own. Then, when no renderer is on PATH, writes a `chromium`
# wrapper over Playwright's headless shell: Chromium refuses to start as
# root without --no-sandbox, and render_png.py does not pass it.
set -euo pipefail

COMMIT=734090317a2155c5bf1ae8bd4cc85c6848a0128f   # upstream 1.4.5, the vendored commit
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/logo-design"
mkdir -p "$CACHE"

if [ -d "$CACHE/svg" ] && [ -f "$CACHE/gallery.html" ]; then
  echo "library: $(ls "$CACHE/svg" | wc -l) reference logos already in $CACHE"
else
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  lib=skills/logo-design/assets/library
  git -C "$tmp" init -q
  git -C "$tmp" remote add origin https://github.com/kaankiziltug/logo-design-skill.git
  git -C "$tmp" sparse-checkout set --no-cone "/$lib/svg/" "/$lib/gallery.html"
  git -C "$tmp" fetch -q --depth 1 --filter=blob:none origin "$COMMIT"
  git -C "$tmp" checkout -q FETCH_HEAD
  rm -rf "$CACHE/svg"
  mv "$tmp/$lib/svg" "$tmp/$lib/gallery.html" "$CACHE/"
  echo "library: fetched $(ls "$CACHE/svg" | wc -l) reference logos into $CACHE"
fi

if command -v rsvg-convert inkscape chromium chromium-browser google-chrome > /dev/null 2>&1; then
  echo "renderer: already on PATH"
  exit 0
fi
shell="$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2> /dev/null | tail -1 || true)"
if [ -z "$shell" ]; then
  echo "renderer: none found; render_png.py --which lists what it can use"
  exit 0
fi
mkdir -p "$CACHE/bin"
printf '#!/bin/sh\nexec "%s" --no-sandbox "$@"\n' "$shell" > "$CACHE/bin/chromium"
chmod +x "$CACHE/bin/chromium"
echo "renderer: run the scripts with PATH=\"$CACHE/bin:\$PATH\""
