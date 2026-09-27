#!/usr/bin/env bash
# Verify the library against its catalog, and the skeleton against its
# placeholders. Runs in CI and before any commit here.
#
# Exit 1 on: a catalog entry whose path is missing, a bundle with no
# LICENSE, a bundle on disk that the catalog does not list, a placeholder
# in a template that spawn.py does not know, a JSON file that does not
# parse, or a shell script with a syntax error.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fails=0
fail() { echo "FAIL: $*"; fails=$((fails + 1)); }

for tool in jq python3; do
  command -v "$tool" > /dev/null 2>&1 || { echo "MISSING $tool"; exit 1; }
done

echo "== catalog =="
jq -e . "$ROOT/library/catalog.json" > /dev/null || fail "library/catalog.json does not parse"

# Every entry with a path exists; every skill bundle has SKILL.md and a LICENSE.
while IFS=$'\t' read -r name kind path; do
  [ "$path" = "null" ] && continue
  if [ ! -e "$ROOT/library/$path" ]; then
    fail "$name: $path is missing"
    continue
  fi
  if [ "$kind" = "skill" ]; then
    [ -f "$ROOT/library/$path/SKILL.md" ] || fail "$name: no SKILL.md"
    ls "$ROOT/library/$path"/LICENSE* > /dev/null 2>&1 || fail "$name: no LICENSE in the bundle"
    front="$(sed -n '2,3p' "$ROOT/library/$path/SKILL.md" | grep -E '^name:' | sed 's/^name:[[:space:]]*//')"
    [ "$front" = "$name" ] || fail "$name: SKILL.md frontmatter name is '$front'"
  fi
  echo "  ok  $kind $name"
done < <(jq -r '.entries[] | [.name, .kind, (.path // "null")] | @tsv' "$ROOT/library/catalog.json")

# Every bundle on disk is in the catalog.
for dir in "$ROOT"/library/skills/*/; do
  bundle="$(basename "$dir")"
  jq -e --arg b "$bundle" '.entries[] | select(.kind == "skill" and .name == $b)' "$ROOT/library/catalog.json" > /dev/null \
    || fail "library/skills/$bundle is on disk but not in the catalog"
done

# Every need an entry names is a declared need.
while IFS= read -r need; do
  jq -e --arg n "$need" '.needs[$n]' "$ROOT/library/catalog.json" > /dev/null || fail "need '$need' is used but not declared"
done < <(jq -r '.entries[].needs[]' "$ROOT/library/catalog.json" | sort -u)

echo
echo "== templates =="
# Every placeholder in skeleton/, handoff/ and library/harness/ is one
# spawn.py can fill. The list is read from spawn.py itself, so a new
# placeholder needs a value before it can be used.
python3 - "$ROOT" <<'PY' || fails=$((fails + 1))
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
src = (root / "scripts/spawn.py").read_text()
known = set(re.findall(r'"([A-Z][A-Z0-9_]+)":', src)) | set(re.findall(r'hv\["([A-Z0-9_]+)"\]', src)) | set(re.findall(r'values\["([A-Z0-9_]+)"\]', src)) | {"REPO_NAME", "SCHEMA_JOB"}
bad = 0
for folder in ("skeleton", "handoff", "library/harness"):
    for path in (root / folder).rglob("*"):
        if path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for key in sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text + str(path))) ):
            if key not in known:
                print(f"FAIL: {path.relative_to(root)} uses {{{{{key}}}}}, which spawn.py never sets")
                bad += 1
print(f"  placeholders: {len(known)} known, {'no' if not bad else bad} unknown")
sys.exit(1 if bad else 0)
PY

echo
echo "== json and shell =="
while IFS= read -r f; do
  jq -e . "$f" > /dev/null 2>&1 || fail "$f does not parse"
done < <(find "$ROOT/library" "$ROOT/examples" "$ROOT/.claude" -name '*.json' -not -path '*/node_modules/*' 2>/dev/null)
while IFS= read -r f; do
  bash -n "$f" || fail "$f has a syntax error"
done < <(find "$ROOT/scripts" "$ROOT/skeleton" "$ROOT/library/harness" "$ROOT/.claude" -name '*.sh' 2>/dev/null)
python3 -m py_compile "$ROOT"/scripts/*.py || fail "a python script does not compile"
echo "  ok  json parses, shell and python compile"

echo
if [ "$fails" -gt 0 ]; then
  echo "$fails problem(s)."
  exit 1
fi
echo "Library and skeleton are consistent."
