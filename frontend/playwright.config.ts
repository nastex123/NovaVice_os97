import { defineConfig } from "@playwright/test";
// Visual snapshot testing for retro desktop (TODO-4.5).
export default defineConfig({
  testDir: "./e2e",
  snapshotPathTemplate: "./e2e/__snapshots__/{testFilePath}/{arg}{ext}",
  use: { baseURL: "http://localhost:3000", screenshot: "only-on-failure" },
});
