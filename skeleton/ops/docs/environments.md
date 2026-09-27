# Environments

Two, per `workflow.md`. Everything on this page is an identifier or a
setting. Nothing on it is a secret, and nothing that is a secret belongs on
it: those live in Secret Manager and in GitHub repository secrets, and this
page says only what they are called.

The steps that create what is listed here are in `../HANDOFF.md`.

## GitHub

Owner: `{{OWNER}}`. Repos: {{REPO_LIST}}.

| Repo | Secret | Holds |
|---|---|---|
{{GITHUB_SECRETS_TABLE}}

{{FIREBASE_SECTION}}

{{CLOUDFLARE_SECTION}}

## Third-party services

| Service | Staging | Prod | Secret |
|---|---|---|---|
{{SERVICES_TABLE}}
