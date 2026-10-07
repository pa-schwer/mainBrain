# Bugs

Findings that did not block the session that found them. One line each,
newest last. A line leaves this file in the commit that fixes it.

Format: `YYYY-MM-DD — area — what is wrong — found while`

---
2026-10-07 — provisioning — an organization created on or after 2024-05-03 enforces `iam.disableServiceAccountKeyCreation` and `iam.allowedPolicyMemberDomains` by default, so step 6 of `provision-firebase.sh` cannot create the deploy key, and a public HTTPS function cannot get its `allUsers` invoker grant; `docs/gcp-provisioning.md` creates exactly such an organization and says nothing about either — found while weighing a Firebase credential for sessions
