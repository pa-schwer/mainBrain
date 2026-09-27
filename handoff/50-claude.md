## E — Claude Code environment

### E1 — Attach the repositories

Where: the Claude Code web app → the environment you use → repositories,
or in a session: `add_repo` for each of {{REPO_LIST}}.

G2 has to be done first; without the app install the attach is refused.

Proof: a session lists the repos in its scope and can push to each.

### E2 — Environment setup script

Where: the environment's settings → setup script. The container is rebuilt
every session, so anything not committed has to be reinstalled here.

```bash
# runs at container start
for d in {{REPO_DIRS}}; do
  [ -f "$d/package.json" ] && (cd "$d" && npm ci --silent)
done
{{PLAYWRIGHT_LINE}}
```

Proof: a fresh session runs `npm test` in any repo without installing
first.

### E3 — Plugins

Nothing to do. `{{PROJECT}}-ops/.claude/settings.json` enables
{{PLUGIN_LIST}} from their marketplaces; Claude Code installs them on the
first session that opens the repo.

Proof: the first session in `{{PROJECT}}-ops` reports the plugins loaded.
