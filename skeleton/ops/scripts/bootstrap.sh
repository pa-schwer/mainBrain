#!/usr/bin/env bash
# Bring a fresh machine to a working {{PROJECT}} workspace.
#
# Clones the sibling repos next to {{PROJECT}}-ops, installs their deps, and
# reports which environment prerequisites are missing. Safe to re-run: an
# existing clone is fetched rather than re-cloned, and installs are
# idempotent.
#
# This script never writes a secret and never deploys.

set -uo pipefail

OPS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="$(dirname "$OPS_ROOT")"
GH_OWNER="${GH_OWNER:-{{OWNER}}}"

SIBLINGS=({{SIBLINGS}})

failures=0

echo "workspace: $WORKSPACE"
echo "owner:     $GH_OWNER  (override with GH_OWNER)"
echo

# ---------------------------------------------------------------- prereqs
echo "== prerequisites =="
check_tool() {
  local tool="$1" why="$2"
  if command -v "$tool" > /dev/null 2>&1; then
    printf '  ok      %-12s %s\n' "$tool" "$($tool --version 2>&1 | head -1)"
  else
    printf '  MISSING %-12s %s\n' "$tool" "$why"
    return 1
  fi
}

check_tool git  "required to clone anything" || failures=$((failures + 1))
check_tool node "Node 22"                    || failures=$((failures + 1))
check_tool npm  "dependency install"         || failures=$((failures + 1))

# Needed to deploy, not to develop. Absence is reported, never fatal.
for optional in firebase wrangler; do
  if command -v "$optional" > /dev/null 2>&1; then
    printf '  ok      %-12s %s\n' "$optional" "$($optional --version 2>&1 | head -1)"
  else
    printf '  absent  %-12s deploy only; not needed to build or test\n' "$optional"
  fi
done

if command -v node > /dev/null 2>&1; then
  major="$(node -p 'process.versions.node.split(".")[0]')"
  if [ "$major" -lt 22 ]; then
    echo "  FAIL    node is v$major; every repo targets Node 22"
    failures=$((failures + 1))
  fi
fi

# ----------------------------------------------------------------- clones
echo
echo "== siblings =="
for repo in "${SIBLINGS[@]}"; do
  dest="$WORKSPACE/$repo"
  if [ -d "$dest/.git" ]; then
    echo "  fetch  $repo"
    git -C "$dest" fetch --quiet origin || {
      echo "         fetch failed"
      failures=$((failures + 1))
    }
  elif [ -e "$dest" ]; then
    echo "  FAIL   $dest exists and is not a git repo"
    failures=$((failures + 1))
  else
    echo "  clone  $repo"
    git clone --quiet "https://github.com/$GH_OWNER/$repo.git" "$dest" || {
      echo "         clone failed; does $GH_OWNER/$repo exist and do you have access?"
      failures=$((failures + 1))
    }
  fi
done

# ------------------------------------------------------------- deps
echo
echo "== dependencies =="
for repo in "${SIBLINGS[@]}"; do
  dest="$WORKSPACE/$repo"
  if [ ! -f "$dest/package.json" ]; then
    echo "  skip   $repo (no package.json yet)"
    continue
  fi
  echo "  npm i  $repo"
  (cd "$dest" && npm install --silent) || {
    echo "         install failed"
    failures=$((failures + 1))
  }
done

# ------------------------------------------------------------- schema
echo
echo "== schema =="
# Invoked through bash, not executed directly: a checkout that lost the
# exec bit must not turn a schema check into a silent skip.
bash "$OPS_ROOT/scripts/check-schema.sh" || failures=$((failures + 1))

# ------------------------------------------------------------- verdict
echo
if [ "$failures" -gt 0 ]; then
  echo "bootstrap finished with $failures problem(s). Read the lines marked"
  echo "MISSING or FAIL above; nothing else needs fixing."
  exit 1
fi

echo "Workspace ready."
echo
echo "Secrets are not handled here. None of them belongs in a file in this"
echo "workspace; docs/environments.md says where each one lives."
exit 0
