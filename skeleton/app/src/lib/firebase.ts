// Firebase client, initialized once.
//
// Initialization and handles, and nothing else. No query lives here, no
// rule, no derived number. This repo reads Firestore and calls functions;
// anything that decides something belongs in the functions repo.

import { initializeApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth } from "firebase/auth";
import { getFirestore, type Firestore } from "firebase/firestore";

// Each value is read as a static `import.meta.env.VITE_*` access. Vite
// substitutes those at build time; a dynamic lookup like env[key] is left
// alone and comes back undefined in the production bundle.
const config = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const missing = Object.entries(config)
  .filter(([, value]) => !value)
  .map(([key]) => key);

if (missing.length > 0) {
  // Fail at startup, naming the fields. A dashboard that boots into an
  // empty screen because one key was blank costs an afternoon to diagnose.
  throw new Error(
    `Firebase config incomplete. Missing: ${missing.join(", ")}. ` +
      `Fill .env.staging and .env.production (HANDOFF.md, step F5).`,
  );
}

export const app: FirebaseApp = initializeApp(config);
export const auth: Auth = getAuth(app);
export const db: Firestore = getFirestore(app);
