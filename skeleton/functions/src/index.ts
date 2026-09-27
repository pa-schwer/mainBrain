// Function entry points. Firebase deploys exactly what this file exports,
// so a function that is not re-exported here does not exist in production.
// deploy.yml reads the `export { name }` lines below to verify the deploy.

export { health } from "./functions/health";
