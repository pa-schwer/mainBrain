# Core Memory

Summaries and pointers. Detail lives in `topics/`.

## Project shape

`{{PROJECT}}-ops` is this repo: orchestrator, guardian of the schema, never
product code. Sibling repos hold the product: {{REPO_LIST}}. The rule that
matters: `docs/schema/types.ts` is the only editable copy of any data type,
and `scripts/check-schema.sh` enforces it.
→ CLAUDE.md

## Origin, and the way back

Spawned from mainBrain on {{DATE}}. The stack, the workflow and the skills
come from there. A structural change made here ships in a mainBrain pull
request too, in the same session; `upstream.py` lists what is owed.
→ CLAUDE.md "Upstream to mainBrain", .mainbrain/manifest.json

## Human actions

`../HANDOFF.md` lists what a human still has to do. A session that needs
one of those steps names it and waits.
→ HANDOFF.md
