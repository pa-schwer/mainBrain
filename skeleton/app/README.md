# {{PROJECT}}-app

Dashboard for {{TITLE}} at {{APP_DOMAIN}}. Vite, React, Firebase client,
served by a Cloudflare Worker.

```bash
npm ci
npm run dev
npm run typecheck && npm test && npm run build
bash scripts/no-hardcoded-tokens.sh
```

Read `CLAUDE.md`. The Firebase web config in `.env.staging` and
`.env.production` is filled by `../{{PROJECT}}-ops/HANDOFF.md`, step F5.
