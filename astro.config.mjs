import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
export default defineConfig({integrations:[mdx()],markdown:{processor:unified({remarkPlugins:[remarkMath],rehypePlugins:[rehypeKatex]}),shikiConfig:{theme:'github-dark'}},server:{host:'127.0.0.1'}});
