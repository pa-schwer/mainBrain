// What `health` answers. Pure, so a test covers it without Firebase.

import { SCHEMA_VERSION } from "./schema/types";

export interface Status {
  ok: true;
  project: string;
  schemaVersion: number;
  now: number;
}

export function statusBody(project: string, now: number): Status {
  return { ok: true, project, schemaVersion: SCHEMA_VERSION, now };
}
