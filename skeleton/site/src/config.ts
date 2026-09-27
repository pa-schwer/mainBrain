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

// LAUNCH.md: the mailbox has to exist before prod.
export const CONTACT_EMAIL = "hello@{{DOMAIN}}";

// LAUNCH.md: a physical postal address is a legal requirement for the
// footer of a commercial site. The marker stays visible until it is filled.
export const POSTAL_ADDRESS = "[POSTAL ADDRESS]";
