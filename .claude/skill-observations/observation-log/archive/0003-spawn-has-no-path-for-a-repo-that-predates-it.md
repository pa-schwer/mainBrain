---
id: 3
title: "spawn-project had no path for a repo that predates the spawn"
status: actioned
type: open-source
skill: [spawn-project]
proposes_skill: []
siblings_checked: "none — spawn-project has no sibling skill in this library"
area: "spawn-project steps 3 and 4.2: workspace location and push-all.sh"
date: 2026-10-07
session_context: "A project whose public site was live before the stack asked for the full stack around it, the site kept as is"
parked_until:
resolved: 2026-10-07
resolution: "Actioned in the same session: an `adopted` key in the answers, push-all.sh skips adopted repos and no longer advises recreating a remote with a history, docs/adoption.md holds the pull-request procedure, and the skill and questionnaire point at it."
reference:
---

**Issue:** The skill assumed every repo in the answers is new. With an
existing site repo, three things went wrong or nearly did. The default
workspace path `<parent>/<project>` collided with the clone of that repo,
named after the project. `push-all.sh` would have pushed the scaffold's
unrelated `main` to the live repo. Its failure message then said
"recreate it empty", which on that repo deletes the site's history. The
`repo_names` override existed for the name, but nothing covered the
history. Adopting the repo by hand also showed what the generator cannot
decide: which skeleton files the repo takes and which stay the product's,
and that the token check forces the brand into `tokens.css`.

**Suggested improvement:** Done here. An `adopted` list in the answers;
`push-all.sh` skips those repos; `docs/adoption.md` gives the pull
request, the visual proof and the manifest trim; the skill steps name it.

**Principle:** A generator that writes into a destination must ask whether
the destination already holds work before it writes, and a recovery
message must never prescribe a destructive step without first ruling out
that the target holds real history.
