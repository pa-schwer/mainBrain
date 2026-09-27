// Runtime wiring shared by every function: the Admin SDK handle and the
// per-project params.
//
// Secrets are declared here and nowhere else, with `defineSecret`, in the
// cycle that first reads them. A declared secret has to exist in Secret
// Manager before the deploy goes through, so declaring one ahead of its use
// blocks every deploy until someone creates a value nothing reads.
// Names this project will use: {{SECRET_NAMES_OR_NONE}}.

import { getApps, initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { defineInt } from "firebase-functions/params";
import { setGlobalOptions } from "firebase-functions/v2";

import { MAX_INSTANCES } from "./policy";

// A ceiling on every function, before anything else is declared. A loop
// that never ends is not a hang on Cloud Functions, it is a bill: the
// platform scales the instance that is stuck. Raising the ceiling is a
// decisions.md line, not an edit.
setGlobalOptions({ maxInstances: MAX_INSTANCES });

// Per-project config, bound from .env.<projectId> at deploy time.
export const WARM_INSTANCES = defineInt("WARM_INSTANCES", { default: 0 });

// Guarded so the emulator, which loads this module more than once, does not
// throw on a second initializeApp.
if (getApps().length === 0) {
  initializeApp();
}

export const db = getFirestore();

/** Epoch ms. Every timestamp in the schema is this, never a Timestamp. */
export const now = (): number => Date.now();
