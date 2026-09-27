import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    // Source maps stay on: this is a dashboard, the bundle is already
    // readable, and a stack trace from a real user's browser is worth more
    // than the obscurity.
    outDir: "dist",
    sourcemap: true,
  },
});
