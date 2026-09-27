// The Firestore layout, in one place.
//
// accounts/{accountId}
//
// Paths built by string concatenation at several call sites drift the same
// way a schema copied into several repos drifts, so they are built here.

export const accountPath = (accountId: string): string => `accounts/${accountId}`;
