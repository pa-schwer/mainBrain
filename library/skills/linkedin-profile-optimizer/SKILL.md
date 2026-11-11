---
name: linkedin-profile-optimizer
description: "Audit and rewrite a LinkedIn profile end-to-end for 2026: headline, About 7-step, Featured, banner, photo, Experience metrics, Skills, custom URL, recommendations. Triggers on \"review my profile\", \"rewrite my headline\", \"fix my About\", \"optimize banner\", \"profile audit\", \"LinkedIn bio\". Converts resume-style profiles to ones that convert 3-5x better. Not for writing feed content (use linkedin-post-writer)."
---

<!-- LOCAL CHANGE (mainBrain): this block is not upstream. Everything below
     the next rule is upstream and unmodified. Strip this block before
     updating from sergebulaev/linkedin-skills. -->

## Addendum: running this in a mainBrain project

Vendored from `sergebulaev/linkedin-skills` at commit `8f8bc4b`: this one
skill of the bundle's twelve, with its five references. The bundle's root
`SKILL.md`, its shared `references/`, and the Python that posts through
Publora or reads through Apify stay upstream; nothing here needs a key or
the network. This block is the only local change, and it overrides the
upstream text below where they conflict.

**Voice.** "Global voice rules: see root `SKILL.md`" points at a file that
is not here. `stop-slop`, standing in every ops repo, is the voice rule
for every line of a rewritten profile. Two upstream rules still apply on
top of it: capitalize personal, company and product names, and prefer a
number to an adjective.

**Numbers come from the person.** The references model headlines and
bullets with metrics ("40% more demos", "$2.4M ARR"). Those are shapes. A
rewrite carries a figure only when the person supplied it or it sits in
the profile they pasted. Where a bullet needs a metric nobody gave, write
the bullet with a marked blank and ask for the figure. Never estimate one.

**Benchmarks are upstream's, unverified.** The uplift figures below
(3.9x views, 3-5x conversion, 71% more interviews, 30% longer viewing
time) come from a vendor's research that upstream cites without a link.
Step 9 asks for an "expected uplift": report the before and after, and
quote a benchmark only as "upstream's figure, source not checked". Never
promise it to the person whose profile it is.

**Related skills.** `linkedin-post-writer` and `linkedin-content-planner`
are not installed. Posts, carousels and the content calendar belong to
`social` when the project has the `social` need. `linkedin-humanizer` is
`stop-slop` here. Outreach from the finished profile (limits, sequence,
messages) is `cold-email`, `references/linkedin-outreach.md`, under the
`outbound` need.

**Where the work lands.** One file per profile in `linkedin/profiles/` in
the ops repo: the pasted source, the scorecard, the rewrites, the open
questions. A profile is personal data: it stays in the project's private
repos and never reaches mainBrain, a card title, or a public page.

---

# LinkedIn Profile Optimizer

Audit the nine components of a LinkedIn profile (photo, banner, headline, About, Featured, Experience, Skills, custom URL, recommendations) against 2026 best practices, then rewrite each section that needs it. Optimized profiles get ~3.9x more views and convert visitors 3-5x better than default/resume-style profiles.

## When to use

- User asks for an audit and pastes their profile text (a bare URL is not readable, see Input)
- User wants to rewrite their headline, About section, or Featured section
- User is launching a content strategy and needs the profile to match
- Any of: "review my profile", "fix my headline", "optimize bio", "profile audit", "LinkedIn optimization"

## Input

**Paste the profile, do not just link it.** The read layer covers posts, comments and engagers; there is no profile actor, so a profile URL cannot be fetched, with an APIFY_TOKEN or without one. Open the profile, copy the sections, paste them in. Screenshots of the visual parts work too.

- Profile text: headline, About, Experience entries, Skills, custom URL
- The visual three (photo, banner, Featured): screenshots, or a sentence describing each
- Goal: **clients** / **job seeking** / **authority** — Featured and CTA vary by goal
- Optional: draft content to grade against the existing profile

If the user supplies only a URL, ask for the text before scoring anything. Never score a section you have not been shown, and never infer profile content from the URL slug.

## Output

A structured audit + rewrite in this shape:

1. **Scorecard** (9 sections, pass/fail/needs-work)
2. **Priority fixes** (ranked by impact)
3. **Before → After rewrites** for each failing section
4. **Expected uplift** (based on benchmark data)

## Steps

1. **Intake.** Collect profile state + goal. If only a URL arrived, ask for the pasted text first. Flag missing sections.
2. **Score each of 9 sections** against the checklist (see references/).
3. **Rewrite headline** using `[What You Do] | [Who You Help] [Achieve What Result]` — fit all 220 chars.
4. **Rebuild About** with 7-step structure; verify first **265-275 chars** hook before "see more".
5. **Curate Featured** (3 strong items) matched to the goal:
   - **Clients:** lead magnet + case study with results + calendar link
   - **Job seeking:** portfolio + best work samples + top-performing post
   - **Authority:** best content + media/podcast features + newsletter signup
6. **Rewrite Experience bullets** as `action verb + specific metric`. Add 5+ skills per role. Pin top 3 skills.
7. **Claim custom URL** (linkedin.com/in/firstnamelastname, not the `-123abc456` default).
8. **Draft recommendation requests** with specifics ("about [project/skill]") — don't send LinkedIn's generic template.
9. **Deliver before/after diff** + expected uplift (3.9x views, 3-5x conversion, 71% more likely to land interviews).

## Nine-component scorecard

| # | Section | Pass criteria (2026) |
|---|---------|----------------------|
| 1 | **Photo** | ≥400x400, face fills 60% of frame, <3 years old, natural light, slight smile |
| 2 | **Banner** | 1584x396, text in right 2/3, high contrast, includes value prop + CTA, tests well on mobile |
| 3 | **Headline** | Uses all 220 chars; format `[What You Do] | [Who You Help] [Result]` |
| 4 | **About** | 200-300 words, first-person, 7-step structure, hook in first 265-275 chars |
| 5 | **Featured** | 3 items, matched to goal, custom 1200x627 thumbnails |
| 6 | **Experience** | Every bullet = `action verb + metric`, 5+ skills per role, media attached |
| 7 | **Skills** | 50 listed, top 3 pinned, mirrors target job descriptions, ≥1 endorsement each |
| 8 | **Custom URL** | `linkedin.com/in/firstnamelastname` (not the default hash) |
| 9 | **Recommendations** | At least 3 recent, specific (not generic), from diverse contexts |

## Key benchmarks (from co.actor research)

- Optimized About sections: **3.9x more views**
- 5+ listed skills: **3x more connection requests**
- Comprehensive profile: **71% more likely to land interviews**
- Featured section content: **30% longer viewing time**
- Personal founder profile vs company page: **315% more engagement, 270% more conversions**

## Hard rules

Global voice rules: see root `SKILL.md` §Voice rules. Additional skill-specific rules:

- First person ("I help...") never third person ("Jane is a passionate...")
- Never "passionate thought leader" / "driven professional" / "results-oriented" (profile-specific AI vocab)
- Avoid wall-of-text. Use line breaks in About section
- 80% of users leave Featured empty. Filling it is a free edge

## Reference files

- `references/profile-headline-formulas.md` — 220-char formula + before/after examples
- `references/about-section-templates.md` — 7-step structure with character budgets
- `references/featured-section-playbook.md` — goal-matched content types
- `references/banner-photo-specs.md` — dimensions, composition, mobile test
- `references/experience-skills-rules.md` — bullet rewriting + skills strategy + custom URL + recommendations

## Related skills

- `linkedin-content-planner` — post pillars should echo the profile's headline/About thesis
- `linkedin-post-writer` — Featured section rotates quarterly; pin your flagship post
- `linkedin-humanizer` — scrub profile copy for the same AI tells we scrub from posts
