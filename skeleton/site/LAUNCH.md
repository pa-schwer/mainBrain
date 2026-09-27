# Launch checklist

Everything between this repo on `main` and a real visitor on {{DOMAIN}}.
Tick in the pull request that does it.

- [ ] `robots.txt`: replace `Disallow: /` with `Disallow:` so crawlers
      are welcome.
- [ ] `{{DOMAIN}}` on Cloudflare DNS, custom domain on the production
      Worker (HANDOFF.md, step C3).
- [ ] `www.{{DOMAIN}}` redirects to `{{DOMAIN}}`.
- [ ] Staging preview URLs do not get indexed: check that Workers previews
      send `X-Robots-Tag: noindex`, or add it for non-prod.
- [ ] A contact mailbox exists and is in the footer.
- [ ] Legal pages (privacy, terms) reviewed by a lawyer; every `{{...}}`
      placeholder filled.
- [ ] Lighthouse mobile ≥ 95 on all four categories against the
      production URL.
