import { defineMiddleware } from 'astro:middleware';
import gone from '../gone.json';

/**
 * Serve 410 Gone for the WordPress template junk.
 *
 * Nineteen of the ~22 URLs in the live sitemap were never meant to be public:
 * WordPress boilerplate, six demo pages carrying English lorem ipsum, four
 * fabricated testimonial pages dated 2014, and five theme footer fragments.
 *
 * 410 rather than 301 because there is nowhere honest to send them. A redirect
 * to the home page is a soft-404, which Google eventually treats as a 404
 * anyway — except it spends crawl budget rediscovering it first. 410 says the
 * URL is deliberately gone and gets it dropped faster.
 *
 * This cannot live in astro.config's `redirects`: that only accepts
 * 301/302/303/307/308, and 410 is not a redirect at all.
 */
const GONE = new Set(gone as string[]);

/** Compare with and without the trailing slash, and decoded. */
function isGone(pathname: string): boolean {
  const decoded = decodeURIComponent(pathname);
  const withSlash = decoded.endsWith('/') ? decoded : `${decoded}/`;
  return GONE.has(decoded) || GONE.has(withSlash);
}

export const onRequest = defineMiddleware(async (context, next) => {
  if (isGone(context.url.pathname)) {
    return new Response(
      '<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">' +
        '<title>הדף הוסר</title><meta name="robots" content="noindex"></head>' +
        '<body><h1>הדף הוסר</h1>' +
        '<p>הדף הזה הוסר מהאתר ולא יוחזר. ' +
        '<a href="/">לעמוד הראשי</a></p></body></html>',
      {
        status: 410,
        headers: { 'content-type': 'text/html; charset=utf-8' },
      }
    );
  }
  return next();
});
