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
  const browserErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") browserErrors.push(message.text());
  });
  page.on("pageerror", (error) => browserErrors.push(error.message));

  await page.goto("/");
  await checkScreen(page, testInfo, "Start with your ZIP code", "help-here");

  await page.getByLabel("ZIP code").fill("96704");
  await page.getByRole("button", { name: "Check my area" }).click();
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
  expect(browserErrors).toEqual([]);
});

test("S07 journey and chat work in Spanish", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Español" }).click();

  await expect(
    page.getByRole("heading", { name: "Comienza con tu código postal" }),
  ).toBeVisible();
  await page.getByLabel("Código postal").fill("96704");
  await page.getByRole("button", { name: "Revisar mi zona" }).click();
  await expect(page.getByText(/La Asistencia Individual está abierta/)).toBeVisible();
  await page.getByRole("link", { name: "Continuar" }).click();

  await expect(
    page.getByRole("heading", { name: "Prepárate para solicitar ayuda" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Era inquilino" }).click();
  await page.getByRole("button", { name: "No", exact: true }).click();
  await page.getByRole("button", { name: "No", exact: true }).click();
  await page.getByRole("button", { name: "No", exact: true }).click();
  await expect(page.getByText("Tu lista")).toBeVisible();

  await page.getByLabel("Tu pregunta").fill("¿Qué pasa si FEMA cobra cargos?");
  await page.getByRole("button", { name: "Enviar" }).click();
  await expect(page.getByText(/Incluya el número de solicitud de FEMA/)).toBeVisible();
  await expect(page.getByText(/FEMA y las otras agencias toman la decisión final/)).toBeVisible();
  await page.getByRole("link", { name: "Continuar" }).click();

  await expect(
    page.getByRole("heading", { name: "Entiende tu carta de FEMA" }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Continuar" }).click();
  await expect(page.getByRole("heading", { name: "Conoce tu fecha límite" })).toBeVisible();
  await page.getByRole("link", { name: "Continuar" }).click();

  await expect(
    page.getByRole("heading", { name: "Otras ayudas que podrías recibir" }),
  ).toBeVisible();
  await page.getByRole("group", { name: /perdiste trabajo/i }).getByLabel("Sí").check();
  await page.getByRole("group", { name: /recibes SNAP/i }).getByLabel("No").check();
  await page.getByLabel(/personas viven en tu hogar/i).fill("1");
  await page.getByRole("button", { name: "Ver programas" }).click();
  await expect(page.getByRole("article")).toHaveCount(5);
  await expect(page.getByText("Solicite en DisasterAssistance.gov", { exact: false })).toBeVisible();
});
