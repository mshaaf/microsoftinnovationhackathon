import { expect, test } from "@playwright/test";

test("stage 1 happy path in mock mode", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("ZIP code").fill("12ab");
  await page.getByRole("button", { name: "Check my area" }).click();
  await expect(page.getByRole("alert")).toContainText("5-digit ZIP");

  await page.getByLabel("ZIP code").fill("96704");
  await page.getByRole("button", { name: "Check my area" }).click();
  await expect(page.getByRole("heading", { name: /Example Severe Storms/ })).toBeVisible();
  await expect(page.getByText(/not the total help available/)).toBeVisible();
  await expect(page).toHaveURL(/\/$/); // no ZIP in the URL

  await page.getByRole("link", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/apply$/);
});
