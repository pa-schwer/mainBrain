### F6 — Secrets

Where: each project → https://console.cloud.google.com/security/secret-manager
→ Create secret. Exact name, value pasted there and nowhere else.

| Name | Service | Read by | Staging value | Prod value |
|---|---|---|---|---|
{{SECRETS_TABLE}}

A secret is created here **before** the cycle that declares it in
`src/config.ts` deploys; a declared secret that does not exist blocks
every deploy. The scaffold declares none, so nothing is needed for the
first deploy. The session that first reads a secret will name this step.

Proof: the secret is listed in both projects, and the deploy that
declares it is green.
