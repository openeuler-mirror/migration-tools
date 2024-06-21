import { fileURLToPath, URL } from "url";
import { viteSingleFile } from "vite-plugin-singlefile";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
// https://github.com/richardtallent/vite-plugin-singlefile
export default defineConfig({
  plugins: [vue(), viteSingleFile()],
  build: {
    cssCodeSplit: false,
    brotliSize: false,
    assetsInlineLimit: 100000000,
    chunkSizeWarningLimit: 100000000,
    rollupOptions: {
      inlineDynamicImports: true,
      input: {
        rc: resolve(__dirname, "index.html"),
        ra: resolve(__dirname, "ra/index.html"),
        ec: resolve(__dirname, "ec/index.html"),
      },
      output: {
        manualChunks: () => "everything.js",
      },
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
