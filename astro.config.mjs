// @ts-check
import { defineConfig, sessionDrivers } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import cloudflare from '@astrojs/cloudflare';
import redirects from './redirects.json' with { type: 'json' };

export default defineConfig({
  // Non-www, matching the canonical the live WordPress site already serves on
  // every page. The rankings such as they are sit on this host; do not flip it
  // to www without a full redirect plan.
  site: 'https://yonatanshamam.com',

  // Static by default. The adapter exists solely so the contact endpoint can
  // run on demand — everything else prerenders.
  //
  // imageService: 'compile' keeps sharp on the build machine. sharp does not
  // run on the Workers runtime, and every page using an image is prerendered,
  // so nothing needs to resize at request time.
  adapter: cloudflare({ imageService: 'compile' }),

  // Nothing here uses sessions. Left unset, the Cloudflare adapter assumes
  // KV-backed sessions and emits a SESSION binding with no namespace id, which
  // fails the deploy until an unused KV namespace exists.
  session: { driver: sessionDrivers.memory() },

  trailingSlash: 'always',
  build: { format: 'directory' },

  // Hebrew only. No i18n block on purpose: a machine-translated legal site is
  // both an SEO liability and, per the Bar's advertising rules, a risk to the
  // dignity of the profession. If English is ever needed it gets hand-written
  // pages, not a translation layer.

  // 301s for every URL that changed in the move off WordPress, plus the 410s
  // for the template junk. Regenerate with: python3 scripts/build-redirects.py
  redirects,

  integrations: [
    sitemap({
      // Redirect sources must not appear in the sitemap — they are not
      // destinations, and listing them invites the old URLs to be re-indexed.
      filter: (page) => {
        const path = decodeURIComponent(new URL(page).pathname);
        return !Object.keys(redirects).includes(path);
      },
    }),
  ],
});
