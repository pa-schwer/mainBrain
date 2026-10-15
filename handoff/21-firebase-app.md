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

Then Authentication → Settings → **Authorized domains** → Add domain, in
both projects. The app is served by Cloudflare, not by Firebase Hosting,
and Firebase opens a sign-in provider's sheet (Google and the like), or
lets an email link continue into the app, only from a domain it lists:

- `{{FIREBASE_STAGING}}`: the host of the `main` preview URL (C1's proof),
  without `https://` and without a path
- `{{FIREBASE_PROD}}`: `{{APP_DOMAIN}}`, once C2 is done

Keep `localhost` and the `firebaseapp.com` and `web.app` entries Firebase
put there.

Proof: on staging, a provider's sign-in opens its sheet; without the
domain it fails with `auth/unauthorized-domain` in the browser console.
