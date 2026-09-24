import { defineConfig } from "@playwright/test";

const apiPort = process.env.SMOKE_API_PORT ?? "8100";
const webPort = process.env.SMOKE_WEB_PORT ?? "5273";
const baseURL = `http://127.0.0.1:${webPort}`;

export default defineConfig({
  testDir: "./e2e",
  outputDir: "./test-results",
  timeout: 60_000,
  workers: 1,
  reporter: [
    ["list"],
    ["html", { open: "never", outputFolder: "playwright-report" }],
  ],
  use: {
    baseURL,
    browserName: "chromium",
    viewport: { width: 360, height: 800 },
    trace: "retain-on-failure",
  },
  webServer: {
    command: `cd .. && APP_MODE=mock API_PORT=${apiPort} WEB_PORT=${webPort} bash scripts/dev.sh`,
    url: baseURL,
    reuseExistingServer: false,
    timeout: 120_000,
  },
});
