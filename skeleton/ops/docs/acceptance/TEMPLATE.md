# Acceptance journal — <feature>

One journal per release to staging. Claude writes it when the staging
deploy is green, before telling the founder to test. The founder fills the
Results column. A release with an unfilled journal does not go to prod.

Everything below is in product terms. No code, no file names, no stack
traces. If a check needs a tool the founder does not have, the check is
wrong, not the founder.

## Release

| | |
|---|---|
| Feature | <name, one line> |
| Commit on `main` | `<sha>` |
| Staging deploy | <link to the green run> |
| Written on | <date> |

## What you need

- <a login, a browser, a phone: the physical prerequisites>
- <where to look: the dashboard URL, the console page, the inbox>

## Checks

Happy path first, then the variations. Each check has steps a person can
follow and one observable expected result.

| # | Do this | Expect this | Result |
|---|---|---|---|
| 1 | <steps> | <what you see, with numbers where there are numbers> | |
| 2 | | | |

## Crash scenarios

What can go wrong, provoked on purpose. Every family below is answered:
either a scenario the founder can trigger on staging, or "not reproducible
on staging, covered by test <name> in CI", or "does not apply because
<reason>". A family with no answer is a gap in the release.

| Family | Scenario | Trigger it | Expect this | Result |
|---|---|---|---|---|
| External service down | | | | |
| Retry or redelivery of the same event | | | | |
| Malformed or unexpected input | | | | |
| Missing config or secret | | | | |
| Permission denied | | | | |
| Two events at the same time | | | | |
| Quota, rate limit, budget cap | | | | |
| Timeout against a promised budget | | | | |
| Data edge: unknown id, paused account, empty field | | | | |
| Runaway loop or repeated sends | | | | |

## Results

Filled by the founder. `ok`, `ko`, or `skip` with a word.

Anything `ko` goes to `docs/bugs.md` if it does not block the release, or
back to the session if it does.

## Verdict

- [ ] go prod
- [ ] not yet: <what blocks>
