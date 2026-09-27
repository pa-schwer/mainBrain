// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // Drives canonical URLs and og:url.
  site: "https://{{DOMAIN}}",

  // Static output. The Worker serves the contents of dist/ and there is no
  // server to run, which is the point of keeping state out of here.
  output: "static",

  build: {
    // Inlining the stylesheet removes the one render-blocking request on
    // the page, which is most of the mobile Lighthouse performance budget.
    inlineStylesheets: "always",
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
