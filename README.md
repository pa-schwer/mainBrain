# mainBrain

A generator for a working software stack, and the library of skills that
runs it. Ask for a project; get a workspace with one repo per kind
(orchestrator, public site, back end, dashboard, pure library), dependencies
installed, every check green, the first commit made, and a `HANDOFF.md`
listing the few steps only a human can do, each with its proof.

```bash
bash scripts/check-library.sh
bash scripts/spawn.sh examples/answers.example.json --out /tmp/demo
cat /tmp/demo/acme/HANDOFF.md
```

## Repositories are created for you

A session cannot create a GitHub repository, so mainBrain does it from a
workflow: `.github/workflows/create-repos.yml` holds a token in this
repo's secrets and creates empty, private repos when a session asks. One
setup per GitHub account or organization, in `docs/repo-creation.md`.
The same pattern provisions Firebase: `docs/gcp-provisioning.md` arms
"Create Firebase projects", which does the Google Cloud side of the
handoff. Both workflows wait for your approval on every run. After that,
`spawn-project` goes from questionnaire to pushed repos and provisioned
projects with two clicks: Approve, Approve.

Read `CLAUDE.md` for the model, `docs/repo-creation.md` to let a session
create the repositories itself, `docs/questionnaire.md` for the questions,
`docs/upstream.md` for how improvements in a project come back here.

This repo is public and holds nothing private: no customer, no account, no
project id, no secret. Spawned projects live elsewhere.
