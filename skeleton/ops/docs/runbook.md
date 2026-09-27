# Runbook

Operational procedures. Each one assumes it is being read at 2am by someone
who did not write it.

## Deploy to staging

Push to `main`. The functions repo's `deploy.yml` runs the tests and
deploys functions and rules to `{{FIREBASE_STAGING}}`. Site and app deploy
from `main` as Cloudflare preview deployments.

Nothing else to do. If the job is red, the log names the missing secret,
the mismatched credential, or the IAM permission. `HANDOFF.md` has the
step for each.

## Promote to prod

Only after the founder has walked the release's acceptance journal in
`docs/acceptance/` on staging, filled every Result, and said go. No
journal, or a journal with empty lines, means no promotion.

```bash
git fetch origin main
git push origin origin/main:prod
```

A fast-forward, nothing else. If the push is rejected as non-fast-forward,
someone committed to `prod` directly; stop and find out who and why before
forcing anything. The push triggers the functions deploy on `prod` and the
Cloudflare production builds of site and app.

Rollback: push the previous `main` commit to `prod` the same way. It is a
fast-forward too, since `prod` never holds a commit `main` did not.

## Secret rotation

1. Create the new version in Secret Manager.
2. Redeploy functions. A running function holds the old version until it is
   replaced; rotation without a deploy changes nothing.
3. Verify with a real request against staging before touching prod.
4. Disable the old version. Do not destroy it the same day; a failed
   rotation needs something to roll back to.

Rotating a secret that signs inbound webhooks invalidates signature
validation the moment it takes effect. Rotate it in a quiet window and
watch the first inbound event.

## A third-party service is down

1. Check the service's status page before anything else.
2. Say what is lost and what is queued. Do not promise a backfill the
   service cannot replay.
3. Tell affected users. Someone who thinks the product is working while it
   is not will blame the product, correctly.
4. Log the window in `decisions.md` only if it changes the architecture.

## A promised budget is breached

Every promise with a number is a constant with a test. When the measured
value crosses it in prod:

1. Read the constant and the test; the comment says what the number costs.
2. Find the step that ate the budget. Acknowledge first, work after.
3. Fix on `main`, verify on staging, promote.
