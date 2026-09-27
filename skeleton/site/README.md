# {{PROJECT}}-site

Public site for {{TITLE}} at {{DOMAIN}}. Astro and Tailwind, static
output, served by a Cloudflare Worker.

```bash
npm ci
npm run dev         # http://localhost:4321
npm run typecheck && npm test && npm run build
bash scripts/no-hardcoded-tokens.sh
```

Read `CLAUDE.md`. Deploy setup and every other manual step is in
`../HANDOFF.md`; the launch checklist is `LAUNCH.md`.
