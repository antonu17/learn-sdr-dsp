import { cp, mkdir } from 'node:fs/promises';
await mkdir('public/labs',{recursive:true});
await cp('labs','public/labs',{recursive:true,filter:src=>!/(^|\/)(\.venv|__pycache__|\.DS_Store)(\/|$)/.test(src)});
