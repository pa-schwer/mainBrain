#!/usr/bin/env bash
# Spawn a project workspace from an answers file.
#
#   bash scripts/spawn.sh examples/answers.example.json [--out DIR] [--no-install] [--no-git] [--force]
#
# Checks the prerequisites, then hands over to scripts/spawn.py. Never
# writes a secret, never talks to GitHub, Firebase or Cloudflare.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
missing=0
for tool in python3 git node npm; do
  if ! command -v "$tool" > /dev/null 2>&1; then
    echo "MISSING $tool"
    missing=$((missing + 1))
  fi
done
[ "$missing" -gt 0 ] && exit 1

if command -v node > /dev/null 2>&1; then
  major="$(node -p 'process.versions.node.split(".")[0]')"
  if [ "$major" -lt 22 ]; then
    echo "node is v$major; the generated repos target Node 22"
    exit 1
  fi
fi

exec python3 "$ROOT/scripts/spawn.py" "$@"
