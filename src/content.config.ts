import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    /** The claim a recruiter can scan in one breath. */
    oneLiner: z.string().max(140),

    /** Honesty gate. If this work sits on top of someone else's engine, say so
     *  here and the upstream URL becomes mandatory below. This is what keeps
     *  the news-radar page truthful without relying on anyone's memory. */
    role: z.enum(['sole author', 'adapted', 'fork + rework']),
    upstream: z.string().url().optional(),

    period: z.string(),
    stack: z.array(z.string()).default([]),
    metrics: z
      .array(z.object({ label: z.string(), value: z.string(), note: z.string().optional() }))
      .default([]),

    repo: z.string().url().optional(),
    repoStatus: z.enum(['private', 'open-source', 'sanitized-fork', 'architecture-only']),

    artifact: z
      .object({
        path: z.string(),
        title: z.string(),
        allow: z.string().optional(),
        caption: z.string().optional(),
      })
      .optional(),

    /** 'planned' entries appear in the index but generate no page. */
    status: z.enum(['published', 'planned']).default('planned'),
    order: z.number(),

    /** HARD GATE. A file copied in without going through review has no
     *  `sanitized` field, so `astro build` fails, so Cloudflare never
     *  deploys it. This is a build error, not a lint warning. */
    sanitized: z.literal(true),
    reviewed: z.coerce.date(),
  })
    .refine((d) => d.role === 'sole author' || !!d.upstream, {
      message: 'role is an adaptation, so `upstream` (the original project URL) is required',
      path: ['upstream'],
    }),
});

export const collections = { projects };
