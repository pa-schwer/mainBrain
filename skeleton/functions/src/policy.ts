// Bounds and promises, as constants.
//
// This module imports nothing that touches the network or the Admin SDK, so
// a test can assert against it without a Firebase project. A rule that
// cannot be asserted in CI is a rule that drifts.

import { LIMITS } from "./schema/types";

/** Instances a runaway cannot outscale. Set once, raised by decision. */
export const MAX_INSTANCES = 10;

/** Documents a scheduled run touches; the rest waits for the next run. */
export const SWEEP_BATCH: number = LIMITS.SWEEP_BATCH;

/** Outbound retries before giving up, with backoff between them. */
export const MAX_RETRIES: number = LIMITS.MAX_RETRIES;
export const RETRY_BACKOFF_MS = 500;
