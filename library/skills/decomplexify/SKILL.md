---
name: decomplexify
description: Strip an interface down to what its first use case needs, by Rémi Guyot's simplification method - one first use case per feature, five operations on every component of a screen (eliminate, hide, reduce, organise, standardise), the absence test for every doubt, and a removal named for every addition. Use when a spec is written, before a mockup reaches the founder, before a pull request that adds or changes something a user sees merges, and whenever someone says "simplifie", "décomplexifie", "épure", "allège", "c'est trop chargé", "trop complexe", "simplify", "declutter", "too busy", "too complex", "CORSE", "HORSE", "C.O.E.U.R.", "first use case" or "test d'absence".
---

# Decomplexify

The method belongs to Rémi Guyot, who ran interface design at PayPal and
product at BlaBlaCar, from his public talks and writing: the
simplification review he calls HORSE in English and CORSE in French
(Blend Web Mix, 2019), the C.O.E.U.R. card game, the First Use Case, the
absence test, fanatical focus, and *Discovery Discipline* (with Tristan
Charvillat, Thiga, 2023). The wording here, and the wiring into the
board, the mockups and the merge gates, are mainBrain's. No passage of
his is reproduced.

## The stance

Complexity is the ground the team works on. "Keep it simple" names a
wish and gives no method; a team that steers clear of hard problems
ships cluttered screens. Your job is to take the complexity in so the
user gets less of it.

Simplifying runs against instinct. Asked to improve something, people
add, and they overlook the option of taking away (Adams and colleagues,
*Nature*, 2021). Taste alone will not get you there, so this skill
gives the subtraction named operations and a record.

Ego adds too. A designer who wants the effort seen draws the problem's
complexity onto the screen. Good simplification hides its own work: if
you do it well, nobody sees what you removed.

The target is a toboggan product: so obvious in the user's day that
they forget they are using it. A tester who comments on the app instead
of the task has hit a snag.

## 1. Before anything is drawn: the first use case

At PayPal the question came as a provocation, "What the F.U.C.?", and
designers would not start until the answer was clear.

- Write it in one line: one user, one moment, one problem. "A shop
  owner, at closing time, sees whether today beat yesterday."
- One first use case per feature. A second use case makes a second
  feature, for later.
- Pitch the answer in 280 characters. If it does not fit, it lacks
  focus.
- Write the Not now list: everything wanted that the first use case
  does not need. Say "not now" instead of "no"; the decision holds for
  now and can be reopened with evidence.
- Keep three to five priorities. Everything else sits on the list to
  avoid, and nobody works on it in passing.
- Draw nothing while the first use case is open. If the card lacks it,
  ask the founder one question.

## 2. On every screen: the five operations

Guyot's simplification review. HORSE and CORSE spell the same five
operations; C.O.E.U.R. deals them as cards. The acronym orders the
letters for memory. Run Eliminate first, because a component that goes
needs no further decision.

1. **Inventory.** List every component of the screen, in every state:
   each heading, label, value, icon, button, link, badge, hint, divider,
   card and empty-state line. Count them.
2. **Verdict.** Ask of each component, against the first use case:
   - **Eliminate.** Does the first use case need it on this screen? If
     two components do the same job, one goes.
   - **Hide.** Needed, but not by most users, or not at this moment?
     Move it behind a tap, to the next step, to a detail view, or to the
     state where it matters.
   - **Reduce.** Needed, but louder than its role? Lower its weight,
     size or contrast, and cut its words.
   - **Organise.** Needed, but in the wrong place? Order the screen by
     the first use case: what the user came for first, one primary
     action, the rest after.
   - **Standardise.** Needed, but drawn unlike its siblings? One icon
     style, one button pattern, one date format, one word per concept.
   - **Keep.** It earns its place as it stands.
3. **Every scale.** Run the same test on a word, a sentence, a
   component, a section and a step of the flow. Take it out; if the flow
   breaks, put it back.
4. **One message.** When two parts of the screen say different things,
   choose the message you want and cut or demote the other.
5. **Record.** Write the verdicts down, with the count before and after.

```markdown
## Simplification review (decomplexify)

First use case: <one user, one moment, one problem>
Components: <before> → <after>

| Component | Verdict | Reason |
|---|---|---|
| Messaging link on each result | Hide | rarely used while comparing rides |
| "Per person" after the price | Hide | most bookings are for one seat |
| Alert sign-up | Organise | moved to the end of the list, where it matters |
| Icons | Standardise | one graphic style |
| Seats left | Eliminate | the room went to a proximity indicator |
```

The examples in that table are BlaBlaCar's search results, the screen
Guyot used to teach the method.

**The card game, with subagents.** For a redesign, or a screen the
founder calls too busy, run C.O.E.U.R. as five background subagents
launched in one message: same screen, same first use case, one
operation each. Each returns its proposals with a reason. You then
converge: drop any proposal that breaks the first use case or an
accessibility rule, and record the rest. With people in the room it is
the same game: five cards dealt, a pitch per card, a debate on
arguments.

## 3. When in doubt: the absence test

- If you cannot decide whether a component earns its place, take it out
  and test the screen without it.
- Never ask a user "is this useful?". People say yes to anything they
  can see. They rarely report a useless element, and they complain fast
  about a missing one they need.
- Evidence comes from behaviour: a usability test in which nobody
  notices the gap, or a metric that holds or rises. BlaBlaCar took
  reviews off its search results; testers did not notice, and
  conversion rose about 10%.
- Some tests lose. A loss puts the element back and keeps the evidence.
- In a mockup, an absence test is a pair of variants, `v1/` with the
  element and `v2/` without; the founder picks from the screenshots.
- A doubt leans toward removal. The element carries the burden of
  proof.

## 4. At merge: every addition names its removal

- A pull request that adds something visible to an existing screen says
  in its body what it removed, hid or reduced to make room, or why
  nothing could go. The BlaBlaCar redesign above cut the seat count and
  hid messaging, and that room went to a proximity indicator worth more
  to the user.
- Build a smaller product, never a half-finished one. Cut scope; keep
  quality.
- A feature on the Not now list does not land as a side effect.
- Reuse what users already know. Before inventing a pattern, find the
  golden nuggets, the answers a reference product already proved for
  this problem, and assemble them. Copy with a reason; copying a whole
  product without one fails.
- When a milestone is planned, propose one card that removes something.
  In 2017, BlaBlaCar's roadmap held more projects that removed things
  than projects that added them.

## What this skill leaves to others

- How a kept component looks (style, color, type, spacing) belongs to
  the static design source: `impeccable` in a project with mockups.
  This skill decides what stays and where it ranks. impeccable's
  `distill` starts here and styles what survives.
- The words that remain follow `BRAND.md`. This skill cuts words;
  `BRAND.md` chooses them.
- It hides, and never eliminates: what a user needs to decide (a price,
  a date, a consequence), an accessibility affordance (a label, focus,
  error text), a legal or compliance element, and a state the card
  names (empty, error, no permission).
- The domain stays as complex as it is. The interface absorbs that
  complexity, and a rule computed in the back end stays there.

## Where it runs in a mainBrain project

| Moment | Sections | Record |
|---|---|---|
| A spec is written (`write-spec`) | 1 | the first use case and the Not now line in the card's Description |
| A mockup is drawn in ops `design/` | 2 and 3, before `check.sh` and impeccable's `critique` | the review in the mockup's `NOTES.md` |
| A site or app pull request adds or changes what a user sees | 4, and 2 on each changed screen | the review in the pull request body |
| A tester comments on the screen instead of the task | 2 on that screen | a finding in the acceptance journal |

The skill lives in the ops repo. Site and app sessions read it by path:
`<ops>/.claude/skills/decomplexify/SKILL.md`.

**Verdict as a gate.** Pass: the first use case is written, every
component of each changed screen has a verdict with a reason, and every
addition names its removal or the reason nothing could go. Block: any of
those is missing, or something from the Not now list appears on the
screen.
