# Upstream: how a project's advances come back

mainBrain spawns projects, and projects improve on what they were given. A
workflow gets a verify step, a hook learns a new warning, a skill gets an
addendum, a CLAUDE.md gains a rule that saved an afternoon. Left in the
project, each of those is lost to the next one. So the flow has a return
path, and it is a rule, not a habit.

## The rule, as every spawned ops repo states it

A structural change lands in two pull requests in the same session: one in
the project, one in mainBrain. Both are opened and merged by the session
on green. The project's `decisions.md` line for the change names the
mainBrain commit. A structural change with no mainBrain pull request is
not delivered.

Structural means: a file the skeleton owns. `<project>-ops/.mainbrain/manifest.json`
lists them per repo, as the generator wrote them. Feature code, product
copy, the schema's types and `docs/product.md` are not structural.

## The tools

`scripts/upstream.py <ops repo>` re-renders the skeleton with the
project's own answers and diffs the result against the live repos next to
ops. It prints two lists:

- **changed in the project since spawn**: candidates to bring here;
- **changed in mainBrain since spawn**: candidates to push down there,
  computed by rendering at the commit the manifest recorded.

`--patch` writes each project-side change as a unified diff against the
skeleton template, with the project's values turned back into
placeholders, under `<ops>/.mainbrain/upstream/`. Read each patch, drop
the hunks that are product-specific, and `git apply --3way` the rest in
mainBrain.

`scripts/check-drift.sh <ops repo>` does the same for the library side:
installed skills, the agent, the command, the hook and the patterns. A
skill the project has that the library lacks is listed as a candidate.

## The direction

mainBrain wins on the generic; the project wins on the specific. When a
patch mixes both, the generic part comes here and the specific part is
rewritten in the project so that the reverse render leaves it out. A
change that only one product could want is not a mainBrain change, and
saying so in the project's `decisions.md` is enough.

## Pulling down

A project that wants a mainBrain improvement runs the same tools in the
other direction: `upstream.py` names the file, the session applies the
skeleton's version by hand or with `skills.py install --only <name>` for
a library entry, and the project's manifest is updated to the new
mainBrain commit in that pull request. Nothing forces a project to take
every update; the manifest records where it stands.
