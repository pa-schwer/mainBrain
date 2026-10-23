// The one function the scaffold deploys. It proves the pipeline end to
// end: build, deploy, IAM, and the verify step in deploy.yml. Keep it.

import { onRequest } from "firebase-functions/v2/https";
import { logger } from "firebase-functions";

import { now } from "../config";
import { statusBody } from "../status";

export const health = onRequest(
  {
    region: "{{REGION}}",
    timeoutSeconds: 10,
    // Every function loads the whole index.js, so health carries what the
    // project's code grows to: a project's took about 100 MB before a
    // request, and at 128 MiB its cold starts failed.
    memory: "256MiB",
    // Public on purpose: it carries no data. A function that a third party
    // must call gets the same invoker grant through the deploy account's
    // Cloud Functions Admin and Cloud Run Admin roles.
    invoker: "public",
  },
  (request, response) => {
    if (request.method !== "GET") {
      response.status(405).json({ ok: false, error: "GET only" });
      return;
    }
    const project = process.env.GCLOUD_PROJECT ?? "unknown";
    const body = statusBody(project, now());
    logger.info("health", body);
    response.status(200).json(body);
  },
);
