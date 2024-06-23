import { defineConfig } from 'astro/config';

import yaml from '@rollup/plugin-yaml';

// https://astro.build/config
export default defineConfig({
  site: 'https://fortunestreetmodding.github.io/',
  build: {
    format: 'file'
  },
  vite: {
    plugins: [
      yaml()
    ]
  }
});