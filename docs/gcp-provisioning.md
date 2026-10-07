# Letting mainBrain create Firebase projects

Out of the box a session cannot create a Google Cloud project, link it to
billing, or let a repository deploy to it. `HANDOFF.md` F1 to F5 ask a
human for each. This page moves those five steps to the
"Create Firebase projects" workflow of this repo: the session triggers
it, a human approves the run, and the workflow provisions staging and
prod with an identity that only this repository can assume.

One setup, about thirty minutes, once per Google Cloud organization. Every
step below is a Cloud Shell command or a console click, in order, with
its proof.

## What it protects

- **No key in GitHub.** The workflow authenticates through Workload
  Identity Federation: GitHub mints a short-lived OIDC token for the run,
  Google trusts it for one service account, from one repository. Nothing
  to rotate, nothing to leak. The projects it creates trust their
  functions repo the same way, one branch each, so no deploy holds a key
  either.
- **One folder, one billing account.** The identity can create projects in
  the `mainbrain-projects` folder and link them to one billing account.
  It cannot touch a project outside the folder.
- **A human approves every run.** Both provisioning workflows run in the
  `provisioning` environment, which requires a reviewer. The session
  triggers, the founder clicks Approve, then it runs. Creating a project
  and linking billing is the one act here that can create a bill, so it
  never happens without that click.
- **Budgets first.** The first thing the script does on a new project,
  after linking billing, is a budget with alerts at 50, 90 and 100 %.

## 0. An organization

The right to create projects (`roles/resourcemanager.projectCreator`) is
granted at organization or folder level only. A personal Google account
with no organization cannot delegate it to anyone. So:

- Have a domain you own (the product's domain works).
- Create a Google Cloud organization with **Cloud Identity Free**:
  https://cloud.google.com/identity/docs/set-up-cloud-identity-admin
  → sign up, verify the domain with the DNS record it gives you. Free,
  no Workspace needed.
- Sign in to https://console.cloud.google.com with the new admin account;
  the organization appears in the project picker.

Proof: `gcloud organizations list` in Cloud Shell shows one line. Note
its `ID`; the steps below call it `ORG_ID`.

Projects that already exist under your personal account can be migrated
into the organization later (IAM & Admin → Settings → Migrate); it is not
required for new projects.

## 1. A billing account

Where: https://console.cloud.google.com/billing → Create account, with
the card. Note its id, `XXXXXX-XXXXXX-XXXXXX`; the steps below call it
`BILLING_ACCOUNT`.

Proof: `gcloud billing accounts list` shows it, `OPEN: True`.

## 2. The folder, the identity, the rights

In Cloud Shell (https://shell.cloud.google.com), signed in as the
organization admin. Replace the three placeholders.

```bash
ORG_ID=<from step 0>
BILLING_ACCOUNT=<from step 1>
GITHUB_REPO=<owner>/mainBrain          # the repository that may assume the identity

# A folder that holds every project mainBrain creates, and nothing else.
gcloud resource-manager folders create --display-name=mainbrain-projects --organization="$ORG_ID"
FOLDER_ID=$(gcloud resource-manager folders list --organization="$ORG_ID" \
  --filter='displayName=mainbrain-projects' --format='value(name)' | sed 's|folders/||')

# A home project for the identity itself (it has to live somewhere).
gcloud projects create mainbrain-admin --folder="$FOLDER_ID" --name="mainBrain admin"
gcloud config set project mainbrain-admin
gcloud services enable iam.googleapis.com iamcredentials.googleapis.com \
  cloudresourcemanager.googleapis.com sts.googleapis.com
ADMIN_NUMBER=$(gcloud projects describe mainbrain-admin --format='value(projectNumber)')

# The identity.
gcloud iam service-accounts create mainbrain-provisioner --display-name="mainBrain provisioner"
SA="mainbrain-provisioner@mainbrain-admin.iam.gserviceaccount.com"

# Its rights: create projects in the folder and own what it creates;
# link and budget on the billing account. Nothing at organization level.
for role in roles/resourcemanager.projectCreator roles/owner roles/serviceusage.serviceUsageAdmin; do
  gcloud resource-manager folders add-iam-policy-binding "$FOLDER_ID" \
    --member="serviceAccount:$SA" --role="$role"
done
for role in roles/billing.user roles/billing.costsManager; do
  gcloud billing accounts add-iam-policy-binding "$BILLING_ACCOUNT" \
    --member="serviceAccount:$SA" --role="$role"
done

# Workload Identity Federation: GitHub Actions of that one repository may
# act as the identity. No key exists.
gcloud iam workload-identity-pools create github --location=global --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc github \
  --location=global --workload-identity-pool=github --display-name="GitHub" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == '$GITHUB_REPO'"
gcloud iam service-accounts add-iam-policy-binding "$SA" \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$ADMIN_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/$GITHUB_REPO"

echo "GCP_WIF_PROVIDER=projects/$ADMIN_NUMBER/locations/global/workloadIdentityPools/github/providers/github"
echo "GCP_PROVISIONER_SA=$SA"
echo "GCP_FOLDER_ID=$FOLDER_ID"
```

Proof: the three `echo` lines print values; keep them for step 4.

### The folder's exceptions to the organization's defaults

An organization created on or after 3 May 2024 enforces Google's
secure-by-default policies. Three of them break this stack, so the
folder overrides those three, before the first run. The others stay,
the ban on service account keys included: nothing here uses a key.

| Constraint | What it breaks | Folder setting |
|---|---|---|
| `iam.allowedPolicyMemberDomains` | the `allUsers` invoker grant a public HTTPS function or a webhook needs | allow all |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | Editor on the default compute account, which Cloud Functions v2 builds and runs as | not enforced |
| `storage.uniformBucketLevelAccess` | Firebase's default Storage bucket, which an enforcing organization can refuse | not enforced |

In the same Cloud Shell, with `ORG_ID` and `FOLDER_ID` still set:

```bash
# Setting a policy takes the Organization Policy Administrator role,
# which the organization admin does not hold by default.
gcloud organizations add-iam-policy-binding "$ORG_ID" \
  --member="user:$(gcloud config get-value account)" \
  --role=roles/orgpolicy.policyAdmin --condition=None

cat > /tmp/policy.yaml <<EOF
name: folders/$FOLDER_ID/policies/iam.allowedPolicyMemberDomains
spec:
  rules:
  - allowAll: true
EOF
gcloud org-policies set-policy /tmp/policy.yaml

for c in iam.automaticIamGrantsForDefaultServiceAccounts storage.uniformBucketLevelAccess; do
  printf 'name: folders/%s/policies/%s\nspec:\n  rules:\n  - enforce: false\n' "$FOLDER_ID" "$c" > /tmp/policy.yaml
  gcloud org-policies set-policy /tmp/policy.yaml
done
```

Proof: `gcloud org-policies describe iam.allowedPolicyMemberDomains
--folder="$FOLDER_ID" --effective` shows `allowAll: true`, and the same
command on the other two shows `enforce: false`. An older organization
enforces none of the three, and the commands change nothing there.

## 3. The GitHub token, widened

The workflow writes two things into the project's repositories: the
deploy identity's two provider ids as Actions variables of the functions
repo, and the public Firebase web config as two files of the app repo.
The `REPO_ADMIN_TOKEN` from `docs/repo-creation.md` needs two more
permissions:

Where: https://github.com/settings/personal-access-tokens → the token →
Repository permissions:

- **Variables: Read and write**
- **Contents: Read and write**

Keep Administration: Read and write. Regenerate if GitHub asks, and paste
the new value into the `REPO_ADMIN_TOKEN` secret.

## 4. Variables and secrets on this repository

Where: this repository → Settings → Secrets and variables → Actions.

Variables (tab **Variables**, not secret: they identify, they do not
authenticate):

| Name | Value |
|---|---|
| `GCP_WIF_PROVIDER` | the `projects/…/providers/github` line from step 2 |
| `GCP_PROVISIONER_SA` | `mainbrain-provisioner@mainbrain-admin.iam.gserviceaccount.com` |
| `GCP_FOLDER_ID` | the folder number from step 2 |

Secret (tab **Secrets**):

| Name | Value |
|---|---|
| `GCP_BILLING_ACCOUNT` | `XXXXXX-XXXXXX-XXXXXX` |

## 5. Enable the APIs the provisioner itself calls

On `mainbrain-admin`, once, in Cloud Shell:

```bash
gcloud services enable cloudbilling.googleapis.com billingbudgets.googleapis.com \
  firebase.googleapis.com serviceusage.googleapis.com --project=mainbrain-admin
```

## 6. The approval gate

Where: this repository → Settings → Environments → New environment →
name `provisioning` → **Required reviewers** → add yourself → Save.

Both provisioning workflows declare `environment: provisioning`. From now
on a triggered run shows "Waiting for review" in Actions until you click
**Review deployments → Approve**. Nothing is created before that click.

Proof: Actions → "Create repositories" → Run workflow with
`repos: mainbrain-smoke-test`: the run waits; approve it; it runs.

## 7. Proof, end to end

Actions → "Create Firebase projects" → Run workflow:

- `project`: `mainbrain-smoke`
- `region`: your region
- `functions_repo`, `app_repo`: empty
- budgets: defaults

Approve the run. It should print, for `mainbrain-smoke-staging` and
`mainbrain-smoke-prod`, one `created` or `ok` line per step and end with
the two web configs. Then delete both projects
(https://console.cloud.google.com/cloud-resource-manager → select →
Delete; they are removed after 30 days and billed nothing meanwhile).

## How a session uses it

`spawn-project`, after the repositories exist and the first commit is
pushed: trigger "Create Firebase projects" with the slug, the region and
the two repo names from the answers file, tell the founder a run is
waiting for approval, and wait. When the run is green, the functions
repo's `Deploy` workflow goes green on its next push, and `HANDOFF.md`
F1 to F5 are done. What remains human is F6: the values of third-party
secrets.

## Reading a red run

Filled in as failures are met, the way `docs/repo-creation.md` was.

| The log says | It means | Fix |
|---|---|---|
| `GCP_WIF_PROVIDER is not set` (or another name) | step 4 not done | add the variable or secret |
| `Waiting for review` for a long time | nobody approved | Actions → the run → Review deployments |
| `permission 'resourcemanager.projects.create' denied` | the identity lacks projectCreator on the folder, or the folder id is wrong | re-run the folder bindings of step 2 |
| `The caller does not have permission` on `billing projects link` | `roles/billing.user` missing on the billing account | the billing bindings of step 2 |
| `Unable to acquire impersonated credentials` | the WIF binding names another repository, or the provider condition does not match | check `GITHUB_REPO` in step 2 matches this repository exactly |
