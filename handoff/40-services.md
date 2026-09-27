## S — Third-party services

One account or mode per environment. Keys go to Secret Manager (F6),
identifiers go to `{{PROJECT}}-ops/docs/environments.md`.

| Service | Staging | Prod | Secret name(s) | Where it is configured |
|---|---|---|---|---|
{{SERVICES_HANDOFF_TABLE}}

Proof: the first cycle that uses the service records its identifiers in
`docs/environments.md` and its deploy is green.
