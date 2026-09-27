// The bounds, asserted. A doc cannot fail a build; these can.

import assert from "node:assert/strict";
import { test } from "node:test";

import { LIMITS, SCHEMA_VERSION } from "../src/schema/types";
import { MAX_INSTANCES, MAX_RETRIES, RETRY_BACKOFF_MS, SWEEP_BATCH } from "../src/policy";

test("the schema copy is the one the functions were written against", () => {
  assert.equal(SCHEMA_VERSION, 1);
});

test("every loop over data has a finite bound", () => {
  assert.ok(Number.isInteger(SWEEP_BATCH) && SWEEP_BATCH > 0);
  assert.equal(SWEEP_BATCH, LIMITS.SWEEP_BATCH);
});

test("every retry has a cap and a backoff", () => {
  assert.ok(Number.isInteger(MAX_RETRIES) && MAX_RETRIES > 0 && MAX_RETRIES <= 5);
  assert.ok(RETRY_BACKOFF_MS >= 100);
});

test("a runaway cannot outscale the instance ceiling", () => {
  assert.ok(Number.isInteger(MAX_INSTANCES) && MAX_INSTANCES > 0 && MAX_INSTANCES <= 50);
});
