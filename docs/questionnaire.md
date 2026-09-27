# The questionnaire

What a session asks before spawning a project, and what each answer
changes. One batch of questions, then the generator runs. A question whose
answer would not change the build is not asked; the defaults below apply.

The answers land in a JSON file (`examples/answers.example.json` is a
filled one) and travel with the project in
`<project>-ops/.mainbrain/answers.json`.

## 1. Identity

| Key | Question | Rule | Changes |
|---|---|---|---|
| `project` | Short name, as a slug | lowercase, digits, dashes, 2-31 chars | every repo name, `<project>-ops` … |
| `title` | Name as it is written | free | titles, `<title>`, headings |
| `description` | One sentence: what it does, for whom | one line | `docs/product.md`, the scaffold page, package descriptions |
| `owner` | GitHub owner (user or organization) | must be able to hold private repos | remotes, CI owner resolution, `HANDOFF.md` |

A brand, voice or copy document the founder already has is not a
question: it goes verbatim into `<project>-ops/BRAND.md` after the spawn,
and the description is drawn from it.

## 2. Shape of the stack

`repos`: which kinds to create. `ops` is always created.

| Kind | Ask it as | Take it when |
|---|---|---|
| `site` | "Is there a public site: landing, pricing, legal pages?" | anything a stranger visits before signing up |
| `functions` | "Is there a back end: webhooks, scheduled jobs, a database, secrets?" | anything that decides, stores, or talks to a third party |
| `app` | "Is there a logged-in screen: a dashboard, settings, a workspace?" | a customer signs in and sees their own data |
| `lib` | "Is there an algorithm worth isolating: a scoring model, a parser, a matcher?" | logic that must be testable in milliseconds with no project id |

Combinations that make sense: `site` alone (a brochure), `site + functions`
(a form that posts), `functions + app` (a tool), all four (a SaaS), `lib`
with any of them. `app` without `functions` still uses Firebase for auth
and reads.

## 3. Names that end up in configuration

| Key | Default | Ask only if |
|---|---|---|
| `domain` | `<project>.example` | a domain exists or is decided |
| `app_domain` | `app.<domain>` | the dashboard lives elsewhere |
| `api_domain` | `api.<domain>` | the back end is fronted differently |
| `firebase_staging` | `<project>-staging` | the project id is already taken on Google |
| `firebase_prod` | `<project>-prod` | same |
| `region` | `us-central1` | the users are far from it, or a law says where data lives |
| `copy_language` | `US English` | the product is sold in another language |
| `html_lang` | `en` | same |

## 4. Skills: what the work will need

`needs`: a list of the keys below. Ask them as "will this project need
…". The defaults for the chosen repo kinds are installed without asking
(the prose, memory, self-improvement, discovery, security and
simplification directives, plus browser testing and UI guidance for any
front end); the list below is what is asked.

| Need | Ask it as | Installs |
|---|---|---|
| `motion` | "Will the site or app have animations, transitions, gestures worth getting right?" | animate + review-animations (a merge gate) |
| `marketing-copy` | "Will a session write the words that sell it?" | copywriting |
| `conversion` | "Is there a page or form to optimize once it has traffic?" | cro |
| `signup` | "Is there a self-serve account creation flow?" | signup |
| `activation` | "Is there a path from paid to first value that must not leak?" | onboarding |
| `experiments` | "Will changes be A/B tested?" | ab-testing |
| `skill-authoring` | "Will this project write skills of its own?" | skill-creator |

`skills_exclude`: names to leave out even if a default would install them.
Rarely needed; every exclusion is a line in the project's `decisions.md`.

When a need has no entry in the library, the answer is `find-skills` in
the spawned project, and a new library entry here when the skill proves
itself.

## 5. Secrets and services

`secrets`: every secret the product will read, by exact name, with the
service and the repo that reads it. Names only; a value never enters the
chat. Each one becomes a row in `HANDOFF.md` step F6 and in
`docs/environments.md`.

```json
{ "name": "STRIPE_SECRET", "service": "Stripe", "used_by": "functions", "needed_from": "the billing cycle" }
```

`services`: every third-party account, with its staging and prod modes
and where it is configured. Each one becomes a row in `HANDOFF.md` group S.

```json
{ "name": "Stripe", "staging": "test mode", "prod": "live mode", "secrets": ["STRIPE_SECRET"], "where": "dashboard.stripe.com → Developers" }
```

A product that has not chosen its services yet leaves both lists empty;
the first cycle that needs one adds the rows and names the HANDOFF step.
