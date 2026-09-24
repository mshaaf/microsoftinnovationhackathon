import { expect, test } from "@playwright/test";

test("renter, not sure, lost ID shows checklist and a chat link", async ({ page }) => {
  await page.goto("/apply");
  await page.getByRole("button", { name: "I rented it" }).click();
  await page.getByRole("button", { name: "Not sure" }).click();
  await page.getByRole("button", { name: "Yes" }).click();
  await page.getByRole("button", { name: "Yes" }).click();
  await expect(page.getByRole("link", { name: "Learn more" }).first()).toBeVisible();

  await page.getByLabel("Your question").fill("What if I lost my ID?");
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.getByRole("link", { name: /Verify identity/ })).toBeVisible();
});
