// Build the dashboard against the Firebase project that matches the branch.
// Workers Builds sets WORKERS_CI_BRANCH; scripts/mode.mjs decides.

import { execSync } from "node:child_process";
import { modeFor } from "./mode.mjs";

const branch = process.env.WORKERS_CI_BRANCH ?? process.env.CF_PAGES_BRANCH ?? "";
const mode = modeFor(branch);

console.log(`branch: ${branch || "(none)"} -> vite mode: ${mode}`);
execSync(`vite build --mode ${mode}`, { stdio: "inherit" });
