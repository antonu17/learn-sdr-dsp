import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
const course = defineCollection({loader:glob({pattern:'**/*.mdx',base:'./src/content/course'}),schema:z.object({title:z.string(),description:z.string(),order:z.number(),kind:z.enum(['lesson','roadmap']),part:z.number()})});
export const collections = {course};
