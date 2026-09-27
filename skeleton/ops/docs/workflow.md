# Workflow

The founder owns the product and tests it. Claude is the CTO. The founder
validates on staging and does not read code, so every check a reviewer
would have done is a machine's job, and one human decision remains: go
prod.

## A feature, start to finish

1. **Spec.** The founder hands over a mockup and a description of what the
   feature does for the user. A link to the design project or an exported
   page both work.
2. **Questions.** Before any code, the session asks what would change the
   build and nothing else, in one batch. A spec with no open question gets
   no questions.
3. **Proto on staging.** The first deliverable is something the founder can
   click. It may be plain on the surface. It is prod-grade on four things
   from the first commit, because those are the costliest to redo: the data
   model, the security rules, the secrets, the invariants that state a
   promise.
4. **Journal.** When the staging deploy is green, the session writes an
   acceptance journal from `docs/acceptance/TEMPLATE.md` into
   `docs/acceptance/<date>-<feature>.md`: what to check, step by step in
   product terms, and the crash scenarios to provoke on purpose. Every
   crash family in the template gets an answer.
5. **Test.** The founder walks the journal on staging and fills the Results
   column. What is `ko` and blocks goes back to the session; what is `ko`
   and does not block goes to `docs/bugs.md`. No code is discussed.
6. **Go prod.** The founder says go on a journal with every line filled.
   Claude promotes the staging commit to prod and says what shipped. A
   release with an unfilled journal does not go to prod.

## Environments

Two. A third, preprod, arrives the day a paying customer has something to
lose.

| | staging | prod |
|---|---|---|
| Git | `main` | `prod`, fast-forwarded from `main` on go |
| Back end project | `{{FIREBASE_STAGING}}` | `{{FIREBASE_PROD}}` |
| Front ends | `main` preview | `prod` production |
| Third-party accounts | test mode | live mode |

Project ids, numbers and hostnames are recorded in each repo's config and
in `docs/environments.md` once they exist. They are not guessed.

`prod` only ever moves forward to a commit that was on `main` and was
tested on staging. Nothing is committed to `prod` directly:

```bash
git fetch origin main
git push origin origin/main:prod
```

## Branches and merges

Features land on a branch and go through a pull request, because the pull
request is where the gates run. When the gates are green Claude merges it.
The founder is never asked to merge, approve, or read a diff.

The gates, in order, all automated:

- typecheck and tests, in CI
- the schema check against `{{PROJECT}}-ops`, in CI
- the design-token check, in CI for site and app
- a security review, run by Claude on every pull request that touches the
  functions repo or its security rules
- a simplification pass, run by Claude before merge
- an animation review, run by Claude with `review-animations` on every
  site or app pull request that touches motion, when that skill is
  installed; Block is red

A gate that is red blocks the merge. There is no override.

The founder's standing authorization: "When I ask for work, you have
everything you need to work safely. You open the PRs, you merge, you
deliver. I only validate staging to prod." It covers every repo, ops
included, and every kind of change: code, docs, skills, memory. A repo
without CI has no gate to wait on; Claude runs the checks it can locally
and merges. Delivery means the change is on `main`, not on a branch
waiting for a click. A session that stops to ask "shall I open the PR?" or
"shall I merge?" has broken the agreement. The one question Claude asks
the founder is go prod.

## Human actions

Some steps cannot be done by a session: creating a repository on a
personal GitHub account, creating a cloud project, pasting a secret,
pointing DNS. `HANDOFF.md` at the workspace root lists them, step by step,
each with the check that proves it was done. A session that hits one names
the step by its number and waits. It never invents a value, never skips
the check, and never writes a secret anywhere but where the step says.

## Structural changes go up to mainBrain

This project was spawned from mainBrain, which spawns the next one. A
change to how the repos work (a workflow, a script, a harness file, a
skill addendum, a convention) ships twice in the same session: here and in
mainBrain. `python3 mainBrain/scripts/upstream.py <ops repo>` lists what
is owed in both directions. Details in `CLAUDE.md`, "Upstream to
mainBrain".

## Session discipline

One goal per session, named in the first message and repeated at the end.

Anything found along the way that does not block that goal goes in
`docs/bugs.md` as one line and stays there. A bug that does block it gets
fixed, and the fix is part of the session's goal.

A session ends with three lines: what shipped, what is on staging with its
journal, what is blocked and on whom.

## The bar for code

- **Clear.** A reader who did not write it can follow it. Names say what a
  thing is; no abbreviation the schema does not use.
- **Documented.** Comments say why a constraint exists. What a line does is
  the line's job.
- **Simple.** No abstraction before its second use. No option nobody asked
  for. No framework for a problem a function solves.
- **Stable.** Every feature has a happy-path test and logs its errors.
  Every webhook is idempotent under a retry. Every timestamp is epoch ms.
- **Bounded.** No loop over data without a bound written in the code and
  held in a constant a test can assert; no retry without a cap; no
  database trigger without a recorded decision and a re-entry guard. On a
  serverless runtime a loop that never ends is a bill.
- **Scalable.** Functions hold no state between calls. Reads are indexed
  before they ship. Nothing fans out per request.
- **Secure.** Rules deny by default. Every inbound webhook validates its
  signature before doing anything. Input is validated at the edge and
  trusted after. Secrets live in Secret Manager and nowhere else.

## What the founder supplies

Cloud project ids, third-party accounts and keys, DNS. A secret goes
straight into Secret Manager or a GitHub secret, never into the chat. A
session that needs one names it and waits.
