#!/usr/bin/env bash
# Diff the canonical schema against the product-repo copies.
#
# {{PROJECT}}-ops owns docs/schema/types.ts. Every copy must be
# byte-identical. Run this before any commit that touches a data shape, and
# in the product repos' CI.
#
# Exit 0 = no drift. Exit 1 = drift, or a copy is missing from a repo that
# is present. A sibling that is not cloned is skipped with a note, because
# this has to be runnable from a machine that only has ops.

set -uo pipefail

OPS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="$(dirname "$OPS_ROOT")"
CANONICAL="$OPS_ROOT/docs/schema/types.ts"

COPIES=(
{{SCHEMA_COPIES_ARRAY}}
)

if [ ! -f "$CANONICAL" ]; then
  echo "FAIL: canonical schema missing at $CANONICAL"
  exit 1
fi

if [ "${#COPIES[@]}" -eq 0 ]; then
  echo "No product repo holds a schema copy. Nothing to check."
  exit 0
fi

drift=0
skipped=0
checked=0

for rel in "${COPIES[@]}"; do
  repo="${rel%%/*}"
  copy="$WORKSPACE/$rel"

  if [ ! -d "$WORKSPACE/$repo" ]; then
    echo "skip: $repo is not cloned at $WORKSPACE/$repo"
    skipped=$((skipped + 1))
    continue
  fi

  if [ ! -f "$copy" ]; then
    echo "FAIL: $repo is cloned but $rel is missing"
    drift=$((drift + 1))
    continue
  fi

  tmp="$(mktemp)"
  if diff -u "$CANONICAL" "$copy" > "$tmp" 2>&1; then
    echo "ok:   $rel"
    checked=$((checked + 1))
  else
    echo "FAIL: $rel has drifted from the canonical schema"
    sed 's/^/      /' "$tmp"
    drift=$((drift + 1))
  fi
  rm -f "$tmp"
done

echo
if [ "$drift" -gt 0 ]; then
  echo "SCHEMA DRIFT: $drift of ${#COPIES[@]} copies are wrong."
  echo "Fix by copying $CANONICAL over the offending file, in the same work"
  echo "cycle as the change that caused it. Never edit a copy directly."
  exit 1
fi

if [ "$checked" -eq 0 ]; then
  echo "No copies checked; $skipped sibling(s) not cloned. Run scripts/bootstrap.sh first."
  exit 0
fi

echo "Schema in sync across $checked copy/copies. $skipped skipped."
exit 0
