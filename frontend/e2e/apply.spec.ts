import { expect, test } from "@playwright/test";

test("renter, not sure, lost ID shows checklist and a chat link", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("ZIP code").fill("96704");
  await page.getByRole("button", { name: "Check my area" }).click();
  await page.getByRole("link", { name: "Continue" }).click();
  await page.getByRole("button", { name: "I rented it" }).click();
  await page.getByRole("button", { name: "Not sure" }).click();
  await page.getByRole("button", { name: "Yes" }).click();
  await page.getByRole("button", { name: "Yes" }).click();
  await expect(page.getByText(/lease or a utility bill/)).toBeVisible();
  await expect(page.getByText(/insurance settlement or denial letter/)).toBeVisible();
  await expect(page.getByText(/identity document/)).toBeVisible();
  await expect(page.getByRole("link", { name: "Learn more" })).toHaveCount(4);

  for (const question of [
    "What can I send if I lost my ID?",
    "I rent and do not know whether my insurance covers this. What should I do?",
    "Where can I apply for help?",
    "Can you promise I will get money?",
  ]) {
    await page.getByLabel("Your question").fill(question);
    const responsePromise = page.waitForResponse((response) =>
      response.url().endsWith("/api/chat") && response.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Send" }).click();
    const response = await responsePromise;
    expect(response.ok()).toBeTruthy();
    const body = (await response.json()) as {
      reply: string;
      citations: { title: string; url: string }[];
    };
    expect(body.citations.length).toBeGreaterThan(0);
    expect(body.reply).toContain("FEMA and the other agencies make the final decision");
    await expect(page.getByText(body.reply, { exact: true })).toBeVisible();
    for (const citation of body.citations) {
      expect(citation.url).toMatch(/^https:\/\/(www\.fema\.gov|www\.disasterassistance\.gov)\//);
      await expect(page.getByRole("link", { name: citation.title, exact: true })).toHaveAttribute(
        "href",
        citation.url,
      );
    }
  }
  await expect(page.getByText(/No one can promise you will get money/)).toBeVisible();
});
