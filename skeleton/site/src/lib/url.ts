// Absolute URLs for canonical links and share tags. No DOM, so it runs
// under a unit test.

export function absoluteUrl(site: string, pathname: string): string {
  const base = site.endsWith("/") ? site : `${site}/`;
  const path = pathname.startsWith("/") ? pathname.slice(1) : pathname;
  return new URL(path, base).href;
}
