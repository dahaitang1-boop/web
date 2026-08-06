// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { WIP } from './src/config.ts';

// https://astro.build/config
export default defineConfig({
  site: 'https://dahaitang.com',
  // No sitemap while the site is unfinished: a sitemap is a public directory
  // of exactly the URLs that are meant to be unlisted for now. Re-enable it
  // together with the WIP flag in src/config.ts.
  integrations: WIP ? [] : [sitemap()],
  build: {
    // Emit /about/index.html rather than /about.html so URLs have no extension.
    format: 'directory',
  },
});
