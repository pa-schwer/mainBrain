// The one pattern every algorithm here follows: a loop over data with a
// bound that is a constant, never the size of the input.

import { LIMITS } from "./schema/types";

/**
 * The first `limit` items, `LIMITS.SWEEP_BATCH` at most whatever the
 * caller asks. The cap is the rule, not the argument.
 */
export function takeBounded<T>(items: readonly T[], limit: number = LIMITS.SWEEP_BATCH): T[] {
  const cap = Math.min(Math.max(0, Math.floor(limit)), LIMITS.SWEEP_BATCH);
  return items.slice(0, cap);
}
