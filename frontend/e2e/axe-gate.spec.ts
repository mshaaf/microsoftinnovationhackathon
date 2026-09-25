import { expect, test } from "@playwright/test";
import { attachScreenAudit } from "./helpers";

test("axe audit rejects a serious violation", async ({ page }, testInfo) => {
  await page.setContent("<button></button>");

  let failure: unknown;
  try {
    await attachScreenAudit(page, testInfo, "intentional-axe-violation");
  } catch (error) {
    failure = error;
  }

  expect(failure).toBeInstanceOf(Error);
  expect(String(failure)).toContain("[axe] intentional-axe-violation");
});
