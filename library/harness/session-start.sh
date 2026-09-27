#!/bin/bash
# SessionStart hook for this repository.
#
# This repo carries no application code, so there are no packages to
# install. What it carries is skill bundles, and two things have to be true
# before a session can use them:
#
#   1. The directives in .claude/session-context.md reach the model.
#   2. python3 exists, because task-observer ships two scripts that need it.
#
# Both are reported rather than assumed. A hook that fails quietly is worse
# than no hook: the session looks configured and is not.

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
CONTEXT_FILE="$ROOT/.claude/session-context.md"

warnings=()

if [ ! -r "$CONTEXT_FILE" ]; then
  warnings+=("session-context.md is missing or unreadable at $CONTEXT_FILE; the repo's skill directives did not load.")
fi

if ! command -v python3 >/dev/null 2>&1; then
  warnings+=("python3 not found; task-observer's migrate-log.py and validate-skill-bundle.py cannot run.")
fi

context=""
[ -r "$CONTEXT_FILE" ] && context="$(cat "$CONTEXT_FILE")"

if [ ${#warnings[@]} -gt 0 ]; then
  context+=$'\n\n## Session start warnings\n\n'
  for w in "${warnings[@]}"; do
    context+="- $w"$'\n'
  done
fi

# jq gives us the documented JSON envelope. Without it, stdout from a
# SessionStart hook is added to context anyway, so the directives still
# land; only the envelope is lost.
if command -v jq >/dev/null 2>&1; then
  printf '%s' "$context" | jq -Rs \
    '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:.}}'
else
  printf '%s\n' "$context"
fi
