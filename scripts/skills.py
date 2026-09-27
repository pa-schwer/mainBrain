"""The skills library: read the catalog, pick entries for a project, install them.

Used by spawn.py and runnable on its own:

    python3 scripts/skills.py select --repos site,app --needs motion
    python3 scripts/skills.py install <ops-dir> --repos site,app --needs motion
    python3 scripts/skills.py install <ops-dir> --only stop-slop,animate

Standard library only. python3 is already a prerequisite of the harness
(task-observer ships two scripts that need it).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library"
CATALOG = LIBRARY / "catalog.json"

STANDING_MODES = {"standing", "automatic"}


def load_catalog() -> dict:
    with CATALOG.open(encoding="utf-8") as fh:
        return json.load(fh)


def select(repos: list[str], needs: list[str], exclude: list[str], only: list[str] | None = None) -> list[dict]:
    """Entries a project gets: defaults for its repo kinds plus the needs it named.

    `only` bypasses the mapping and takes the names as given; it still
    validates them against the catalog.
    """
    catalog = load_catalog()
    by_name = {e["name"]: e for e in catalog["entries"]}
    known_needs = set(catalog["needs"])

    unknown = sorted(set(needs) - known_needs)
    if unknown:
        raise SystemExit(f"unknown need(s): {', '.join(unknown)}. Known: {', '.join(sorted(known_needs))}")

    if only is not None:
        missing = sorted(set(only) - set(by_name))
        if missing:
            raise SystemExit(f"unknown skill(s): {', '.join(missing)}")
        return [by_name[n] for n in only]

    repo_set, need_set = set(repos), set(needs)
    return [
        entry for entry in catalog["entries"]
        if entry["name"] not in exclude
        and (repo_set & set(entry["default_for"]) or need_set & set(entry["needs"]))
    ]


def _copy_into(src: Path, dst_dir: Path, name: str | None = None) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_dir / (name or src.name))


def install(ops_dir: Path, entries: list[dict]) -> list[str]:
    """Copy each entry into the ops repo's .claude tree. Returns what landed."""
    claude = ops_dir / ".claude"
    landed = []
    for entry in entries:
        kind = entry["kind"]
        if kind == "skill":
            dst = claude / "skills" / entry["name"]
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(LIBRARY / entry["path"], dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            landed.append(f"skill   {entry['name']}")
        elif kind == "agent":
            _copy_into(LIBRARY / entry["path"], claude / "agents")
            _copy_into(LIBRARY / "agents" / "LICENSE", claude / "agents")
            landed.append(f"agent   {entry['name']}")
        elif kind == "command":
            _copy_into(LIBRARY / entry["path"], claude / "commands")
            _copy_into(LIBRARY / "commands" / "LICENSE-mem", claude / "memory", "LICENSE")
            landed.append(f"command {entry['name']}")
        elif kind == "plugin":
            # Enabled through settings.json; nothing to copy except the
            # repo rules that security-guidance reads.
            landed.append(f"plugin  {entry['plugin_id']}")
        else:
            raise SystemExit(f"catalog entry {entry['name']} has unknown kind {kind}")
    return landed


def plugin_ids(entries: list[dict]) -> list[str]:
    return [e["plugin_id"] for e in entries if e["kind"] == "plugin"]


def standing(entries: list[dict]) -> list[dict]:
    return [e for e in entries if e["kind"] != "plugin" and e["mode"] in STANDING_MODES]


def on_demand(entries: list[dict]) -> list[dict]:
    return [e for e in entries if e["kind"] != "plugin" and e["mode"] not in STANDING_MODES]


def table(entries: list[dict]) -> str:
    rows = []
    for e in entries:
        note = " (local change)" if e.get("local_change") else ""
        rows.append(f"| {e['name']}{note} | {e['mode']} | {e['origin']} | {e['license']} |")
    return "\n".join(rows)


def _split(value: str | None) -> list[str]:
    return [v for v in (value or "").split(",") if v]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("select", "install"):
        p = sub.add_parser(name)
        if name == "install":
            p.add_argument("ops_dir", type=Path)
        p.add_argument("--repos", default="ops")
        p.add_argument("--needs", default="")
        p.add_argument("--exclude", default="")
        p.add_argument("--only", default=None)
    args = parser.parse_args(argv)

    only = None if args.only is None else _split(args.only)
    entries = select(_split(args.repos), _split(args.needs), _split(args.exclude), only)
    if args.cmd == "select":
        for e in entries:
            print(f"{e['kind']:8}{e['mode']:10}{e['name']}")
        return 0

    ops_dir: Path = args.ops_dir
    if not (ops_dir / "CLAUDE.md").exists():
        raise SystemExit(f"{ops_dir} does not look like an ops repo (no CLAUDE.md)")
    for line in install(ops_dir, entries):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
