import { expect, test } from "@playwright/test";

test("stage 1 happy path in mock mode", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("ZIP code").fill("12ab");
  await page.getByRole("button", { name: "Check my area" }).click();
  await expect(page.getByRole("alert")).toContainText("5-digit ZIP");

  await page.getByLabel("ZIP code").fill("96704");
  await page.getByRole("button", { name: "Check my area" }).click();
  await expect(page.getByRole("heading", { name: /Disaster 4936: EARTHQUAKE/i })).toBeVisible();
  await expect(page.getByText(/Individual Assistance is open in Hawaii County/)).toBeVisible();
  await expect(page.getByText(/Apply by October 1, 2026.*may be extended/)).toBeVisible();
  await expect(page.getByText(/not the total help available/)).toBeVisible();
  await expect(page).toHaveURL(/\/$/); // no ZIP in the URL

  await page.getByRole("link", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/apply$/);
});

test("multi-county ZIP asks the survivor to choose", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("ZIP code").fill("39426");
  await page.getByRole("button", { name: "Check my area" }).click();

  await expect(page.getByText(/covers more than one county/)).toBeVisible();
  await expect(page.getByRole("radio")).toHaveCount(2);
  await page.getByRole("radio").last().check();
  await page.getByRole("button", { name: "Continue with this county" }).click();
  await expect(page.getByRole("heading", { name: /Disaster/ })).toBeVisible();
});

test("ZIP without an active declaration shows other help", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("ZIP code").fill("02134");
  await page.getByRole("button", { name: "Check my area" }).click();

  await expect(page.getByRole("heading", { name: /No open disaster found/ })).toBeVisible();
  await expect(page.getByText(/Call 211/)).toBeVisible();
  await expect(page.getByText(/FEMA Helpline at 1-800-621-3362/)).toBeVisible();
});
