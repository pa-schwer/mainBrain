---
name: spawn-project
description: Create a new project workspace from the mainBrain skeleton and skills library. Use when the user asks to start, create, spawn, scaffold or bootstrap a new project, product, SaaS, site, app or back end, or says "nouveau projet", "crée un projet", "new project". Asks the questionnaire in one batch, writes the answers file, runs the generator, hands over the workspace and its HANDOFF.md.
---

# Spawn a project

You are turning a request for a new project into a ready workspace. The
generator does the work; your job is the questionnaire, the answers file,
and the handover. Read `docs/questionnaire.md` once before asking
anything.

## 1. Ask, once

Ask every question whose answer changes the build, in **one batch**, in
the user's language. Use the wording in `docs/questionnaire.md`, section by
section:

1. identity: slug, title, one-line description, GitHub owner;
2. shape: site, functions, app, lib, each as a yes/no with its "take it
   when" line;
3. names that end in config: only the ones the user is likely to know
   (a domain if it exists); state the defaults for the rest;
4. needs: the seven skill questions, as yes/no;
5. secrets and services: "which third-party services, and what secret
   names will the back end read?" with the reminder that a value never
   enters the chat.

If the user has already answered some of it in the request, do not ask
again. If the user says "just defaults", take the defaults and ask only
for the slug, the title, the description and the owner.

## 2. Write the answers file

Write `<parent>/<project>.answers.json` outside this repo (next to where
the workspace will go), in the shape of `examples/answers.example.json`.
Read the file back and show the user a five-line summary: repos, needs,
secrets, services, domain. Do not wait for confirmation unless something
was ambiguous; the founder's standing rule is to build.

If the founder hands over a brand, voice or copy document, draw the
one-line description from it, and after the generator runs, put the
document verbatim in `<project>-ops/BRAND.md` (it replaces the
placeholder) in a second commit on `main`, with `docs/product.md` filled
from it in English. Sessions in every repo read it there by path.

## 3. Run the generator

```bash
bash scripts/spawn.sh <parent>/<project>.answers.json --out <parent>
```

`<parent>` is the directory that holds this repo's clone, unless the user
named another. The generator installs dependencies, runs every check and
makes the first commit in each repo. Read its output. If a check fails,
read `<parent>/<project>/spawn.log`, fix the cause in the skeleton (a
skeleton bug, since the example spawn is green in CI) and re-run with
`--force`; then that fix is a mainBrain pull request too.

## 4. Create the repos and push

Ask nothing. In this order:

1. Trigger this repo's "Create repositories" workflow
   (`.github/workflows/create-repos.yml`) with `repos` set to the
   comma-separated repo names from the answers file, `owner` set to the
   answers file's `owner`, and `visibility` `private`. Wait for the run. Green means the repos exist, empty. Red
   with "REPO_ADMIN_TOKEN is not set" means the one-time setup in
   `docs/repo-creation.md` has not been done: say so in one line, point at
   it, and continue with step 2 in case the repos were created by hand.
2. Check with `add_repo` whether `<owner>/<ops repo>` is reachable. If it
   is, attach every repo and run `bash <parent>/<project>/push-all.sh`;
   open no pull request, the first commit on `main` is the scaffold. If it
   is not, say so and point at `HANDOFF.md` G1 and G2: without the
   workflow, the repos are created by hand, on a personal account or an
   organization.

## 4b. Provision Firebase, if the stack has functions or app

After the push, when the answers include `functions` or `app`: trigger
this repo's "Create Firebase projects" workflow
(`.github/workflows/create-firebase-projects.yml`) with `project` = the
slug, `region` = the answers' region, `functions_repo` and `app_repo` =
`<owner>/<repo>` from the answers (empty for a kind not in the stack), and
the two `firebase_*` ids if the answers override them. Tell the user, in
one line, that the run waits for their approval in mainBrain's Actions.
Do not wait in a loop: end the turn, and check the run when the user
says it is approved or when you are next asked. Green means `HANDOFF.md`
F1 to F5 are done. Red with a name "is not set" means
`docs/gcp-provisioning.md` was never done: say so, point at it, and leave
F1 to F5 to the manual path.

## 5. Hand over

Tell the user, in their language:

- where the workspace is and what it contains (one line per repo);
- that every check a session can run is green;
- what remains, as the list of HANDOFF.md steps by number and title, with
  the first one to do;
- that a session in the new ops repo picks up from `CLAUDE.md` there.

Then, in this repo, append one line to `.claude/memory/topics/spawns.md`:
the date, the kinds spawned and the needs chosen. No project name, no
owner, no domain: this repo is public.

## What not to do

- Do not spawn inside this repo. The workspace goes next to it.
- Do not invent a domain, an owner or a project id. Ask, or take the
  documented default and say so.
- Do not paste a secret value anywhere, and do not ask for one. Names
  only.
- Do not edit a generated repo by hand to fix a skeleton bug. Fix the
  skeleton, re-render.
