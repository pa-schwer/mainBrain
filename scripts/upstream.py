"""Find structural changes in a spawned project that belong in mainBrain,
and mainBrain changes the project has not taken yet.

    python3 scripts/upstream.py /path/to/<project>-ops            # report
    python3 scripts/upstream.py /path/to/<project>-ops --patch     # also write patches against skeleton/

Reads the manifest that spawn.py left in <project>-ops/.mainbrain/,
re-renders the skeleton with the same answers into a temporary directory,
and diffs every skeleton-owned file against the live repo next to ops.
A file the project changed is a candidate to upstream; a file mainBrain
changed since the spawn is a candidate to pull down. Feature code is never
listed: only paths the skeleton generated are compared.

With --patch, each changed file is reverse-rendered (project values back
to {{PLACEHOLDERS}}) and written as a unified diff against the skeleton
template under <ops>/.mainbrain/upstream/, ready to read, trim and apply
to mainBrain with `git apply`. Standard library only.
"""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import is_text, render, reverse  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Rendered from the same skeleton file for every project, so the reverse
# render maps them back to one template.
SHARED_SOURCES = {
    "scripts/no-hardcoded-tokens.sh": "skeleton/_shared/no-hardcoded-tokens.sh",
    "src/styles/tokens.css": "skeleton/_shared/tokens.css",
}

# Generated, not templated: compared, never patched back.
NOT_TEMPLATED = {".mainbrain/manifest.json", ".mainbrain/answers.json", ".claude/settings.json", ".claude/session-context.md"}


def respawn(spawn_py: Path, answers: Path, out: Path) -> None:
    cmd = [sys.executable, str(spawn_py), str(answers), "--out", str(out), "--no-install", "--no-git", "--force"]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def owned_paths(owned: list[str]) -> list[str]:
    return [rel for rel in owned if " " not in rel]  # install log lines ("skill   x") are not paths


def template_for(kind: str, rel: str, values: dict[str, str]) -> Path | None:
    if rel in SHARED_SOURCES:
        return ROOT / SHARED_SOURCES[rel]
    if rel in NOT_TEMPLATED or rel.startswith((".claude/skills/", ".claude/agents/", ".claude/commands/")):
        return None
    if rel.startswith(".claude/hooks/") or rel in (".claude/claude-security-guidance.md", ".claude/security-patterns.json"):
        return ROOT / "library/harness" / Path(rel).name
    # a file name may itself carry a placeholder (.env.<project>-staging)
    candidate = ROOT / "skeleton" / kind / reverse(rel, values)
    return candidate if candidate.exists() else None


def changed_in_project(manifest: dict, workspace: Path, fresh_ws: Path, ops_name: str) -> list[tuple[str, str, str]]:
    """(repo, rel, kind) for every skeleton-owned file the project changed."""
    project = manifest["answers"]["project"]
    changed: list[tuple[str, str, str]] = []
    for repo, owned in manifest["skeleton_owned"].items():
        kind = repo[len(project) + 1:]
        live_repo = workspace / repo
        if not live_repo.exists():
            print(f"skip    {repo} is not next to {ops_name}")
            continue
        for rel in owned_paths(owned):
            live = live_repo / rel
            fresh = fresh_ws / repo / rel
            if not live.exists():
                print(f"deleted {repo}/{rel} (skeleton file removed in the project)")
                continue
            if fresh.exists() and is_text(live) and live.read_bytes() != fresh.read_bytes():
                changed.append((repo, rel, kind))
    return changed


def changed_in_mainbrain(manifest: dict, answers: Path, fresh_ws: Path) -> list[tuple[str, str]]:
    """What mainBrain changed since the spawn: the fresh render vs the
    render at the recorded commit. Only when that commit is reachable."""
    commit = manifest["mainbrain_commit"]
    if commit == "uncommitted":
        return []
    project = manifest["answers"]["project"]
    changed: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory() as old:
        worktree = Path(old) / "mb"
        try:
            subprocess.run(["git", "worktree", "add", "--detach", "--quiet", str(worktree), commit], cwd=ROOT, check=True, capture_output=True)
            respawn(worktree / "scripts/spawn.py", answers, Path(old) / "ws")
            for repo, owned in manifest["skeleton_owned"].items():
                for rel in owned_paths(owned):
                    a = Path(old) / "ws" / project / repo / rel
                    b = fresh_ws / repo / rel
                    if a.exists() and b.exists() and a.read_bytes() != b.read_bytes():
                        changed.append((repo, rel))
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, capture_output=True)
    return changed


def write_patches(changed: list[tuple[str, str, str]], workspace: Path, values: dict[str, str], out_dir: Path) -> int:
    """Reverse-render each changed file and diff it against its template. Returns how many were written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for repo, rel, kind in changed:
        template = template_for(kind, rel, values)
        if template is None:
            continue
        # The schema CI job is a shared fragment rendered into every
        # product repo's workflow; fold it back to its placeholder so
        # the patch shows only what the project changed.
        repo_values = dict(values, REPO_NAME=repo)
        if kind != "ops":
            repo_values["SCHEMA_JOB"] = render((ROOT / "skeleton/_shared/schema-job.yml").read_text(encoding="utf-8"), repo_values, "schema-job.yml")
        live_text = reverse((workspace / repo / rel).read_text(encoding="utf-8"), repo_values)
        tmpl_text = template.read_text(encoding="utf-8")
        rel_template = template.relative_to(ROOT)
        patch = "".join(difflib.unified_diff(tmpl_text.splitlines(keepends=True), live_text.splitlines(keepends=True),
                                             fromfile=f"a/{rel_template}", tofile=f"b/{rel_template}"))
        if not patch:
            continue
        name = f"{repo}__{rel.replace('/', '__')}.patch"
        (out_dir / name).write_text(patch, encoding="utf-8")
        written += 1
    return written


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ops", type=Path)
    parser.add_argument("--patch", action="store_true")
    args = parser.parse_args(argv)

    ops = args.ops.resolve()
    manifest_path = ops / ".mainbrain/manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"{ops} has no .mainbrain/manifest.json; it was not spawned by mainBrain")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    answers = manifest["answers"]
    answers_file = ops / ".mainbrain/answers.json"
    workspace = ops.parent

    # Values for the reverse render: the scalar answers only. Derived
    # blocks (tables, maps) cannot be reversed and are left as they are.
    values = {
        "PROJECT": answers["project"],
        "TITLE": answers["title"],
        "DESCRIPTION": answers["description"],
        "OWNER": answers["owner"],
        "DOMAIN": answers["domain"],
        "APP_DOMAIN": answers["app_domain"],
        "API_DOMAIN": answers["api_domain"],
        "FIREBASE_STAGING": answers["firebase_staging"],
        "FIREBASE_PROD": answers["firebase_prod"],
        "DATE": manifest["spawned_on"],
    }

    with tempfile.TemporaryDirectory() as tmp:
        respawn(ROOT / "scripts/spawn.py", answers_file, Path(tmp))
        fresh_ws = Path(tmp) / answers["project"]
        changed_here = changed_in_project(manifest, workspace, fresh_ws, ops.name)
        changed_upstream = changed_in_mainbrain(manifest, answers_file, fresh_ws)

    print(f"manifest: spawned {manifest['spawned_on']} from mainBrain {manifest['mainbrain_commit'][:12]}")
    print()
    print(f"== changed in the project since spawn ({len(changed_here)}) : candidates to upstream ==")
    for repo, rel, _ in changed_here:
        print(f"  {repo}/{rel}")
    print()
    print(f"== changed in mainBrain since spawn ({len(changed_upstream)}) : candidates to pull down ==")
    for repo, rel in changed_upstream:
        print(f"  {repo}/{rel}")

    if args.patch and changed_here:
        out_dir = ops / ".mainbrain/upstream"
        written = write_patches(changed_here, workspace, values, out_dir)
        print()
        print(f"wrote {written} patch(es) to {out_dir}. Read each, drop the project-specific hunks, then in mainBrain:")
        print(f"  git apply --3way {out_dir}/<name>.patch")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
