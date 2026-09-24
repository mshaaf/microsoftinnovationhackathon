import { expect, test, type Page, type TestInfo } from "@playwright/test";
import {
  attachScreenAudit,
  captureRequests,
  expectNoRequestContains,
} from "./helpers";

async function checkScreen(
  page: Page,
  testInfo: TestInfo,
  heading: string,
  name: string,
) {
  await expect(page.getByRole("heading", { name: heading })).toBeVisible();
  await attachScreenAudit(page, testInfo, name);
}

test("a survivor can walk through every placeholder stage", async ({ page }, testInfo) => {
  const requests = captureRequests(page);

  await page.goto("/");
  await checkScreen(page, testInfo, "Start with your ZIP code", "help-here");

  await page.getByRole("link", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/apply$/);
  await checkScreen(page, testInfo, "Get ready to apply", "apply");

  await page.getByRole("link", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/letter$/);
  await checkScreen(page, testInfo, "Understand your FEMA letter", "letter");

  await page.getByRole("link", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/deadline$/);
  await checkScreen(page, testInfo, "Know your deadline", "deadline");

  await page.getByRole("link", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/programs$/);
  await checkScreen(page, testInfo, "Other help you may qualify for", "programs");

  await page.getByRole("link", { name: "About" }).first().click();
  await checkScreen(page, testInfo, "About this navigator", "about");

  await page.getByRole("link", { name: "Status" }).click();
  await checkScreen(page, testInfo, "Service status", "status");

  expectNoRequestContains(requests, "Jordan Samplewell");
});
