# dahaitang.com

Source for my personal site: **[dahaitang.com](https://dahaitang.com)**

I work in strategy and operations, and I build my own systems with AI. The site has write-ups of six of those systems and a few short pieces of writing.

## How it is built

- [Astro](https://astro.build), static output, deployed on Cloudflare.
- No analytics, no cookies, self-hosted font.
- A privacy scanner runs before every build and stops it if a page contains anything that looks private. See [`scripts/scan_secrets.py`](scripts/scan_secrets.py) and the write-up: [A privacy gate for a public site](https://dahaitang.com/writing/privacy-gate/).

## Run it locally

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # runs the scanner, then builds to ./dist
```

## Layout

```text
src/content/projects/   one Markdown file per system
src/content/writing/    one Markdown file per article
src/pages/              routes
src/styles/tokens.css   colours, type, shared classes
scripts/                privacy scanner and its rules
```

Content © Dahai Tang. The code is free to read and learn from.
