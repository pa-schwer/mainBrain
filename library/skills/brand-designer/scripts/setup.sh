#!/usr/bin/env bash
# Run once per container, from anywhere:
#   bash <skill-dir>/scripts/setup.sh
#
# The two engines of this bundle leave their reference data out of the
# repository: mark/ has no assets/library/svg/ (1,432 logos of real
# brands), identity/ has no assets/library/ (measured site palettes of
# 318 real brands, with their names and addresses). Every one of them
# belongs to its owner, neither MIT license covers them, and a public
# library names no company. This script fetches both, each at its
# vendored commit, into the container cache, where mark/scripts/svglib.py
# and identity/scripts/build_catalog.py look when the bundle has none.
#
# Then it gives the mark engine a renderer. Unless rsvg-convert or
# Inkscape is on PATH, it writes a `google-chrome` wrapper over
# Playwright's headless shell: Chromium refuses to start as root without
# --no-sandbox, mark/scripts/render_png.py does not pass it, and the web
# container's full Chrome hangs on --screenshot. The wrapper adds the
# flag only when it runs as root, and lives in a folder of its own that
# goes on PATH for the mark engine's commands alone. The identity engine
# drives the browser itself and needs no wrapper.
set -euo pipefail

MARK_COMMIT=734090317a2155c5bf1ae8bd4cc85c6848a0128f       # kaankiziltug/logo-design-skill 1.4.5
IDENTITY_COMMIT=af7ba40fe067b8b4aaeb2af90ed6c8996d014791   # fatihaydost/brand-identity-skill, after 1.1.1
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}"
MARK_CACHE="$CACHE_ROOT/logo-design"
IDENTITY_CACHE="$CACHE_ROOT/brand-identity"
mkdir -p "$MARK_CACHE" "$IDENTITY_CACHE"

# Staged inside the cache so that each move below is a rename on one
# filesystem: an interrupted run leaves no half-copied library that the
# next run would take for a complete one. The trap clears the stage on
# every exit, a failed fetch included.
STAGE="$(mktemp -d "$CACHE_ROOT/brand-designer-setup.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT

# fetch <name> <repo url> <commit> <folder inside the repo>: a sparse,
# blobless checkout of that one folder into $STAGE/<name>. Called as a
# plain statement, never inside $(...), where bash drops `set -e` and a
# failed git command would go unnoticed.
fetch() {
  local repo="$STAGE/$1"
  git init -q "$repo"
  git -C "$repo" remote add origin "$2"
  git -C "$repo" sparse-checkout set --no-cone "/$4/"
  git -C "$repo" fetch -q --depth 1 --filter=blob:none origin "$3"
  git -C "$repo" checkout -q FETCH_HEAD
}

count_logos() { find "$MARK_CACHE/svg" -maxdepth 1 -type f | wc -l; }

# gallery.html moves last, so its presence says the svg folder is whole.
if [ -d "$MARK_CACHE/svg" ] && [ -f "$MARK_CACHE/gallery.html" ]; then
  echo "mark library: $(count_logos) reference logos already in $MARK_CACHE"
else
  lib=skills/logo-design/assets/library
  fetch mark https://github.com/kaankiziltug/logo-design-skill.git "$MARK_COMMIT" "$lib"
  rm -rf "$MARK_CACHE/svg"
  mv "$STAGE/mark/$lib/svg" "$STAGE/mark/$lib/gallery.html" "$MARK_CACHE/"
  echo "mark library: fetched $(count_logos) reference logos into $MARK_CACHE"
fi

if [ -f "$IDENTITY_CACHE/library/catalog.json" ]; then
  echo "palette library: already in $IDENTITY_CACHE/library"
else
  lib=skills/brand-identity/assets/library
  fetch identity https://github.com/fatihaydost/brand-identity-skill.git "$IDENTITY_COMMIT" "$lib"
  rm -rf "$IDENTITY_CACHE/library"
  mv "$STAGE/identity/$lib" "$IDENTITY_CACHE/library"
  echo "palette library: fetched into $IDENTITY_CACHE/library"
fi

if command -v rsvg-convert inkscape > /dev/null 2>&1; then
  echo "mark renderer: already on PATH"
  exit 0
fi
headless_shell="$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2> /dev/null | tail -1 || true)"
if [ -z "$headless_shell" ]; then
  echo "mark renderer: no headless shell found; mark/scripts/render_png.py --which lists what it can use"
  exit 0
fi
mkdir -p "$MARK_CACHE/bin"
cat > "$MARK_CACHE/bin/google-chrome" <<EOF
#!/bin/sh
# Chromium will not start as root with its sandbox; any other user keeps it.
[ "\$(id -u)" = 0 ] && set -- --no-sandbox "\$@"
exec "$headless_shell" "\$@"
EOF
chmod +x "$MARK_CACHE/bin/google-chrome"
echo "mark renderer: run the mark engine's scripts with PATH=\"$MARK_CACHE/bin:\$PATH\""
