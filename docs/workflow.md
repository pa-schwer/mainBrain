# Workflow in mainBrain

The same working agreement as every spawned project, with one difference:
there is no staging and no prod here. A change is delivered when it is on
`main` and the checks are green.

## A change, start to finish

1. **Name the goal** in the first message. One goal per session.
2. **Change** the skeleton, the library, the handoff or the scripts.
3. **Check**: `bash scripts/check-library.sh`, then a full spawn of
   `examples/answers.example.json` into a temporary directory, every
   check green in every generated repo.
4. **Record** the reason in `docs/decisions.md` if the skeleton or the
   stack changed.
5. **Pull request**, merged by Claude on green, without asking.

## Gates

- `check-library.sh`: catalog versus disk, placeholders versus `spawn.py`,
  JSON parses, shell and python compile.
- the example spawn, end to end, with installs, in CI.
- security-guidance on every edit, turn and commit: this repo is public,
  and its rules in `.claude/claude-security-guidance.md` say what may not
  appear here.

## Session discipline

One goal per session. Side findings go to `docs/bugs.md` as one line. A
session ends with what is on `main` and what is blocked.

## Public repository

Nothing here names a customer, a person, an account, a project id, a
domain that is not an example, or a secret. When an example is needed it
is `example-owner`, `acme`, `acme.example`. A spawned project is "a
project". The security guidance enforces the patterns; the reviewer
enforces the rest.
