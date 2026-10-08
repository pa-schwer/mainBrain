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
with no organization cannot delegate it to anyone, and a service account
cannot create a project without a parent. So the workflow needs an
organization, and an organization needs a domain you own. A domain that
outlives any one product suits it best: the organization holds every
product's projects, and its domain never shows to a customer.

- Create a Google Cloud organization with **Cloud Identity Free**,
  in a private browser window so the new admin account stays apart from
  your personal one:
  https://workspace.google.com/gcpidentity/signup?sku=identitybasic
  Sign up with the domain, then verify it with the TXT record Google
  gives you. On Cloudflare DNS, Google offers to add the record itself.
- Sign in to https://console.cloud.google.com with the new admin account
  and accept the terms. The organization appears in the project picker.
  A picker that shows only "No organization" is signed in with another
  account.

Proof: the project picker, signed in as the admin, lists the domain as an
organization.

Projects that already exist under your personal account can be migrated
into the organization later (IAM & Admin → Settings → Migrate); it is not
required for new projects.

## 1. The billing account

Reuse one that your personal account owns, or create one with the card.
Either way the admin account gets exactly one: signed in with the account
that owns it, https://console.cloud.google.com/billing → the account →
Account management → Add principal → the admin account, role **Billing
Account Administrator**. Rename the account while there, so a budget
alert says which one it is.

The admin's billing page lists it under "No organization": the account
belongs to your personal account, not to the organization, and that is
fine. The script in step 2 and the workflow both find it because it is
the only open account they can see, and both stop if they see two.

Proof: `gcloud billing accounts list` in the admin's Cloud Shell shows one
line, `OPEN: True`.

## 2. The folder, the identity, the rights

One script, `scripts/arm-gcp.sh`. In Cloud Shell
(https://shell.cloud.google.com), signed in as the organization admin,
with your owner in both places:

```bash
curl -fsSL https://raw.githubusercontent.com/<owner>/mainBrain/main/scripts/arm-gcp.sh | bash -s -- <owner>/mainBrain
```

It reads the organization and the billing account, and stops unless it
finds exactly one of each. Then, in order:

1. grants the admin Folder Admin, Project Creator and Organization Policy
   Administrator on the organization, which the admin role lacks;
2. creates the folder `mainbrain-projects`, and in it the project
   `mainbrain-admin-<last six digits of the organization id>`, with the
   APIs the provisioner calls;
3. sets the folder's three exceptions, below;
4. creates the `mainbrain-provisioner` service account: Project Creator,
   Owner and Service Usage Admin on the folder, Billing User and Billing
   Costs Manager on the billing account, nothing on the organization;
5. lets GitHub Actions act as it through Workload Identity Federation:
   this repository by id, on `main`, in a job of the `provisioning`
   environment, so only an approved run gets a token;
6. prints the three repository variables of step 4.

Grants and policies take minutes to apply, a folder policy up to fifteen,
and the script waits for them. A run that stops anyway can be started
again as is: it finds what exists and creates the rest.

### The folder's exceptions to the organization's defaults

An organization created on or after 3 May 2024 enforces Google's
secure-by-default policies. Three of them break this stack, so the
folder overrides those three. The others stay, the ban on service
account keys included: nothing here uses a key.

| Constraint | What it breaks | Folder setting |
|---|---|---|
| `iam.allowedPolicyMemberDomains` | the `allUsers` invoker grant a public HTTPS function or a webhook needs, and the federated grant of step 5 above | allow all |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | Editor on the default compute account, which Cloud Functions v2 builds and runs as | not enforced |
| `storage.uniformBucketLevelAccess` | Firebase's default Storage bucket, which an enforcing organization can refuse | not enforced |

An older organization enforces none of the three, and the script changes
nothing there.

Proof: the script ends with `done` and three variables.

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

## 4. Variables on this repository

Where: this repository → Settings → Secrets and variables → Actions →
tab **Variables**. They identify, they do not authenticate.

| Name | Value |
|---|---|
| `GCP_WIF_PROVIDER` | the `projects/…/providers/github` line the script printed |
| `GCP_PROVISIONER_SA` | the `mainbrain-provisioner@…` line |
| `GCP_FOLDER_ID` | the folder number |

No billing secret: the workflow uses the one billing account the
provisioner can see. A `GCP_BILLING_ACCOUNT` secret, if set, names it
instead, for an identity that can see several.

## 5. The provisioner's own APIs

`arm-gcp.sh` enables them on the admin project. Nothing to do.

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
| `GCP_WIF_PROVIDER is not set` (or another name) | step 4 not done | add the variable |
| `Waiting for review` for a long time | nobody approved | Actions → the run → Review deployments |
| `permission 'resourcemanager.projects.create' denied` | the identity lacks projectCreator on the folder, or the folder id is wrong | run `arm-gcp.sh` again, then compare `GCP_FOLDER_ID` with what it prints |
| `The caller does not have permission` on `billing projects link` | `roles/billing.user` missing on the billing account | run `arm-gcp.sh` again |
| `can use 0 open billing accounts` or `2` | step 1 gave the admin none, or more than one | step 1, then `arm-gcp.sh` again |
| `Unable to acquire impersonated credentials` | the provider accepts this repository on `main` in the `provisioning` environment only | dispatch the workflow from `main`; a renamed or recreated repository needs `arm-gcp.sh` again |
