import { expect, test } from "@playwright/test";
import { attachScreenAudit } from "./helpers";

test("axe audit rejects a serious violation", async ({ page }, testInfo) => {
  await page.setContent(`
    <!doctype html>
    <html lang="en">
      <head><title>Accessibility gate fixture</title></head>
      <body><main><button></button></main></body>
    </html>
  `);

  let failure: unknown;
  try {
    await attachScreenAudit(page, testInfo, "intentional-axe-violation");
  } catch (error) {
    failure = error;
  }

  expect(failure).toBeInstanceOf(Error);
  expect(String(failure)).toContain("[axe] intentional-axe-violation");
  expect(String(failure)).toContain("button-name");
});
