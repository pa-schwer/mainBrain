// SOURCE OF TRUTH: {{PROJECT}}-ops — do not edit here unless this file is
// {{PROJECT}}-ops/docs/schema/types.ts. Every other copy is byte-identical:
{{SCHEMA_COPY_COMMENT}}
// Run scripts/check-schema.sh after any change.
//
// Rules that every type below follows:
//   - timestamps are epoch ms `number`, never a database Timestamp
//   - changes are additive: new fields optional, no rename, no type change
//   - a constant that states a promise (a limit, a price, a legal rule)
//     lives here and has a test in the functions repo

/** Bumped on every change to this file. The functions repo asserts it. */
export const SCHEMA_VERSION = 1;

/** Epoch milliseconds. */
export type EpochMs = number;

/**
 * Bounds that every loop over data respects. A loop over data with no
 * bound is a bill on a serverless runtime; the bound is a constant so a
 * test can assert it.
 */
export const LIMITS = {
  /** Documents processed per scheduled run; the rest waits for the next run. */
  SWEEP_BATCH: 200,
  /** Retries of an outbound call before giving up. */
  MAX_RETRIES: 3,
} as const;
