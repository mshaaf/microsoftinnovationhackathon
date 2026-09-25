import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import { JourneyProvider } from "../../app/JourneyContext";
import { LanguageToggle } from "../../app/LanguageToggle";
import { LanguageProvider } from "../../app/LanguageContext";
import * as client from "../../shared/api/client";
import { ApplyPage } from "./ApplyPage";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function setup() {
  render(
    <MemoryRouter>
      <LanguageProvider>
        <JourneyProvider>
          <LanguageToggle />
          <ApplyPage />
        </JourneyProvider>
      </LanguageProvider>
    </MemoryRouter>,
  );
  return userEvent.setup();
}

async function answerAll(user: ReturnType<typeof userEvent.setup>) {
  await user.click(screen.getByRole("button", { name: "I rented it" }));
  await user.click(screen.getByRole("button", { name: "Not sure" }));
  await user.click(screen.getByRole("button", { name: "Yes" }));
  await user.click(screen.getByRole("button", { name: "Yes" }));
}

describe("apply questions", () => {
  it("asks one question at a time and can go back", async () => {
    const user = setup();
    expect(screen.getByText("Did you own or rent your home?")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "I owned it" }));
    expect(screen.getByText("Did you have insurance on it?")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Back" }));
    expect(screen.getByText("Did you own or rent your home?")).toBeInTheDocument();
  });

  it("shows the checklist with why and source link", async () => {
    const spy = vi.spyOn(client, "apiRequest");
    const user = setup();
    await answerAll(user);
    expect(await screen.findByText(/lived there/)).toBeInTheDocument();
    expect(screen.getByText(/FEMA needs to confirm/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Learn more" })).toHaveAttribute(
      "href",
      expect.stringContaining("fema.gov"),
    );
    const body = JSON.parse(spy.mock.calls[0][1]?.body as string);
    expect(body.answers).toEqual({ housing: "rent", insured: "not_sure", lost_id: true, displaced: true });
    expect(body.disaster_number).toBe(9999);
  });

  it("shows an error with a retry", async () => {
    vi.spyOn(client, "apiRequest").mockRejectedValueOnce(new Error("x"));
    const user = setup();
    await answerAll(user);
    expect(await screen.findByRole("alert")).toHaveTextContent("Check your connection");
    await user.click(screen.getByRole("button", { name: "Try again" }));
    expect(await screen.findByText(/lived there/)).toBeInTheDocument();
  });

  it("shows an empty state", async () => {
    vi.spyOn(client, "apiRequest").mockResolvedValueOnce({ request_id: "r", rules_regime: "x", items: [] } as never);
    const user = setup();
    await answerAll(user);
    expect(await screen.findByText(/no items for you yet/)).toBeInTheDocument();
  });
});

describe("chat panel", () => {
  it("shows a reply with citation links", async () => {
    const user = setup();
    await user.type(screen.getByLabelText("Your question"), "What if I lost my ID?");
    await user.click(screen.getByRole("button", { name: "Send" }));
    expect(await screen.findByText(/FEMA makes the decision/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Verify identity/ })).toHaveAttribute("href", expect.stringContaining("fema.gov"));
  });

  it("loads a handoff card when chat returns a handoff reason", async () => {
    const request = vi.spyOn(client, "apiRequest");
    request.mockResolvedValueOnce({
      request_id: "r",
      reply: "Please call.",
      citations: [],
      handoff: "emergency",
    } as never).mockResolvedValueOnce({
      request_id: "r2",
      card: {
        title: "Get help now",
        steps: ["Call 911."],
        phones: [{ label: "Emergency", number: "911" }],
      },
    } as never);
    const user = setup();
    await user.type(screen.getByLabelText("Your question"), "help");
    await user.click(screen.getByRole("button", { name: "Send" }));
    expect(await screen.findByRole("heading", { name: "Get help now" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Emergency/ })).toHaveAttribute("href", "tel:911");
    expect(request.mock.calls.map(([path]) => path)).toEqual(["/api/chat", "/api/escalate"]);
  });

  it("works in Spanish", async () => {
    const user = setup();
    await user.click(screen.getByRole("button", { name: /espa/i }));
    expect(screen.getByText("¿Eras dueño o inquilino de tu casa?")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Haz una pregunta" })).toBeInTheDocument();
  });

  it("keeps chat text out of storage", async () => {
    const user = setup();
    await user.type(screen.getByLabelText("Your question"), "secret text");
    await user.click(screen.getByRole("button", { name: "Send" }));
    await screen.findByText(/FEMA makes the decision/);
    expect(JSON.stringify(localStorage) + JSON.stringify(sessionStorage)).not.toContain("secret");
  });
});
