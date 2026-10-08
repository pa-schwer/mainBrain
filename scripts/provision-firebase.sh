#!/usr/bin/env bash
# Provision the two Firebase projects of a spawned project: staging and
# prod. Runs inside .github/workflows/create-firebase-projects.yml, after
# the workflow has authenticated to Google Cloud and GitHub. Idempotent:
# every step checks before it creates, so a re-run after a red step picks
# up where it stopped.
#
# What it does, per project:
#   1. create the project in the folder            (HANDOFF F1)
#   2. link it to the billing account, Blaze        (HANDOFF F2)
#   3. create a budget with alerts                  (HANDOFF F2)
#   4. enable the APIs Functions v2 needs           (HANDOFF F3)
#   5. add Firebase, Firestore Native, Email auth,
#      the default Storage bucket                   (HANDOFF F1, F5)
#   6. create the github-deploy account, 4 roles, and let the
#      functions repo act as it, keyless                    (HANDOFF F4)
#   7. create the web app and print its public config       (HANDOFF F5)
#
# Inputs, as environment variables (the workflow sets them):
#   PROJECT           slug, used for names
#   STAGING_ID, PROD_ID   Google Cloud project ids
#   REGION            Firestore and Functions region
#   FOLDER_ID         numeric folder that holds every mainBrain project
#   BILLING_ACCOUNT   XXXXXX-XXXXXX-XXXXXX, or empty: the one open account the
#                     provisioning identity can use (docs/gcp-provisioning.md)
#   FUNCTIONS_REPO    owner/name of the functions repo, or empty
#   APP_REPO          owner/name of the app repo, or empty
#   BUDGET_STAGING, BUDGET_PROD   monthly amounts, in the billing currency
#   GH_TOKEN          a token that can write Actions variables and contents
#
# No key exists. Each project gets a Workload Identity pool that trusts
# the functions repo's GitHub OIDC token on one branch, and the repo gets
# the pool's provider id as a variable, which identifies and grants nothing.

set -euo pipefail

: "${PROJECT:?}" "${STAGING_ID:?}" "${PROD_ID:?}" "${REGION:?}" "${FOLDER_ID:?}"
if [ -z "${BILLING_ACCOUNT:-}" ]; then
  # scripts/arm-gcp.sh grants the identity exactly one billing account. Two
  # would make this a guess about who pays, so it stops instead.
  mapfile -t bills < <(gcloud billing accounts list --filter='open=true' --format='value(name.basename())')
  if [ "${#bills[@]}" -ne 1 ]; then
    echo "The provisioning identity can use ${#bills[@]} open billing accounts; set the"
    echo "GCP_BILLING_ACCOUNT secret on this repository to name the one that pays."
    exit 1
  fi
  BILLING_ACCOUNT="${bills[0]}"
fi
FUNCTIONS_REPO="${FUNCTIONS_REPO:-}"
APP_REPO="${APP_REPO:-}"
BUDGET_STAGING="${BUDGET_STAGING:-10}"
BUDGET_PROD="${BUDGET_PROD:-50}"

APIS=(
  cloudresourcemanager.googleapis.com
  serviceusage.googleapis.com
  iam.googleapis.com
  iamcredentials.googleapis.com
  sts.googleapis.com
  cloudbilling.googleapis.com
  billingbudgets.googleapis.com
  firebase.googleapis.com
  firestore.googleapis.com
  identitytoolkit.googleapis.com
  firebasestorage.googleapis.com
  storage.googleapis.com
  cloudfunctions.googleapis.com
  cloudbuild.googleapis.com
  artifactregistry.googleapis.com
  run.googleapis.com
  eventarc.googleapis.com
  pubsub.googleapis.com
  cloudscheduler.googleapis.com
  secretmanager.googleapis.com
)

# The four roles the deploy account needs. Editor carries no setIamPolicy,
# which is why the last two exist: an HTTPS function a third party calls
# needs an invoker grant on the function and on its Cloud Run service.
DEPLOY_ROLES=(
  roles/editor
  roles/secretmanager.admin
  roles/cloudfunctions.admin
  roles/run.admin
)

say() { printf '\n== %s\n' "$*"; }
ok()  { printf '  ok      %s\n' "$*"; }
did() { printf '  created %s\n' "$*"; }

provision() {
  local id="$1" env="$2" budget="$3" var_name="$4"

  say "$id ($env)"

  # 1. project
  if gcloud projects describe "$id" --format='value(projectId)' > /dev/null 2>&1; then
    ok "project exists"
  else
    gcloud projects create "$id" --name="$PROJECT $env" --folder="$FOLDER_ID" --quiet
    did "project"
  fi
  local number
  number=$(gcloud projects describe "$id" --format='value(projectNumber)')

  # 2. billing
  local linked
  linked=$(gcloud billing projects describe "$id" --format='value(billingAccountName)' 2>/dev/null || true)
  if [ "$linked" = "billingAccounts/$BILLING_ACCOUNT" ]; then
    ok "billing linked"
  else
    gcloud billing projects link "$id" --billing-account="$BILLING_ACCOUNT" --quiet
    did "billing link (Blaze)"
  fi

  # 4. APIs (before the budget: billingbudgets is one of them)
  gcloud services enable "${APIS[@]}" --project="$id" --quiet
  ok "${#APIS[@]} APIs enabled"

  # 3. budget, the last safety net against a runaway loop
  if gcloud billing budgets list --billing-account="$BILLING_ACCOUNT" \
       --filter="displayName=$id" --format='value(name)' | grep -q .; then
    ok "budget exists"
  else
    gcloud billing budgets create --billing-account="$BILLING_ACCOUNT" \
      --display-name="$id" --budget-amount="$budget" \
      --filter-projects="projects/$number" \
      --threshold-rule=percent=0.5 --threshold-rule=percent=0.9 --threshold-rule=percent=1.0 \
      --quiet
    did "budget $budget with alerts at 50, 90, 100 %"
  fi

  # 5. Firebase, Firestore, Auth, Storage
  if firebase projects:list --json 2>/dev/null | jq -e --arg id "$id" '.result[] | select(.projectId == $id)' > /dev/null; then
    ok "firebase added"
  else
    firebase projects:addfirebase "$id" --non-interactive
    did "firebase"
  fi

  if gcloud firestore databases describe --database='(default)' --project="$id" > /dev/null 2>&1; then
    ok "firestore exists"
  else
    gcloud firestore databases create --database='(default)' --location="$REGION" \
      --type=firestore-native --project="$id" --quiet
    did "firestore native in $REGION"
  fi

  # Email/Password sign-in. The config resource appears once Firebase is
  # added; PATCH is idempotent.
  local token
  token=$(gcloud auth print-access-token)
  local code
  code=$(curl -sS -o /tmp/auth.json -w '%{http_code}' -X PATCH \
    -H "Authorization: Bearer $token" -H "Content-Type: application/json" \
    "https://identitytoolkit.googleapis.com/admin/v2/projects/$id/config?updateMask=signIn.email" \
    -d '{"signIn":{"email":{"enabled":true,"passwordRequired":true}}}')
  if [ "$code" = "200" ]; then
    ok "auth email/password enabled"
  else
    echo "  WARN    auth config returned $code; enable Email/Password by hand in the console (HANDOFF F5)"
  fi

  # The default Storage bucket. `firebase deploy --only storage` stops on a
  # project without one and points at the console's Get Started button.
  # Create re-links a bucket that exists, so a re-run is safe.
  code=$(curl -sS -o /tmp/bucket.json -w '%{http_code}' -X POST \
    -H "Authorization: Bearer $token" -H "Content-Type: application/json" \
    -H "X-Goog-User-Project: $id" \
    "https://firebasestorage.googleapis.com/v1beta/projects/$id/defaultBucket" \
    -d "{\"location\":\"$REGION\"}")
  if [ "$code" = "200" ] || [ "$code" = "409" ]; then
    ok "storage default bucket in $REGION"
  else
    echo "  WARN    storage bucket returned $code: $(jq -r '.error.message // empty' /tmp/bucket.json)"
    echo "          the functions deploy stops on storage until it exists (HANDOFF F1)"
  fi

  # 6. deploy account and roles; the functions repo acts as it through
  # Workload Identity Federation. The pool trusts one repository by id (a
  # name can be registered again after a rename) and one branch: main for
  # staging, prod for prod.
  local sa="github-deploy@$id.iam.gserviceaccount.com"
  if gcloud iam service-accounts describe "$sa" --project="$id" > /dev/null 2>&1; then
    ok "deploy account exists"
  else
    gcloud iam service-accounts create github-deploy --display-name="GitHub Actions deploy" --project="$id" --quiet
    did "deploy account"
  fi
  for role in "${DEPLOY_ROLES[@]}"; do
    gcloud projects add-iam-policy-binding "$id" --member="serviceAccount:$sa" --role="$role" \
      --condition=None --quiet > /dev/null
  done
  ok "4 roles on the deploy account"

  if [ -n "$FUNCTIONS_REPO" ]; then
    local repo_id branch pool
    repo_id=$(gh api "repos/$FUNCTIONS_REPO" --jq .id)
    branch=$([ "$env" = staging ] && echo main || echo prod)
    pool="projects/$number/locations/global/workloadIdentityPools/github"

    if gcloud iam workload-identity-pools describe github --location=global --project="$id" > /dev/null 2>&1; then
      ok "identity pool exists"
    else
      gcloud iam workload-identity-pools create github --location=global \
        --display-name="GitHub Actions" --project="$id" --quiet
      did "identity pool"
    fi

    # update-oidc on a re-run, so a changed repo or branch replaces the old trust.
    local verb=create-oidc
    if gcloud iam workload-identity-pools providers describe github --workload-identity-pool=github \
         --location=global --project="$id" > /dev/null 2>&1; then
      verb=update-oidc
    fi
    gcloud iam workload-identity-pools providers "$verb" github \
      --workload-identity-pool=github --location=global --project="$id" \
      --issuer-uri="https://token.actions.githubusercontent.com" \
      --attribute-mapping="google.subject=assertion.sub,attribute.repository_id=assertion.repository_id,attribute.ref=assertion.ref" \
      --attribute-condition="assertion.repository_id == '$repo_id' && assertion.ref == 'refs/heads/$branch'" \
      --quiet > /dev/null
    ok "provider trusts $FUNCTIONS_REPO on $branch"

    gcloud iam service-accounts add-iam-policy-binding "$sa" --project="$id" \
      --role=roles/iam.workloadIdentityUser \
      --member="principalSet://iam.googleapis.com/$pool/attribute.repository_id/$repo_id" \
      --quiet > /dev/null
    ok "$FUNCTIONS_REPO may act as the deploy account"

    gh variable set "$var_name" --repo "$FUNCTIONS_REPO" --body "$pool/providers/github"
    ok "$var_name on $FUNCTIONS_REPO"
  else
    echo "  skip    no functions repo given; no deploy identity"
  fi

  # 7. web app and its public config
  local app_id
  app_id=$(firebase apps:list WEB --project "$id" --json 2>/dev/null | jq -r '.result[0].appId // empty')
  if [ -z "$app_id" ]; then
    firebase apps:create WEB "$PROJECT-app" --project "$id" --non-interactive > /dev/null
    app_id=$(firebase apps:list WEB --project "$id" --json | jq -r '.result[0].appId')
    did "web app"
  else
    ok "web app exists"
  fi
  local cfg
  cfg=$(firebase apps:sdkconfig WEB "$app_id" --project "$id" --json | jq -r '.result.sdkConfig')
  # Public by construction: these values ship in the browser bundle. The
  # security boundary is firestore.rules.
  local env_file
  env_file=$(mktemp)
  {
    echo "# Firebase web config for $id, written by mainBrain's provisioning workflow."
    echo "# Public by construction; the security boundary is firestore.rules."
    echo "VITE_FIREBASE_API_KEY=$(jq -r .apiKey <<< "$cfg")"
    echo "VITE_FIREBASE_AUTH_DOMAIN=$(jq -r .authDomain <<< "$cfg")"
    echo "VITE_FIREBASE_PROJECT_ID=$(jq -r .projectId <<< "$cfg")"
    echo "VITE_FIREBASE_APP_ID=$(jq -r .appId <<< "$cfg")"
  } > "$env_file"
  local target
  target=$([ "$env" = staging ] && echo ".env.staging" || echo ".env.production")
  if [ -n "$APP_REPO" ]; then
    local sha
    sha=$(gh api "repos/$APP_REPO/contents/$target" --jq .sha 2>/dev/null || true)
    if gh api --method PUT "repos/$APP_REPO/contents/$target" \
         -f message="chore: Firebase web config for $id (provisioning workflow)" \
         -f content="$(base64 -w0 "$env_file")" ${sha:+-f sha="$sha"} > /dev/null; then
      did "$target committed to $APP_REPO"
    else
      echo "  WARN    could not write $target to $APP_REPO; the values follow"
      cat "$env_file"
    fi
  else
    echo "  info    no app repo given; $target values:"
    cat "$env_file"
  fi
  rm -f "$env_file"
}

provision "$STAGING_ID" staging "$BUDGET_STAGING" GCP_WIF_PROVIDER_STAGING
provision "$PROD_ID"    prod    "$BUDGET_PROD"    GCP_WIF_PROVIDER_PROD

say "done"
echo "Proof: push main of the functions repo; its Deploy workflow should end with"
echo "'all exported functions are deployed on staging'."
