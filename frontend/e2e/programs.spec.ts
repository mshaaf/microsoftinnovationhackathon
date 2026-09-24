import { expect, test } from "@playwright/test";

test("S07 sees five program cards in Spanish urgency order", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("ZIP code").fill("96704");
  await page.getByRole("button", { name: "Check my area" }).click();
  await page.getByRole("link", { name: "Continue" }).click();

  await page.getByRole("button", { name: "I rented it" }).click();
  await page.getByRole("button", { name: "No", exact: true }).click();
  await page.getByRole("button", { name: "No", exact: true }).click();
  await page.getByRole("button", { name: "No", exact: true }).click();
  await page.getByRole("link", { name: "Continue" }).click();
  await page.getByRole("link", { name: "Continue" }).click();
  await page.getByRole("link", { name: "Continue" }).click();

  await expect(page).toHaveURL(/\/programs$/);
  await page.getByRole("button", { name: "Español" }).click();
  await page.getByRole("group", { name: /perdiste trabajo/i }).getByLabel("Sí").check();
  await page.getByRole("group", { name: /recibes SNAP/i }).getByLabel("No").check();
  await page.getByLabel(/personas viven en tu hogar/i).fill("1");
  await page.getByRole("button", { name: "Ver programas" }).click();

  const cards = page.getByRole("article");
  await expect(cards).toHaveCount(5);
  for (const [index, tier] of ["check_now", "check_now", "open", "likely", "optional"].entries()) {
    await expect(cards.nth(index).locator("[data-tier]")).toHaveAttribute("data-tier", tier);
  }
  await expect(cards.nth(0)).toContainText("Revisar ahora");
  await expect(cards.nth(1)).toContainText("Revisar ahora");
  await expect(cards.nth(2)).toContainText("Abierto");
  await expect(cards.nth(3)).toContainText("Podría aplicar");
  await expect(cards.nth(4)).toContainText("Opcional");
});
