import { defineConfig } from 'astro/config';

import solidJs from "@astrojs/solid-js";
import yaml from '@rollup/plugin-yaml';


// https://astro.build/config
export default defineConfig({
  integrations: [solidJs()],
  vite: {
    plugins: [yaml()]
  }
});