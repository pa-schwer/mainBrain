// Which Vite mode a branch builds with. Pure, so scripts/mode.test.mjs
// covers it without running a build.
//
// `prod` builds with .env.production; everything else, including a local
// machine with no branch variable at all, builds with .env.staging. The
// default is staging on purpose: a build that cannot tell where it is
// must not point at prod.

export function modeFor(branch) {
  return branch === "prod" ? "production" : "staging";
}
