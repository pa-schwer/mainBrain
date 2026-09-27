/**
 * Dashboard shell. Scaffold only.
 *
 * Nothing here reads Firestore yet. src/lib/firebase.ts is wired and
 * unused on purpose: importing it throws when the Firebase env vars are
 * blank, and `npm run dev` should work on a fresh checkout.
 *
 * When the real screens land, they read and render. A derived number is
 * computed in the functions repo, not here.
 */
export default function App() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="text-2xl font-semibold tracking-tight">{{TITLE}}</h1>
      <p className="mt-2 text-sm">Dashboard scaffold.</p>
    </main>
  );
}
