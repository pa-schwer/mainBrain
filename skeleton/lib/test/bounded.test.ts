import assert from "node:assert/strict";
import { test } from "node:test";

import { LIMITS, takeBounded } from "../src/index";

test("returns the items when there are fewer than the bound", () => {
  assert.deepEqual(takeBounded([1, 2, 3]), [1, 2, 3]);
});

test("never returns more than the schema bound, whatever the caller asks", () => {
  const many = Array.from({ length: LIMITS.SWEEP_BATCH * 3 }, (_, i) => i);
  assert.equal(takeBounded(many).length, LIMITS.SWEEP_BATCH);
  assert.equal(takeBounded(many, LIMITS.SWEEP_BATCH * 10).length, LIMITS.SWEEP_BATCH);
});

test("a negative or fractional limit is clamped", () => {
  assert.deepEqual(takeBounded([1, 2, 3], -1), []);
  assert.deepEqual(takeBounded([1, 2, 3], 1.9), [1]);
});
