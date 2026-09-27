import assert from "node:assert/strict";
import { test } from "node:test";

import { statusBody } from "../src/status";

test("health answers ok with the project and the schema version", () => {
  const body = statusBody("{{FIREBASE_STAGING}}", 1_700_000_000_000);
  assert.deepEqual(body, {
    ok: true,
    project: "{{FIREBASE_STAGING}}",
    schemaVersion: 1,
    now: 1_700_000_000_000,
  });
});
