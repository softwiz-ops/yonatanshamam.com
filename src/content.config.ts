import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Articles.
 *
 * These sit upstream of the service pages. A service page catches someone who
 * already knows what they need; an article catches the question they typed
 * before they knew. That is the half of the funnel the site currently misses.
 *
 * Every article must link to at least one service page and be linked back from
 * it. On the old WordPress site the demand-letter post and the demand-letter
 * service had no link between them in either direction — the single most
 * obvious thing left on the table there.
 */
const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    /** Page title. Written per article, never templated from the h1. */
    seoTitle: z.string(),
    seoDescription: z.string(),
    /** One or two sentences. Shown in the index and used as the standfirst. */
    summary: z.string(),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    /** Slugs from src/data/services.ts. Renders the internal links. */
    relatedServices: z.array(z.string()).min(1),
    /** Who the piece is written for, mirroring the service audiences. */
    audience: z.enum(['private', 'business', 'both']),
    draft: z.boolean().default(false),
  }),
});

export const collections = { articles };
