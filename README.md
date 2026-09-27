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

Read `CLAUDE.md` for the model, `docs/repo-creation.md` to let a session
create the repositories itself, `docs/questionnaire.md` for the questions,
`docs/upstream.md` for how improvements in a project come back here.

This repo is public and holds nothing private: no customer, no account, no
project id, no secret. Spawned projects live elsewhere.
