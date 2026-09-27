"""Generate a project workspace from an answers file.

    python3 scripts/spawn.py examples/answers.example.json --out /path/to/parent

Reads the answers, renders the skeleton for each requested repo kind,
copies the schema into every product repo, installs the harness and the
selected skills into the ops repo, writes HANDOFF.md with the human steps
that remain for that stack, installs dependencies, runs every check, and
makes the first commit of each repo on `main`.

Nothing here talks to GitHub, Firebase or Cloudflare. What needs those is
in the generated HANDOFF.md. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skills  # noqa: E402
from render import is_text, leftovers, render  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SKELETON = ROOT / "skeleton"
SHARED = SKELETON / "_shared"
HANDOFF = ROOT / "handoff"
LIBRARY = ROOT / "library"

KINDS = ("ops", "site", "functions", "app", "lib")
SLUG = re.compile(r"^[a-z][a-z0-9-]{1,30}$")

# Where each product repo keeps its byte-identical schema copy.
SCHEMA_COPY = {
    "functions": "src/schema/types.ts",
    "app": "src/schema/types.ts",
    "site": "src/lib/schema.ts",
    "lib": "src/schema/types.ts",
}

PURPOSE = {
    "ops": "orchestrator, never product code",
    "site": "public site — Astro + Tailwind → Cloudflare Workers",
    "functions": "back end — Firebase Cloud Functions v2 + Firestore",
    "app": "dashboard — Vite/React → Cloudflare Workers",
    "lib": "pure logic — TypeScript, no I/O, no deploy target",
}

FORBIDDEN = {
    "ops": "product code of any kind",
    "site": "state, business logic",
    "functions": "HTML",
    "app": "business logic — it reads Firestore and calls functions",
    "lib": "network, database or file system access",
}

FRONTEND = {"site", "app"}
FIREBASE = {"functions", "app"}


# ----------------------------------------------------------------- answers
def load_answers(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        answers = json.load(fh)

    required = ("project", "title", "description", "owner", "repos")
    missing = [k for k in required if not answers.get(k)]
    if missing:
        raise SystemExit(f"answers file is missing: {', '.join(missing)}")
    if not SLUG.match(answers["project"]):
        raise SystemExit("project must be a slug: lowercase letters, digits, dashes, 2-31 chars")

    repos = list(dict.fromkeys(["ops", *answers["repos"]]))
    unknown = [r for r in repos if r not in KINDS]
    if unknown:
        raise SystemExit(f"unknown repo kind(s): {', '.join(unknown)}. Known: {', '.join(KINDS)}")
    answers["repos"] = [k for k in KINDS if k in repos]

    answers.setdefault("domain", f"{answers['project']}.example")
    answers.setdefault("app_domain", f"app.{answers['domain']}")
    answers.setdefault("api_domain", f"api.{answers['domain']}")
    answers.setdefault("region", "us-central1")
    answers.setdefault("copy_language", "US English")
    answers.setdefault("html_lang", "en")
    answers.setdefault("firebase_staging", f"{answers['project']}-staging")
    answers.setdefault("firebase_prod", f"{answers['project']}-prod")
    answers.setdefault("needs", [])
    answers.setdefault("skills_exclude", [])
    answers.setdefault("secrets", [])
    answers.setdefault("services", [])
    return answers


# ------------------------------------------------------------------ values
def repo_name(project: str, kind: str) -> str:
    return f"{project}-{kind}"


def build_values(a: dict, entries: list[dict], today: str) -> dict[str, str]:
    p = a["project"]
    repos = a["repos"]
    names = [repo_name(p, k) for k in repos]
    product = [k for k in repos if k != "ops"]

    arch = "\n".join(f"├── {repo_name(p, k) + '/':<20}{PURPOSE[k]}" for k in repos)
    arch = arch.rsplit("├──", 1)
    arch = "└──".join(arch) if len(arch) == 2 else arch[0]

    copies = [f"{repo_name(p, k)}/{SCHEMA_COPY[k]}" for k in product]
    secret_names = ", ".join(f"`{s['name']}`" for s in a["secrets"])

    standing = skills.standing(entries)
    on_demand = skills.on_demand(entries)

    values = {
        "PROJECT": p,
        "TITLE": a["title"],
        "DESCRIPTION": a["description"],
        "OWNER": a["owner"],
        "DOMAIN": a["domain"],
        "APP_DOMAIN": a["app_domain"],
        "API_DOMAIN": a["api_domain"],
        "REGION": a["region"],
        "COPY_LANGUAGE": a["copy_language"],
        "HTML_LANG": a["html_lang"],
        "FIREBASE_STAGING": a["firebase_staging"],
        "FIREBASE_PROD": a["firebase_prod"],
        "DATE": today,
        "REPO_COUNT": str(len(repos)),
        "REPO_LIST": ", ".join(f"`{n}`" for n in names),
        "REPO_DIRS": " ".join(names),
        "SIBLINGS": " ".join(repo_name(p, k) for k in product),
        "ARCHITECTURE_MAP": arch,
        "FORBIDDEN_ZONES": "\n".join(f"| `{repo_name(p, k)}` | {FORBIDDEN[k]} |" for k in repos),
        "SCHEMA_COPY_LIST": "\n".join(f"- `{c}`" for c in copies) or "- (no product repo yet)",
        "SCHEMA_COPY_COMMENT": "\n".join(f"//   {c}" for c in copies) or "//   (no product repo yet)",
        "SCHEMA_COPIES_ARRAY": "\n".join(f'  "{c}"' for c in copies),
        "SECRET_NAMES": secret_names or "(none declared yet)",
        "SECRET_NAMES_OR_NONE": secret_names or "none yet; the first cycle that reads one declares it and names the HANDOFF step",
        "STANDING_SKILLS": ", ".join(e["name"] for e in standing),
        "ON_DEMAND_SKILLS_OR_NONE": ", ".join(e["name"] for e in on_demand) or "no on-demand skill is installed yet; `find-skills` and the mainBrain library",
        "SKILLS_TABLE": skills.table(entries),
        "PLUGIN_LIST": ", ".join(f"`{pid}`" for pid in skills.plugin_ids(entries)) or "no plugin",
        "GITHUB_SECRETS_TABLE": github_secrets_table(a),
        "FIREBASE_SECTION": firebase_section(a),
        "CLOUDFLARE_SECTION": cloudflare_section(a),
        "SERVICES_TABLE": "\n".join(
            f"| {s['name']} | {s.get('staging', 'test mode')} | {s.get('prod', 'live mode')} | {', '.join(f'`{n}`' for n in s.get('secrets', [])) or '—'} |"
            for s in a["services"]
        ) or "| (none yet) | | | |",
    }
    values["SCHEMA_JOB"] = ""  # per repo, set in render_repo
    values["REPO_NAME"] = ""
    return values


def github_secrets_table(a: dict) -> str:
    p = a["project"]
    rows = []
    for k in a["repos"]:
        if k == "ops":
            continue
        rows.append(f"| `{repo_name(p, k)}` | `OPS_READ_TOKEN` | PAT, Contents: read on `{a['owner']}/{repo_name(p, 'ops')}` |")
    if "functions" in a["repos"]:
        rows.append(f"| `{repo_name(p, 'functions')}` | `FIREBASE_SERVICE_ACCOUNT_STAGING` | service account JSON, {a['firebase_staging']} |")
        rows.append(f"| `{repo_name(p, 'functions')}` | `FIREBASE_SERVICE_ACCOUNT_PROD` | service account JSON, {a['firebase_prod']} |")
    return "\n".join(rows) or "| (none) | | |"


def firebase_section(a: dict) -> str:
    if not FIREBASE & set(a["repos"]):
        return "## Firebase\n\nNot used: no functions repo and no app repo."
    p = a["project"]
    lines = [
        "## Firebase",
        "",
        "| | staging | prod |",
        "|---|---|---|",
        f"| Project ID | `{a['firebase_staging']}` | `{a['firebase_prod']}` |",
        f"| Region | `{a['region']}` | `{a['region']}` |",
        "| Firestore | Native mode | Native mode |",
    ]
    if "functions" in a["repos"]:
        lines.append(f"| Deploys from | `main` of `{repo_name(p, 'functions')}` | `prod` of `{repo_name(p, 'functions')}` |")
    if "app" in a["repos"]:
        lines += [
            "",
            "### Web app config",
            "",
            "Public by construction: it ships inside the dashboard bundle. The security",
            f"boundary is `firestore.rules` in `{repo_name(p, 'functions') if 'functions' in a['repos'] else 'the functions repo'}`. The two configs are",
            f"committed in `{repo_name(p, 'app')}` as `.env.staging` and `.env.production`;",
            "`scripts/build.mjs` picks one by branch.",
        ]
    lines += [
        "",
        "### Secret Manager, per project",
        "",
        "| Name | Used by | Needed from |",
        "|---|---|---|",
    ]
    for s in a["secrets"]:
        lines.append(f"| `{s['name']}` | {s.get('used_by', 'functions')} | {s.get('needed_from', 'the cycle that first reads it')} |")
    if not a["secrets"]:
        lines.append("| (none declared yet) | | |")
    lines += [
        "",
        "A function that declares a secret fails to deploy until the secret exists",
        "in that project, so a secret is declared in the cycle that first reads it",
        "and created before that cycle's first deploy (HANDOFF.md, F6).",
        "",
        "### Deploy credential",
        "",
        "One service account key per project, held as `FIREBASE_SERVICE_ACCOUNT_STAGING`",
        "and `FIREBASE_SERVICE_ACCOUNT_PROD` in the functions repo. Four roles: Editor,",
        "Secret Manager Admin, Cloud Functions Admin, Cloud Run Admin (HANDOFF.md, F4).",
    ]
    return "\n".join(lines)


def cloudflare_section(a: dict) -> str:
    fronts = [k for k in a["repos"] if k in FRONTEND]
    if not fronts:
        return "## Cloudflare Workers\n\nNot used: no site repo and no app repo."
    p = a["project"]
    lines = [
        "## Cloudflare Workers",
        "",
        "Assets-only Workers built by Workers Builds on every push. `prod` is the",
        "production branch; every other branch is a preview, and `main` is staging.",
        "",
        "| Worker | Repo | Production branch | Build | Deploy | Domain |",
        "|---|---|---|---|---|---|",
    ]
    for k in fronts:
        domain = a["domain"] if k == "site" else a["app_domain"]
        lines.append(f"| `{repo_name(p, k)}` | `{a['owner']}/{repo_name(p, k)}` | `prod` | `npm run build` | `npx wrangler deploy` | `{domain}` |")
    return "\n".join(lines)


# --------------------------------------------------------------- rendering
def copy_rendered(src: Path, dst: Path, values: dict[str, str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if is_text(src):
        text = render(src.read_text(encoding="utf-8"), values, str(src))
        left = leftovers(text)
        if left:
            raise SystemExit(f"{src}: unresolved placeholder(s) {', '.join(left)}")
        dst.write_text(text, encoding="utf-8")
    else:
        shutil.copy2(src, dst)
    dst.chmod(src.stat().st_mode)


def render_repo(kind: str, out: Path, values: dict[str, str]) -> list[str]:
    """Render skeleton/<kind> into out. Returns the repo-relative paths the
    skeleton owns, so upstream.py can tell structure from feature code."""
    src_root = SKELETON / kind
    owned: list[str] = []
    per_repo = dict(values, REPO_NAME=out.name)
    per_repo["SCHEMA_JOB"] = render((SHARED / "schema-job.yml").read_text(encoding="utf-8"), per_repo, "schema-job.yml") if kind != "ops" else ""

    for src in sorted(src_root.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(src_root)
        rel_rendered = Path(render(str(rel), per_repo, str(src)))
        copy_rendered(src, out / rel_rendered, per_repo)
        owned.append(str(rel_rendered))

    if kind in FRONTEND:
        copy_rendered(SHARED / "no-hardcoded-tokens.sh", out / "scripts/no-hardcoded-tokens.sh", per_repo)
        copy_rendered(SHARED / "tokens.css", out / "src/styles/tokens.css", per_repo)
        owned += ["scripts/no-hardcoded-tokens.sh", "src/styles/tokens.css"]
    return owned


def install_harness(ops: Path, entries: list[dict], values: dict[str, str]) -> list[str]:
    claude = ops / ".claude"
    (claude / "hooks").mkdir(parents=True, exist_ok=True)
    owned = []

    copy_rendered(LIBRARY / "harness/session-start.sh", claude / "hooks/session-start.sh", values)
    copy_rendered(LIBRARY / "harness/claude-security-guidance.md", claude / "claude-security-guidance.md", values)
    copy_rendered(LIBRARY / "harness/security-patterns.json", claude / "security-patterns.json", values)
    owned += [".claude/hooks/session-start.sh", ".claude/claude-security-guidance.md", ".claude/security-patterns.json"]

    settings = json.loads((LIBRARY / "harness/settings.json").read_text(encoding="utf-8"))
    settings["enabledPlugins"] = {pid: True for pid in skills.plugin_ids(entries)}
    (claude / "settings.json").write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    owned.append(".claude/settings.json")

    # session-context.md lists only the standing directives that were installed.
    context = (LIBRARY / "harness/session-context.md").read_text(encoding="utf-8")
    installed = {e["name"] for e in entries}
    sections = re.split(r"(?m)^(?=## )", context)
    kept = [sections[0]]
    for section in sections[1:]:
        name = section.split(" ", 2)[1]
        if name in installed:
            kept.append(section)
    (claude / "session-context.md").write_text("".join(kept).rstrip() + "\n", encoding="utf-8")
    owned.append(".claude/session-context.md")

    for line in skills.install(ops, entries):
        owned.append(line)
    return owned


# ----------------------------------------------------------------- handoff
def write_handoff(ws: Path, a: dict, values: dict[str, str], entries: list[dict]) -> None:
    p = a["project"]
    repos = a["repos"]
    product = [k for k in repos if k != "ops"]
    fronts = [k for k in repos if k in FRONTEND]
    firebase = bool(FIREBASE & set(repos))

    groups = [("G", "GitHub", "every repo"), ("E", "Claude Code environment", "every session")]
    if firebase:
        groups.insert(1, ("F", "Firebase and Google Cloud", "functions, app"))
    if fronts:
        groups.insert(-1, ("C", "Cloudflare Workers", ", ".join(fronts)))
    if a["services"]:
        groups.insert(-1, ("S", "Third-party services", ", ".join(s["name"] for s in a["services"])))

    proofs = [
        ("G1", "the repo URLs open", "github.com"),
        ("G2", "`add_repo` returns a clone command", "a Claude Code session"),
        ("G3", "CI runs on every repo", "each repo → Actions"),
    ]
    if product:
        proofs.append(("G4", f"`schema matches {p}-ops` green", ", ".join(repo_name(p, k) for k in product) + " → Actions"))
    if firebase:
        proofs += [
            ("F1", "both projects open in the console", "console.firebase.google.com"),
            ("F2", "Plan: Blaze, one budget per project", "Usage and billing; Billing → Budgets"),
            ("F3", "both API pages say enabled", "console.developers.google.com"),
        ]
        if "functions" in repos:
            proofs.append(("F4", "`Deploy` green on `main`, all exports live", f"{p}-functions → Actions → Deploy"))
        if "app" in repos:
            proofs.append(("F5", "no blank value in `.env.staging` / `.env.production`", f"{p}-app"))
        if a["secrets"]:
            proofs.append(("F6", "every secret listed in both projects", "Secret Manager"))
    if fronts:
        proofs.append(("C1", "a `main` push shows a preview URL that serves the page", "Cloudflare → Workers & Pages"))
        proofs.append(("C2", "the domain serves the production Worker", "the browser"))
    if a["services"]:
        proofs.append(("S", "identifiers in `docs/environments.md`, deploy green", f"{p}-ops"))
    proofs += [
        ("E1", "the session lists every repo in scope", "a Claude Code session"),
        ("E2", "`npm test` works in a fresh session without install", "a Claude Code session"),
        ("E3", "plugins reported loaded", f"first session in {p}-ops"),
    ]

    hv = dict(values)
    hv["GROUPS_TABLE"] = "\n".join(f"| {g} | {n} | {w} |" for g, n, w in groups)
    hv["REPO_CREATE_LIST"] = "\n".join(f"- [ ] `{a['owner']}/{repo_name(p, k)}` → https://github.com/{a['owner']}/{repo_name(p, k)}" for k in repos)
    hv["OPS_TOKEN_REPO_LIST"] = "\n".join(f"   - [ ] `{repo_name(p, k)}`" for k in product) or "   - (no product repo yet)"
    hv["CF_REPO_LIST"] = "\n".join(f"- [ ] `{a['owner']}/{repo_name(p, k)}` → Worker `{repo_name(p, k)}`" for k in fronts)
    hv["CF_ENV_NOTE"] = (
        f", except `PUBLIC_API_BASE` on the site Worker if staging must post somewhere other than `https://{a['api_domain']}`"
        if "site" in fronts else ""
    )
    hv["CF_DOMAIN_LIST"] = "\n".join(
        f"- [ ] `{a['domain'] if k == 'site' else a['app_domain']}` → Worker `{repo_name(p, k)}`" for k in fronts
    )
    hv["SECRETS_TABLE"] = "\n".join(
        f"| `{s['name']}` | {s.get('service', '')} | {s.get('used_by', 'functions')} | from the {s.get('service', 'service')} test account | from the live account |"
        for s in a["secrets"]
    )
    hv["SERVICES_HANDOFF_TABLE"] = "\n".join(
        f"| {s['name']} | {s.get('staging', 'test mode')} | {s.get('prod', 'live mode')} | {', '.join(f'`{n}`' for n in s.get('secrets', [])) or '—'} | {s.get('where', 'the service dashboard')} |"
        for s in a["services"]
    )
    hv["PLAYWRIGHT_LINE"] = (
        "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 pip install --quiet playwright   # webapp-testing; browsers are at /opt/pw-browsers"
        if any(e["name"] == "webapp-testing" for e in entries) else "# (no browser testing skill installed)"
    )
    hv["PROOFS_TABLE"] = "\n".join(f"| {s} | {pr} | {w} |" for s, pr, w in proofs)

    parts = ["00-intro.md", "10-github.md"]
    if firebase:
        parts.append("20-firebase.md")
        if "app" in repos:
            parts.append("21-firebase-app.md")
        if a["secrets"]:
            parts.append("22-firebase-secrets.md")
    if fronts:
        parts.append("30-cloudflare.md")
    if a["services"]:
        parts.append("40-services.md")
    parts += ["50-claude.md", "90-verification.md"]

    text = "\n".join(render((HANDOFF / name).read_text(encoding="utf-8"), hv, name).rstrip() + "\n" for name in parts)
    left = leftovers(text)
    if left:
        raise SystemExit(f"HANDOFF.md: unresolved placeholder(s) {', '.join(left)}")
    (ws / "HANDOFF.md").write_text(text, encoding="utf-8")


def write_push_script(ws: Path, a: dict) -> None:
    names = [repo_name(a["project"], k) for k in a["repos"]]
    script = f"""#!/usr/bin/env bash
# Push main of every generated repo to its origin. Safe to re-run.
# The remotes were set by mainBrain at spawn time; the repos themselves
# are created by hand (HANDOFF.md, G1) because a GitHub App on a personal
# account cannot create them.
set -uo pipefail
cd "$(dirname "${{BASH_SOURCE[0]}}")"
failed=0
for repo in {' '.join(names)}; do
  echo "== $repo"
  if ! git -C "$repo" push -u origin main; then
    echo "   push failed. If the remote is not empty, it was created with a"
    echo "   README; recreate it empty (HANDOFF.md, G1) and re-run."
    failed=$((failed + 1))
  fi
done
[ "$failed" -eq 0 ] && echo "All repos pushed." || exit 1
"""
    path = ws / "push-all.sh"
    path.write_text(script, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


# ------------------------------------------------------------ install/check
def run(cmd: list[str], cwd: Path, log: Path) -> bool:
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"\n$ {' '.join(cmd)}   (in {cwd})\n")
        fh.flush()
        result = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT, text=True)
    return result.returncode == 0


def install_and_check(ws: Path, a: dict, log: Path) -> list[tuple[str, str, bool]]:
    results = []
    p = a["project"]
    for kind in a["repos"]:
        repo = ws / repo_name(p, kind)
        if kind == "ops":
            results.append((repo.name, "check-schema.sh", run(["bash", "scripts/check-schema.sh"], repo, log)))
            continue
        ok = run(["npm", "install", "--silent", "--no-audit", "--no-fund"], repo, log)
        results.append((repo.name, "npm install", ok))
        if not ok:
            continue
        results.append((repo.name, "npm run typecheck", run(["npm", "run", "typecheck", "--silent"], repo, log)))
        results.append((repo.name, "npm test", run(["npm", "test", "--silent"], repo, log)))
        if kind in FRONTEND:
            results.append((repo.name, "no-hardcoded-tokens.sh", run(["bash", "scripts/no-hardcoded-tokens.sh"], repo, log)))
        if kind == "site":
            results.append((repo.name, "npm run build", run(["npm", "run", "build", "--silent"], repo, log)))
        if kind == "app":
            results.append((repo.name, "vite build", run(["npx", "vite", "build"], repo, log)))
    return results


def git_init(ws: Path, a: dict, log: Path) -> None:
    p = a["project"]
    for kind in a["repos"]:
        repo = ws / repo_name(p, kind)
        env = dict(os.environ, GIT_AUTHOR_NAME="mainBrain", GIT_AUTHOR_EMAIL="mainbrain@localhost",
                   GIT_COMMITTER_NAME="mainBrain", GIT_COMMITTER_EMAIL="mainbrain@localhost")
        for cmd in (
            ["git", "init", "--quiet", "-b", "main"],
            ["git", "remote", "add", "origin", f"https://github.com/{a['owner']}/{repo.name}.git"],
            ["git", "add", "-A"],
            ["git", "commit", "--quiet", "-m", f"chore: scaffold {repo.name} from mainBrain\n\nGenerated by mainBrain spawn on {dt.date.today().isoformat()}. HANDOFF.md at the workspace root lists what a human still has to do."],
        ):
            with log.open("a", encoding="utf-8") as fh:
                fh.write(f"\n$ {' '.join(cmd)}   (in {repo})\n")
                fh.flush()
                subprocess.run(cmd, cwd=repo, env=env, stdout=fh, stderr=subprocess.STDOUT, check=True)


def mainbrain_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        return "uncommitted"


# -------------------------------------------------------------------- main
def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("answers", type=Path)
    parser.add_argument("--out", type=Path, default=None, help="parent directory; the workspace is <out>/<project>. Default: next to mainBrain")
    parser.add_argument("--no-install", action="store_true", help="skip npm install and the checks")
    parser.add_argument("--no-git", action="store_true", help="skip git init and the first commit")
    parser.add_argument("--force", action="store_true", help="replace an existing workspace")
    args = parser.parse_args(argv)

    a = load_answers(args.answers)
    today = dt.date.today().isoformat()
    parent = args.out or ROOT.parent
    ws = parent / a["project"]
    if ws.exists():
        if not args.force:
            raise SystemExit(f"{ws} exists. Pass --force to replace it.")
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    log = ws / "spawn.log"

    entries = skills.select(a["repos"], a["needs"], a["skills_exclude"])
    values = build_values(a, entries, today)

    owned: dict[str, list[str]] = {}
    for kind in a["repos"]:
        out = ws / repo_name(a["project"], kind)
        owned[out.name] = render_repo(kind, out, values)
        print(f"rendered  {out.name}")

    ops = ws / repo_name(a["project"], "ops")
    schema = (ops / "docs/schema/types.ts").read_bytes()
    for kind in a["repos"]:
        if kind in SCHEMA_COPY:
            dst = ws / repo_name(a["project"], kind) / SCHEMA_COPY[kind]
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(schema)
            owned[repo_name(a["project"], kind)].append(SCHEMA_COPY[kind])

    harness = install_harness(ops, entries, values)
    for line in harness:
        print(f"installed {line}")
    # Harness files are skeleton-owned too: upstream.py must see a change to
    # the hook or the security guidance. Install log lines carry a space.
    owned[ops.name] += [h for h in harness if " " not in h]

    manifest = {
        "mainbrain_commit": mainbrain_commit(),
        "spawned_on": today,
        "answers": a,
        "skills": [e["name"] for e in entries],
        "skeleton_owned": owned,
    }
    (ops / ".mainbrain").mkdir(exist_ok=True)
    (ops / ".mainbrain/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (ops / ".mainbrain/answers.json").write_text(json.dumps(a, indent=2) + "\n", encoding="utf-8")

    write_handoff(ws, a, values, entries)
    write_push_script(ws, a)
    print("written   HANDOFF.md, push-all.sh")

    failed = 0
    if not args.no_install:
        print("installing dependencies and running every check (see spawn.log) ...")
        for repo, check, ok in install_and_check(ws, a, log):
            print(f"  {'ok  ' if ok else 'FAIL'}  {repo:<24} {check}")
            failed += 0 if ok else 1

    if not args.no_git:
        git_init(ws, a, log)
        print("committed first commit on main in every repo")

    print()
    print(f"workspace: {ws}")
    if failed:
        print(f"{failed} check(s) failed; read {log}. Fix before pushing.")
        return 1
    print("Every check a session can run is green. What remains is HANDOFF.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
