/**
 * Work-in-progress mode.
 *
 * While true:
 *   - `/` serves a holding page; the finished homepage lives at `/index-full/`
 *   - every page is marked noindex/nofollow
 *   - the header navigation is hidden, so nothing links onward from the
 *     holding page
 *   - no sitemap is generated, since a sitemap is a public directory of
 *     exactly the URLs that should not be browsable yet
 *
 * The case-study pages are still SERVED — a link you send by hand works. They
 * are unlisted, not protected. Anyone who is given a URL, or who guesses one,
 * can read it. If they ever need to be genuinely private, that is Cloudflare
 * Access, not this flag.
 *
 * To relaunch: set this to false, move index-full.astro back to index.astro,
 * and re-enable the sitemap integration in astro.config.mjs.
 */
export const WIP = true;
