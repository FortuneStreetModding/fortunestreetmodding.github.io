import { defineConfig } from "@solidjs/start/config";
/* @ts-ignore */
import pkg from "@vinxi/plugin-mdx";
import fsp from "node:fs/promises";
import { join } from "pathe";

const { default: mdx } = pkg;
export default defineConfig({
  extensions: ["mdx", "md"],
  vite: {
    plugins: [
      mdx.withImports({})({
        jsx: true,
        jsxImportSource: "solid-js",
        providerImportSource: "solid-mdx"
      })
    ]
  },
  server: {
    extends: "static",
    commands: {
      deploy: "bun gh-pages --dotfiles -d ./public",
    },
    prerender: {
      routes: [
        "/",
        // https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site
        "/404.html",
      ],
      crawlLinks: true
    },
    hooks: {
      async compiled(nitro) {
        await fsp.writeFile(
          join(nitro.options.output.publicDir, ".nojekyll"),
          ""
        );
      },
    }
  },
  ssr: true,
  appRoot: 'src'
});
