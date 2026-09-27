// Site-wide settings, all in one file.
//
// PUBLIC_API_BASE is read at build time and baked into the static output.
// It points at the back end, for the day a page posts a form. The default
// is prod, so a build that forgets to set it posts to the real API rather
// than to nowhere; staging builds set it explicitly.

export const API_BASE: string = (
  import.meta.env.PUBLIC_API_BASE || "https://{{API_DOMAIN}}"
).replace(/\/+$/, "");

export const SITE_DOMAIN = "{{DOMAIN}}";
export const SITE_TITLE = "{{TITLE}}";
