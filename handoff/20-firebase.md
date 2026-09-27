## F — Firebase and Google Cloud

Two projects, `{{FIREBASE_STAGING}}` and `{{FIREBASE_PROD}}`. Everything is
done twice, once per project, unless a step says otherwise.

### F1 — Create the projects

Where: https://console.firebase.google.com/ → Add project.

Project id must be exactly `{{FIREBASE_STAGING}}`, then `{{FIREBASE_PROD}}`;
the deploy workflow refuses a credential whose project id is not the
target, and the ids are written into the repos. Google Analytics: off for
both (a dashboard is not a place for a tracker).

Then in each project: Build → Firestore Database → Create database →
**Native mode**, location `{{REGION}}`, start in **production mode** (the
repo's rules replace the defaults on first deploy).

Proof: both projects open at
https://console.firebase.google.com/project/{{FIREBASE_STAGING}} and
https://console.firebase.google.com/project/{{FIREBASE_PROD}}.

### F2 — Billing and the budget alert

Where: each project → Settings (gear) → Usage and billing → Modify plan →
**Blaze**. Cloud Functions v2 does not deploy on Spark. Blaze is per
project; a card on the account is not enough.

Then, once per project, the last safety net against a runaway loop:
https://console.cloud.google.com/billing → Budgets & alerts → Create
budget. Scope: the project. Amount: what you would notice, $10 for
staging, $50 for prod at the start. Thresholds 50%, 90%, 100%, email to
you.

Proof: "Plan: Blaze" on the usage page, and one budget listed per project.

### F3 — Enable two APIs

Where, once per project (replace the project in the URL):

- https://console.developers.google.com/apis/api/secretmanager.googleapis.com/overview?project={{FIREBASE_STAGING}}
- https://console.developers.google.com/apis/api/cloudbilling.googleapis.com/overview?project={{FIREBASE_STAGING}}

and the same with `project={{FIREBASE_PROD}}`. `firebase-tools` enables
every other API it needs; these two it does not, and the first deploy
stops on them with a link back here.

Proof: each page shows "API enabled".

### F4 — The deploy credential

Where: https://console.cloud.google.com/iam-admin/serviceaccounts, per
project.

1. Create service account `github-deploy`.
2. Grant it four roles on the project. Editor alone cannot make an HTTPS
   function callable from outside, which is why the last two exist:
   - **Editor**: create functions, rules, Cloud Run services, enable APIs
   - **Secret Manager Admin**: let a deployed function read its secrets
   - **Cloud Functions Admin**: `setIamPolicy` on the function, so a third
     party can call it without a Google identity
   - **Cloud Run Admin**: the same grant on the Cloud Run service behind
     each v2 function
3. Keys → Add key → JSON. Download once.
4. In `{{OWNER}}/{{PROJECT}}-functions` → Settings → Secrets and variables →
   Actions → New repository secret. Name `FIREBASE_SERVICE_ACCOUNT_STAGING`
   for the staging key, `FIREBASE_SERVICE_ACCOUNT_PROD` for the prod key.
   Value: the whole JSON file, as is.
5. Delete the downloaded files.

Proof: the `Deploy` workflow in `{{PROJECT}}-functions` is green on `main`,
ending with "all exported functions are deployed on staging". A first
deploy on a fresh project can lose one function to a bucket-creation race;
the verify step says to re-run, and the second run passes. Prod deploys
the first time `main` is promoted.
