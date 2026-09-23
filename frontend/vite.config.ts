import { defineConfig } from "vitest/config";

const apiPort = process.env.API_PORT ?? "8000";

export default defineConfig({
  server: {
    port: Number(process.env.WEB_PORT ?? "5173"),
    proxy: {
      "/api": `http://127.0.0.1:${apiPort}`,
    },
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"],
  },
});
