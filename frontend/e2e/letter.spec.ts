import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { captureRequests, expectNoRequestContains } from "./helpers";

const l03 = JSON.parse(readFileSync(new URL("../../fixtures/letters/L03.expected.json", import.meta.url), "utf8")) as { fake_pii: string[] };

test("letter draft fields stay in the browser", async ({ page }) => {
  const requests = captureRequests(page);
  await page.goto("/letter");
  await expect(page.getByRole("heading", { name: "Understand your FEMA letter" })).toBeVisible();
  const decode = page.waitForResponse((response) => response.url().endsWith("/api/letter/decode"));
  await page.getByLabel("Choose a letter").setInputFiles(fileURLToPath(new URL("../../fixtures/letters/L03.png", import.meta.url)));
  expect((await decode).status()).toBe(200);
  const preview = page.getByLabel("Redacted preview");
  await expect(preview).toBeVisible();
  for (const fakePii of l03.fake_pii) await expect(preview).not.toContainText(fakePii);
  await expect(page.getByLabel("Appeal draft")).toBeVisible();
  await page.getByLabel("Your name (optional)").fill("Jordan Private Name");
  await page.getByLabel("FEMA registration number (optional)").fill("123456789");
  await expect(page.getByLabel("Appeal draft")).toHaveValue(/Jordan Private Name/);
  await page.getByRole("button", { name: "Copy draft" }).click();
  expectNoRequestContains(requests, "Jordan Private Name");
  expectNoRequestContains(requests, "123456789");
});
