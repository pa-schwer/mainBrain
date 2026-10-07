# Adopting a repo that predates the spawn

A project sometimes starts before mainBrain does: a site already live, an
app with a history. The stack still gets generated around it, and that
repo joins as an adopted one. The generator renders it like any other, so
the structure is on disk to copy from. Nothing overwrites the repo: the
skeleton reaches it through one pull request, and its product files stay
its own.

## In the answers

```json
"repo_names": { "site": "existing-repo-name" },
"adopted": ["site"]
```

`repo_names` keeps the repo's real name when it does not follow
`<project>-<kind>`. `adopted` lists the kinds whose repo already has a
history. `ops` cannot be adopted; the generator refuses it.

Spawn into a parent directory that does not already hold a clone named
after the project: the workspace is `<out>/<project>`, and `--force`
replaces whatever is there.

## What changes in the run

- The "Create repositories" workflow takes the full list, as for any
  spawn. It reports the adopted repo as `exists` and moves on.
- `push-all.sh` skips the adopted repo and says so. A push of the
  generated `main` would be rejected, and recreating the remote to make it
  pass would destroy the history.
- The manifest records `adopted` with the rest of the answers.

## The pull request in the adopted repo

On a branch of the existing repo, with the generated copy next to it:

1. **Take the structure.** The CI workflow, `scripts/`, the schema copy,
   `public/_headers` and `robots.txt`, `CLAUDE.md` and `LAUNCH.md`. Adapt
   only what is false for this repo: its Worker name, its canonical host,
   its languages, its launch switch.
2. **Keep the product.** Pages, layouts, `astro.config.mjs` or
   `vite.config.ts`, `wrangler.jsonc`, the README. `package.json` keeps its
   name and dependencies and gains the scripts CI calls (`typecheck`,
   `test`) and their dev dependencies.
3. **Bring its tokens home.** The token check fails on every color and
   font stack outside `src/styles/tokens.css`. Move them there, write
   them as tables in `<project>-ops/docs/design-system.md`, and express a
   shade as the same token at a lower opacity. Keep the font stacks
   exactly as the repo rendered them: a different fallback changes every
   glyph the main font lacks.
4. **Give `npm test` a real subject.** A test of the repo's own logic
   (URL building, i18n paths), not the skeleton's sample.
5. **Prove nothing moved.** Build before and after, screenshot the same
   pages with the Chromium at `/opt/pw-browsers`, and compare the files.
   A page that loads remote images renders in more than one state: every
   after shot must be identical to some before shot.

The schema job stays red until `OPS_READ_TOKEN` is set (HANDOFF G4), as in
every product repo of the stack. Every other check is green before merge.

## In the ops repo

A second commit on `main`, before or after the push:

- `.mainbrain/manifest.json`: `skeleton_owned` for the adopted repo lists
  only the files step 1 took. `upstream.py` then compares what the
  skeleton owns and leaves the product's files alone.
- `docs/decisions.md`: one line naming the adopted repo, what it took and
  what stayed its own.
- `docs/design-system.md`: filled from step 3.

## HANDOFF

Steps the adopted repo already did, such as a Cloudflare import or a
custom domain, are checked against what exists, never redone. Its Worker
keeps its name even when HANDOFF names it after the repo.
