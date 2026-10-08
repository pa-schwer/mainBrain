#!/usr/bin/env bash
# Arm the "Create Firebase projects" workflow for one Google Cloud
# organization: docs/gcp-provisioning.md steps 2 and 5 in one run. Run it
# once, in Cloud Shell, signed in as the organization admin:
#
#   bash <(curl -fsSL https://raw.githubusercontent.com/<owner>/mainBrain/<commit>/scripts/arm-gcp.sh) <owner>/mainBrain
#
# <commit> is the full id of a commit whose copy of this file you have
# read: an organization admin runs it, so a branch that can move is not
# a source.
# It reads the organization and the billing account from what the admin
# can see, and stops unless there is exactly one of each: a guess here
# would hand the wrong account to the workflow. Idempotent: a re-run finds
# what exists and creates the rest. It ends by printing the three
# repository variables the workflow needs (docs step 4).

set -euo pipefail
export CLOUDSDK_CORE_DISABLE_PROMPTS=1

GITHUB_REPO="${1:?usage: bash arm-gcp.sh <owner>/mainBrain}"
FOLDER_NAME=mainbrain-projects

say() { printf '\n== %s\n' "$*"; }
ok()  { printf '  ok      %s\n' "$*"; }
did() { printf '  created %s\n' "$*"; }
die() { printf '  STOP    %s\n' "$*" >&2; exit 1; }

# A grant, a new resource or an enabled API takes minutes to apply (an
# organization grant up to seven), and a policy up to fifteen. Retry until
# the command succeeds; the last try shows its error. TRIES overrides the
# default eight minutes.
retry() {
  local i out tries="${TRIES:-24}"
  for ((i = 1; i < tries; i++)); do
    if out=$("$@" 2> /dev/null); then
      printf '%s' "$out"
      return 0
    fi
    printf '  wait    not applied yet, retry %s/%s in 20 s\n' "$i" "$tries" >&2
    sleep 20
  done
  "$@"
}

say "what this admin can see"
ME=$(gcloud config get-value account 2> /dev/null)
mapfile -t orgs < <(gcloud organizations list --format='value(ID)')
[ "${#orgs[@]}" -eq 1 ] || die "expected one organization, found ${#orgs[@]}; sign in as the organization admin"
ORG_ID="${orgs[0]}"
mapfile -t bills < <(gcloud billing accounts list --filter='open=true' --format='value(name.basename())')
[ "${#bills[@]}" -eq 1 ] || die "expected one open billing account, found ${#bills[@]}; docs step 1 gives this admin exactly one"
BILLING_ACCOUNT="${bills[0]}"
# A failed request falls through to the check below, so it stops with a reason.
REPO_ID=$(curl -fsS "https://api.github.com/repos/$GITHUB_REPO" | jq -r '.id') || true
[[ "$REPO_ID" =~ ^[0-9]+$ ]] || die "cannot read the id of $GITHUB_REPO from GitHub"
ok "$ME, organization $ORG_ID"
ok "billing account $(gcloud billing accounts describe "$BILLING_ACCOUNT" --format='value(displayName)')"
ok "$GITHUB_REPO is repository $REPO_ID"

say "your rights on the organization"
# The organization admin may grant roles but not create folders or set
# policies; it grants itself those two, and project creation.
for role in roles/resourcemanager.folderAdmin roles/resourcemanager.projectCreator roles/orgpolicy.policyAdmin; do
  gcloud organizations add-iam-policy-binding "$ORG_ID" --member="user:$ME" --role="$role" \
    --condition=None > /dev/null
done
ok "folder admin, project creator, organization policy admin"

say "the folder"
folder_id() {
  local id
  id=$(gcloud resource-manager folders list --organization="$ORG_ID" \
    --filter="displayName=$FOLDER_NAME" --format='value(name.basename())') && [ -n "$id" ] && printf '%s' "$id"
}
# Listing waits for the grants above; an empty organization lists nothing.
retry gcloud resource-manager folders list --organization="$ORG_ID" --limit=1 > /dev/null
if FOLDER_ID=$(folder_id); then
  ok "$FOLDER_NAME exists"
else
  retry gcloud resource-manager folders create --display-name="$FOLDER_NAME" --organization="$ORG_ID" > /dev/null
  FOLDER_ID=$(retry folder_id)
  did "$FOLDER_NAME"
fi
ok "folder $FOLDER_ID"

say "the admin project"
# Outside the folder: the provisioner owns what it creates in the folder,
# and must not reach the project that holds its own identity. Project ids
# are global; the organization's id keeps this one unique and the same on
# every re-run.
ADMIN_PROJECT="mainbrain-admin-${ORG_ID: -6}"
if gcloud projects describe "$ADMIN_PROJECT" > /dev/null 2>&1; then
  ok "$ADMIN_PROJECT exists"
else
  retry gcloud projects create "$ADMIN_PROJECT" --organization="$ORG_ID" --name="mainBrain admin" > /dev/null
  did "$ADMIN_PROJECT"
fi
ADMIN_NUMBER=$(retry gcloud projects describe "$ADMIN_PROJECT" --format='value(projectNumber)')
retry gcloud services enable iam.googleapis.com iamcredentials.googleapis.com sts.googleapis.com \
  cloudresourcemanager.googleapis.com serviceusage.googleapis.com orgpolicy.googleapis.com \
  cloudbilling.googleapis.com billingbudgets.googleapis.com firebase.googleapis.com \
  --project="$ADMIN_PROJECT" > /dev/null
ok "APIs enabled"

say "the exceptions to the organization's defaults"
# docs/gcp-provisioning.md step 2 says what each one unblocks. The folder
# holds product projects only; the admin project gets the domain exception
# alone, for the federated grant below. Set before any grant.
policy=$(mktemp)
for parent in "folders/$FOLDER_ID" "projects/$ADMIN_PROJECT"; do
  printf 'name: %s/policies/iam.allowedPolicyMemberDomains\nspec:\n  rules:\n  - allowAll: true\n' \
    "$parent" > "$policy"
  retry gcloud org-policies set-policy "$policy" --billing-project="$ADMIN_PROJECT" > /dev/null
done
for c in iam.automaticIamGrantsForDefaultServiceAccounts storage.uniformBucketLevelAccess; do
  printf 'name: folders/%s/policies/%s\nspec:\n  rules:\n  - enforce: false\n' "$FOLDER_ID" "$c" > "$policy"
  retry gcloud org-policies set-policy "$policy" --billing-project="$ADMIN_PROJECT" > /dev/null
done
rm -f "$policy"
ok "public invoker, default account grants, bucket access: allowed in the folder"
# These overrides name the classic constraints. An organization can also
# enforce "managed" ones the script does not know; say which, so a red
# provisioning run is read against them. The key bans are expected.
managed=$(gcloud org-policies list --organization="$ORG_ID" --billing-project="$ADMIN_PROJECT" \
  --format='value(name.basename())' 2> /dev/null | grep '\.managed\.' | grep -v 'ServiceAccountKey' || true)
[ -z "$managed" ] || printf '  note    the organization also enforces: %s\n' "$(echo $managed)"

say "the provisioning identity"
SA="mainbrain-provisioner@$ADMIN_PROJECT.iam.gserviceaccount.com"
if gcloud iam service-accounts describe "$SA" --project="$ADMIN_PROJECT" > /dev/null 2>&1; then
  ok "service account exists"
else
  retry gcloud iam service-accounts create mainbrain-provisioner --display-name="mainBrain provisioner" \
    --project="$ADMIN_PROJECT" > /dev/null
  did "service account"
fi
# Create projects in the folder: a project's creator becomes its owner,
# so the provisioner owns what it creates and nothing else. Link and
# budget on the one billing account. Nothing at organization level. The
# folder grant waits for the folder's policy, up to fifteen minutes.
TRIES=45 retry gcloud resource-manager folders add-iam-policy-binding "$FOLDER_ID" \
  --member="serviceAccount:$SA" --role=roles/resourcemanager.projectCreator --condition=None > /dev/null
for role in roles/billing.user roles/billing.costsManager; do
  retry gcloud billing accounts add-iam-policy-binding "$BILLING_ACCOUNT" \
    --member="serviceAccount:$SA" --role="$role" > /dev/null
done
ok "rights on the folder and the billing account"

say "who may act as it"
# GitHub Actions of that one repository, by id, on main, in the job that
# waits for the founder's approval (the provisioning environment).
if gcloud iam workload-identity-pools describe github --location=global --project="$ADMIN_PROJECT" > /dev/null 2>&1; then
  ok "identity pool exists"
else
  retry gcloud iam workload-identity-pools create github --location=global --display-name="GitHub Actions" \
    --project="$ADMIN_PROJECT" > /dev/null
  did "identity pool"
fi
verb=create-oidc
if gcloud iam workload-identity-pools providers describe github --workload-identity-pool=github \
     --location=global --project="$ADMIN_PROJECT" > /dev/null 2>&1; then
  verb=update-oidc
fi
retry gcloud iam workload-identity-pools providers "$verb" github \
  --workload-identity-pool=github --location=global --project="$ADMIN_PROJECT" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository_id=assertion.repository_id" \
  --attribute-condition="assertion.repository_id == '$REPO_ID' && assertion.ref == 'refs/heads/main' && assertion.environment == 'provisioning'" \
  > /dev/null
pool="projects/$ADMIN_NUMBER/locations/global/workloadIdentityPools/github"
TRIES=45 retry gcloud iam service-accounts add-iam-policy-binding "$SA" --project="$ADMIN_PROJECT" \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/$pool/attribute.repository_id/$REPO_ID" > /dev/null
ok "$GITHUB_REPO on main, environment provisioning"

say "done. Three repository variables for $GITHUB_REPO (docs step 4):"
echo "  https://github.com/$GITHUB_REPO/settings/variables/actions"
echo
echo "  GCP_WIF_PROVIDER    $pool/providers/github"
echo "  GCP_PROVISIONER_SA  $SA"
echo "  GCP_FOLDER_ID       $FOLDER_ID"
echo
echo "No billing secret: the workflow finds the one billing account the identity can use."
