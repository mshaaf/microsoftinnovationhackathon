import AxeBuilder from "@axe-core/playwright";
import { expect, type Page, type TestInfo } from "@playwright/test";

const axeTags = ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"];

export async function attachScreenAudit(
  page: Page,
  testInfo: TestInfo,
  name: string,
) {
  const results = await new AxeBuilder({ page }).withTags(axeTags).analyze();
  const serious = results.violations.filter((violation) =>
    ["critical", "serious"].includes(violation.impact ?? ""),
  );

  await testInfo.attach(`${name}-axe`, {
    body: JSON.stringify(results.violations, null, 2),
    contentType: "application/json",
  });
  await testInfo.attach(`${name}-screenshot`, {
    body: await page.screenshot({ fullPage: true }),
    contentType: "image/png",
  });

  expect(serious, `[axe] ${name}: critical/serious accessibility violations`).toEqual([]);
}

export function captureRequests(page: Page) {
  const requests: string[] = [];

  page.on("request", (request) => {
    requests.push(
      [request.method(), request.url(), request.postData() ?? ""].join("\n"),
    );
  });

  return requests;
}

export function expectNoRequestContains(requests: string[], sensitiveText: string) {
  for (const request of requests) {
    expect(request).not.toContain(sensitiveText);
  }
}
