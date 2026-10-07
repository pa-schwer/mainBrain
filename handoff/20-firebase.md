## F — Firebase and Google Cloud

Two projects, `{{FIREBASE_STAGING}}` and `{{FIREBASE_PROD}}`. Everything is
done twice, once per project, unless a step says otherwise.

**Automatic path (default).** When mainBrain's "Create Firebase projects"
workflow is armed for your Google Cloud organization
(`mainBrain/docs/gcp-provisioning.md`, once, about thirty minutes), F1 to
F5 are one run: the session triggers it with the slug, the region and the
two repo names; you approve the run in mainBrain's Actions (it waits for
your click, and nothing is created before it); the workflow creates both
projects in the `mainbrain-projects` folder, links Blaze, sets a budget
with alerts, enables the APIs, adds Firebase, Firestore Native,
Email/Password sign-in and the default Storage bucket, creates the deploy
account with its four roles, lets `{{PROJECT}}-functions` act as it
through Workload Identity Federation with no key, sets
`GCP_WIF_PROVIDER_STAGING` and `_PROD` on that repo, creates the web app
and commits its public config into `{{PROJECT}}-app`. Proof: the `Deploy` workflow of
`{{PROJECT}}-functions` is green on the next push. Read F1 to F5 below as
what the run did, and as the manual path if it is not armed.

**After provisioning, nothing in Firebase is configured by hand.**
Sign-in providers, Firestore rules and indexes, and Storage rules live in
`{{PROJECT}}-functions/firebase.json` and the files it names. A session
edits them, and the `Deploy` workflow applies them: to staging on every
push to `main`, to prod at promotion. A Firestore collection needs no
creation step: it exists from its first document, behind the rules.

**Manual path.** Each step below, by hand.

### F1 — Create the projects

Where: https://console.firebase.google.com/ → Add project.

Project id must be exactly `{{FIREBASE_STAGING}}`, then `{{FIREBASE_PROD}}`;
the deploy workflow refuses a credential whose project id is not the
target, and the ids are written into the repos. Google Analytics: off for
both (a dashboard is not a place for a tracker).

Then in each project: Build → Firestore Database → Create database →
**Native mode**, location `{{REGION}}`, start in **production mode** (the
repo's rules replace the defaults on first deploy).

Then Build → Storage → Get started, location `{{REGION}}`, production
mode. The deploy stops on Storage until the bucket exists.

Proof: both projects open at
https://console.firebase.google.com/project/{{FIREBASE_STAGING}} and
https://console.firebase.google.com/project/{{FIREBASE_PROD}}, and each
shows a bucket under Storage.

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

### F4 — The deploy identity

No key. The functions repo's `Deploy` workflow proves who it is with a
GitHub OIDC token, and each project trusts that token on one branch.

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
3. In Cloud Shell, once with the first line as is, once with
   `PROJECT_ID={{FIREBASE_PROD}}; BRANCH=prod`:

   ```bash
   PROJECT_ID={{FIREBASE_STAGING}}; BRANCH=main
   REPO={{OWNER}}/{{PROJECT}}-functions
   NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
   gcloud services enable iamcredentials.googleapis.com sts.googleapis.com --project="$PROJECT_ID"
   gcloud iam workload-identity-pools create github --location=global --project="$PROJECT_ID"
   gcloud iam workload-identity-pools providers create-oidc github \
     --workload-identity-pool=github --location=global --project="$PROJECT_ID" \
     --issuer-uri="https://token.actions.githubusercontent.com" \
     --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
     --attribute-condition="assertion.repository == '$REPO' && assertion.ref == 'refs/heads/$BRANCH'"
   gcloud iam service-accounts add-iam-policy-binding "github-deploy@$PROJECT_ID.iam.gserviceaccount.com" \
     --project="$PROJECT_ID" --role=roles/iam.workloadIdentityUser \
     --member="principalSet://iam.googleapis.com/projects/$NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/$REPO"
   echo "projects/$NUMBER/locations/global/workloadIdentityPools/github/providers/github"
   ```

4. In `{{OWNER}}/{{PROJECT}}-functions` → Settings → Secrets and variables →
   Actions → Variables → New repository variable: `GCP_WIF_PROVIDER_STAGING`
   holds the last line printed for staging, `GCP_WIF_PROVIDER_PROD` the one
   for prod.

In an organization created since May 2024, a public HTTPS function also
needs the folder exceptions in `mainBrain/docs/gcp-provisioning.md`,
step 2.

Proof: the `Deploy` workflow in `{{PROJECT}}-functions` is green on `main`,
ending with "all exported functions are deployed on staging". A first
deploy on a fresh project can lose one function to a bucket-creation race;
the verify step says to re-run, and the second run passes. Prod deploys
the first time `main` is promoted.
