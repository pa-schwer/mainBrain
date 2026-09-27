#!/usr/bin/env bash
# Compare a child ops repo's installed skills, agent, command and harness
# with the mainBrain library. Direction-agnostic: a difference is either
# an improvement to bring up here, or an update to push down there.
#
#   bash scripts/check-drift.sh /path/to/<project>-ops
#
# Exit 0 = identical. Exit 1 = drift, with the diff printed. A skill the
# child has that the library lacks is listed, not diffed: it is a
# candidate for the library.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPS="${1:?usage: check-drift.sh <ops-repo>}"
OPS="$(cd "$OPS" && pwd)"
[ -d "$OPS/.claude" ] || { echo "$OPS has no .claude directory"; exit 1; }

drift=0

compare() {
  local label="$1" lib="$2" child="$3"
  if [ ! -e "$child" ]; then
    echo "absent  $label (not installed in the child)"
    return
  fi
  if diff -rq -x '__pycache__' -x '*.pyc' "$lib" "$child" > /dev/null 2>&1; then
    echo "same    $label"
  else
    echo "DRIFT   $label"
    diff -ru -x '__pycache__' -x '*.pyc' "$lib" "$child" | sed 's/^/        /'
    drift=$((drift + 1))
  fi
}

echo "== skills =="
for dir in "$ROOT"/library/skills/*/; do
  name="$(basename "$dir")"
  compare "skills/$name" "$dir" "$OPS/.claude/skills/$name"
done
for dir in "$OPS"/.claude/skills/*/; do
  [ -d "$dir" ] || continue
  name="$(basename "$dir")"
  [ -d "$ROOT/library/skills/$name" ] || { echo "NEW     skills/$name exists in the child only: a candidate for the library"; drift=$((drift + 1)); }
done

echo
echo "== agent, command =="
compare "agents/code-simplifier.md" "$ROOT/library/agents/code-simplifier.md" "$OPS/.claude/agents/code-simplifier.md"
compare "commands/mem.md" "$ROOT/library/commands/mem.md" "$OPS/.claude/commands/mem.md"

echo
echo "== harness (rendered files differ by project name; only the hook and the patterns are byte-comparable) =="
compare "hooks/session-start.sh" "$ROOT/library/harness/session-start.sh" "$OPS/.claude/hooks/session-start.sh"
compare "security-patterns.json" "$ROOT/library/harness/security-patterns.json" "$OPS/.claude/security-patterns.json"

echo
if [ "$drift" -gt 0 ]; then
  echo "$drift difference(s). Read each one and decide the direction:"
  echo "  child is better  -> edit the library here, commit, then re-install in every child"
  echo "  library is newer -> python3 scripts/skills.py install $OPS --only <name>"
  echo "For structural files outside .claude/, run scripts/upstream.py."
  exit 1
fi
echo "No drift between the library and $OPS."
