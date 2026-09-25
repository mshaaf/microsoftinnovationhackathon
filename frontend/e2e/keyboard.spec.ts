import { expect, test, type Locator, type Page } from "@playwright/test";
import { attachScreenAudit } from "./helpers";

async function tabTo(page: Page, target: Locator) {
  for (let i = 0; i < 80; i += 1) {
    if (await target.evaluate((element) => element === document.activeElement)) return;
    await page.keyboard.press("Tab");
  }
  throw new Error("Keyboard tab order did not reach the requested control");
}

async function expectKeyboardFocus(target: Locator, hitArea = target) {
  const style = await target.evaluate((element) => {
    const computed = getComputedStyle(element);
    return {
      outlineStyle: computed.outlineStyle,
      outlineWidth: Number.parseFloat(computed.outlineWidth),
    };
  });
  const { width, height } = await hitArea.evaluate((element) => {
    const rect = element.getBoundingClientRect();
    return { width: rect.width, height: rect.height };
  });
  expect(style.outlineStyle).not.toBe("none");
  expect(style.outlineWidth).toBeGreaterThanOrEqual(2);
  expect(width).toBeGreaterThanOrEqual(44);
  expect(height).toBeGreaterThanOrEqual(44);
}

async function activate(page: Page, target: Locator) {
  await tabTo(page, target);
  await expectKeyboardFocus(target);
  await page.keyboard.press("Enter");
}

async function expectOnePageHeading(page: Page) {
  await expect(page.getByRole("heading", { level: 1 })).toHaveCount(1);
  const { contentWidth, viewportWidth } = await page.evaluate(() => ({
    contentWidth: document.documentElement.scrollWidth,
    viewportWidth: window.innerWidth,
  }));
  expect(contentWidth).toBeLessThanOrEqual(viewportWidth);
}

test("survivor can reach the next stages with keyboard only", async ({ page }, testInfo) => {
  await page.goto("/");
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-start");

  const zip = page.getByLabel("ZIP code");
  await tabTo(page, zip);
  await page.keyboard.insertText("96704");
  await activate(page, page.getByRole("button", { name: "Check my area" }));
  await expect(page.getByRole("heading", { name: /Disaster 4936:/ })).toBeVisible();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-declaration");

  await activate(page, page.getByRole("link", { name: "Continue", exact: true }));
  await expect(page).toHaveURL(/\/apply$/);
  await expectOnePageHeading(page);

  for (const answer of ["I rented it", "Not sure", "Yes", "Yes"]) {
    await activate(page, page.getByRole("button", { name: answer, exact: true }));
  }
  await expect(page.getByText(/lease or a utility bill/)).toBeVisible();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-checklist");

  const question = page.getByLabel("Your question");
  await tabTo(page, question);
  await expectKeyboardFocus(question);
  await page.keyboard.insertText("Where can I apply for help?");
  const chatResponse = page.waitForResponse((response) =>
    response.url().endsWith("/api/chat") && response.request().method() === "POST",
  );
  await activate(page, page.getByRole("button", { name: "Send", exact: true }));
  expect((await chatResponse).ok()).toBeTruthy();
  await expect(page.locator('[aria-live="polite"]')).not.toBeEmpty();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-chat-reply");

  await activate(page, page.getByRole("link", { name: "Continue", exact: true }));
  await expect(page.getByRole("heading", { name: "Understand your FEMA letter" })).toBeVisible();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-letter");

  await tabTo(page, page.getByLabel("Choose a letter"));
  await expectKeyboardFocus(page.getByLabel("Choose a letter"));

  await activate(page, page.getByRole("link", { name: "Continue", exact: true }));
  await expect(page.getByRole("heading", { name: "Know your deadline" })).toBeVisible();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-deadline");

  await activate(page, page.getByRole("link", { name: "Continue", exact: true }));
  await expect(page.getByRole("heading", { name: "Other help you may qualify for" })).toBeVisible();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-program-questions");

  const programRadios = page.getByRole("radio");
  const lostWorkYes = programRadios.nth(0);
  await tabTo(page, lostWorkYes);
  await expectKeyboardFocus(lostWorkYes, lostWorkYes.locator("xpath=.."));
  await page.keyboard.press("Space");
  await expect(lostWorkYes).toBeChecked();

  const snapYes = programRadios.nth(2);
  await tabTo(page, snapYes);
  await expectKeyboardFocus(snapYes, snapYes.locator("xpath=.."));
  await page.keyboard.press("Space");
  await page.keyboard.press("ArrowRight");
  await expect(programRadios.nth(3)).toBeChecked();

  const household = page.getByLabel("How many people are in your household?");
  await tabTo(page, household);
  await expectKeyboardFocus(household);
  await page.keyboard.insertText("3");
  await activate(page, page.getByRole("button", { name: "See programs" }));
  await expect(page.getByRole("article").first()).toBeVisible();
  await expectOnePageHeading(page);
  await attachScreenAudit(page, testInfo, "keyboard-program-results");
});
