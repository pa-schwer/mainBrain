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
# runs at container start, as root, before Claude Code launches
for d in {{REPO_DIRS}}; do
  [ -f "$d/package.json" ] && (cd "$d" && npm ci --silent)
done
{{PLAYWRIGHT_LINE}}
# plugins: a cloud session never installs the ones settings.json enables
{{PLUGIN_SETUP_LINES}}
```

Proof: a fresh session runs `npm test` in any repo without installing
first.

### E3 — Plugins

Nothing more once E2 is in. A cloud session does not install the plugins
a repository's `.claude/settings.json` enables, so E2 installs
{{PLUGIN_LIST}} at user scope and the environment cache keeps them.
`settings.json` still names them for a session on a local machine.

Proof: `claude plugin list` in a fresh session shows each one enabled.
