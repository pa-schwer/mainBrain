import assert from "node:assert/strict";
import { test } from "node:test";
import { modeFor } from "./mode.mjs";

test("prod is the only branch that builds against production", () => {
  assert.equal(modeFor("prod"), "production");
  assert.equal(modeFor("main"), "staging");
  assert.equal(modeFor("feature/x"), "staging");
});

test("an unknown branch builds against staging", () => {
  assert.equal(modeFor(""), "staging");
  assert.equal(modeFor(undefined), "staging");
});
