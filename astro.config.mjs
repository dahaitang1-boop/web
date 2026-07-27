// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Must be set before anything ships: canonical URLs and the sitemap both
  // silently no-op without it. Change this when the real domain is bought.
  site: 'https://dahaitang.com',
  integrations: [sitemap()],
  build: {
    // Emit /about/index.html rather than /about.html so URLs have no extension.
    format: 'directory',
  },
});
