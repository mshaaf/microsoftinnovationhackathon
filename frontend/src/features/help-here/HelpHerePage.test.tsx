import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import { JourneyProvider, useJourney } from "../../app/JourneyContext";
import { LanguageProvider } from "../../app/LanguageContext";
import declarations from "../../../../contracts/examples/declarations.json";
import location from "../../../../contracts/examples/location.json";
import { HelpHerePage } from "./HelpHerePage";

function Probe() {
  const { journey } = useJourney();
  return <output data-testid="j">{JSON.stringify(journey)}</output>;
}

function setup() {
  render(
    <MemoryRouter>
      <LanguageProvider>
        <JourneyProvider>
          <HelpHerePage />
          <Probe />
        </JourneyProvider>
      </LanguageProvider>
    </MemoryRouter>,
  );
}

const json = (body: unknown, ok = true) =>
  Promise.resolve({ ok, json: () => Promise.resolve(body) } as Response);

function stubLive(handler: (url: string) => Promise<Response>) {
  vi.stubEnv("VITE_APP_MODE", "live");
  const f = vi.fn((url: string) => handler(url));
  vi.stubGlobal("fetch", f);
  return f;
}

async function submit(zip: string) {
  await userEvent.type(screen.getByLabelText("ZIP code"), zip);
  await userEvent.click(screen.getByRole("button", { name: "Check my area" }));
}

afterEach(() => {
  cleanup();
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe("HelpHerePage", () => {
  it("rejects a ZIP that is not 5 digits", async () => {
    setup();
    await submit("9a7");
    expect(screen.getByRole("alert")).toHaveTextContent("Enter a 5-digit ZIP code");
  });

  it("shows the disaster card and Serious Needs callout in mock mode", async () => {
    setup();
    await submit("96704");
    expect(await screen.findByText(/Example Severe Storms/)).toBeInTheDocument();
    expect(screen.getByText(/Declared on September 10, 2026/)).toBeInTheDocument();
    expect(screen.getByText(/Individual Assistance is open/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /FEMA.gov/ })).toHaveAttribute(
      "href",
      "https://www.fema.gov/disaster/9999",
    );
    expect(screen.getByText(/up to \$770/)).toBeInTheDocument();
    expect(screen.getByText(/October 10, 2026. This date may be extended/)).toBeInTheDocument();
    expect(screen.getByText(/not the total help available/)).toBeInTheDocument();
    expect(screen.getByText(/Register with FEMA by November 9, 2026/)).toBeInTheDocument();
    expect(screen.getByTestId("j")).toHaveTextContent('"disasterNumber":"9999"');
    expect(screen.getByTestId("j")).toHaveTextContent('"zipCode":"96704"');
    expect(screen.getByRole("link", { name: "Continue" })).toHaveAttribute("href", "/apply");
  });

  it("shows a loading state", async () => {
    stubLive(() => new Promise(() => {}));
    setup();
    await submit("96704");
    expect(screen.getByText("Checking your area...")).toBeInTheDocument();
  });

  it("shows an error state with a retry", async () => {
    stubLive(() => json({ error: { message: "boom" } }, false));
    setup();
    await submit("96704");
    expect(await screen.findByText(/could not check right now/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
  });

  it("asks which county for a multi-county ZIP (S12)", async () => {
    const two = {
      ...location,
      zip: "39426",
      needs_confirmation: true,
      counties: [
        { state: "MS", county_fips: "28035", name: "Forrest County" },
        { state: "MS", county_fips: "28073", name: "Lamar County" },
      ],
    };
    const f = stubLive((url) =>
      url.startsWith("/api/location") ? json(two) : json(declarations),
    );
    setup();
    await submit("39426");
    await userEvent.click(await screen.findByLabelText("Lamar County, MS"));
    await userEvent.click(screen.getByRole("button", { name: "Continue with this county" }));
    expect(await screen.findByText(/Example Severe Storms/)).toBeInTheDocument();
    const declUrl = f.mock.calls.map((c) => c[0]).find((u) => u.startsWith("/api/declarations"))!;
    expect(declUrl).toContain("county_fips=28073");
    expect(declUrl).toContain("state=MS");
    await waitFor(() =>
      expect(screen.getByTestId("j")).toHaveTextContent("Lamar County"),
    );
  });

  it("shows registration closed", async () => {
    const closed = structuredClone(declarations);
    closed.declarations[0].registration_open = false;
    stubLive((url) => (url.startsWith("/api/location") ? json(location) : json(closed)));
    setup();
    await submit("12345");
    expect(await screen.findByText(/Registration closed on November 9, 2026/)).toBeInTheDocument();
    expect(screen.queryByText(/Register with FEMA by/)).not.toBeInTheDocument();
  });

  it("shows the no-declaration state (S13)", async () => {
    const none = { ...declarations, declarations: [] };
    stubLive((url) => (url.startsWith("/api/location") ? json(location) : json(none)));
    setup();
    await submit("02134");
    expect(await screen.findByText(/No open disaster found/)).toBeInTheDocument();
    expect(screen.getByText(/Call 211/)).toBeInTheDocument();
    expect(screen.getByText(/1-800-621-3362/)).toBeInTheDocument();
  });
});
