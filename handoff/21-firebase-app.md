### F5 — The web app config

Where: each project → Project settings → General → Your apps → Add app →
Web. Nickname `{{PROJECT}}-app`. No hosting.

Copy `apiKey` and `appId` from the SDK snippet into the app repo:

- `{{PROJECT}}-app/.env.staging` from `{{FIREBASE_STAGING}}`
- `{{PROJECT}}-app/.env.production` from `{{FIREBASE_PROD}}`

These are public identifiers that ship in the browser bundle; the security
boundary is `firestore.rules` in the functions repo. Commit them.

Then Build → Authentication → Get started → Sign-in method →
Email/Password → Enable, in both projects.

Proof: `npm run dev` in the app boots without "Firebase config incomplete"
once a screen imports `src/lib/firebase.ts`. Until then, the two files
have no blank value.
