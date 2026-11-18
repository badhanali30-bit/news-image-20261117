// news-image-20261117 entry (Node 22, standard library only).
// Copies the entry image beside this file to the output directory:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
