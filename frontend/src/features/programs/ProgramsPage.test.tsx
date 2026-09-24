import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useEffect, useRef } from "react";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";
import { JourneyProvider, useJourney } from "../../app/JourneyContext";
import { LanguageProvider } from "../../app/LanguageContext";
import { LanguageToggle } from "../../app/LanguageToggle";
import * as client from "../../shared/api/client";
import type { ApiResponse } from "../../shared/api/client";
import { ProgramsPage } from "./ProgramsPage";

type ApiCard = ApiResponse<"/api/programs">["cards"][number];
type TestCard = Omit<ApiCard, "deadline"> & { deadline: ApiCard["deadline"] | null };
const cards: TestCard[] = (
  [
    ["sba_loan", "optional"],
    ["irs_relief", "likely"],
    ["fema_ihp", "open"],
    ["dua", "check_now"],
  ] as const
).map(([program_id, tier]) => ({
  program_id,
  tier,
  title: program_id,
  why: "Why this may help.",
  deadline: program_id === "fema_ihp" ? { date: "2026-11-09", label: "Apply by" } : null,
  how_to_apply: "Apply online.",
  source_url: "https://example.gov/",
  last_verified: "2026-09-23",
}));
const location = {
  request_id: "r1",
  zip: "96704",
  counties: [{ state: "HI", county_fips: "15001", name: "Hawaii County" }],
  needs_confirmation: false,
};

function SeedJourney() {
  const { updateJourney } = useJourney();
  const seeded = useRef(false);
  useEffect(() => {
    if (seeded.current) return;
    seeded.current = true;
    updateJourney({ zipCode: "96704", county: "Hawaii County", disasterNumber: "4936", answers: { housing: "rent" } });
  }, [updateJourney]);
  return <><LanguageToggle /><ProgramsPage /></>;
}

function setup() {
  render(<MemoryRouter><LanguageProvider><JourneyProvider><SeedJourney /></JourneyProvider></LanguageProvider></MemoryRouter>);
  return userEvent.setup();
}

function mockResponse(localized = false) {
  const api = vi.spyOn(client, "apiRequest");
  api.mockResolvedValueOnce(location as never).mockResolvedValueOnce({
    request_id: "r2",
    cards: cards.map((card) => ({
      ...card,
      title: localized ? `ES ${card.title}` : card.title,
      deadline: card.deadline && localized ? { ...card.deadline, label: "Solicítelo antes del" } : card.deadline,
    })),
  } as never);
  return api;
}

async function answerForm(user: ReturnType<typeof userEvent.setup>, language: "en" | "es" = "en", lostWork?: string) {
  const spanish = language === "es";
  if (spanish) await user.click(screen.getByRole("button", { name: "Español" }));
  const groups = spanish
    ? [/perdiste trabajo/i, /recibes SNAP/i]
    : [/lose work/i, /receiving SNAP/i];
  const yes = spanish ? "Sí" : "Yes";
  const no = spanish ? "No" : "No";
  await user.click(within(screen.getByRole("group", { name: groups[0] })).getByLabelText(lostWork ?? yes));
  await user.click(within(screen.getByRole("group", { name: groups[1] })).getByLabelText(no));
  const household = screen.getByLabelText(spanish ? /personas viven en tu hogar/i : /people are in your household/i);
  await user.type(household, "1");
  await user.click(screen.getByRole("button", { name: spanish ? "Ver programas" : "See programs" }));
}

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("program cards", () => {
  it("sorts all tiers by urgency and submits the S07 answers", async () => {
    const api = mockResponse();
    await answerForm(setup());
    const articles = await screen.findAllByRole("article");
    expect(articles.map((article) => article.querySelector("[data-tier]")?.getAttribute("data-tier"))).toEqual([
      "check_now", "open", "likely", "optional",
    ]);
    for (const [index, label] of ["Check now", "Open", "May apply", "Optional"].entries()) {
      expect(articles[index]).toHaveTextContent(label);
    }
    expect(articles[0]).toHaveTextContent("No exact date confirmed. The window may be short, so check now.");
    expect(articles[1]).toHaveTextContent("Apply by: November 9, 2026");
    expect(articles[0]).toHaveTextContent("How to apply: Apply online.");
    expect(articles[0]).toHaveTextContent("Last verified: September 23, 2026");
    expect(within(articles[0]).getByRole("link", { name: "Official source" })).toHaveAttribute("href", "https://example.gov/");
    expect(JSON.parse(api.mock.calls[1][1]?.body as string)).toEqual({
      disaster_number: 4936,
      county_fips: "15001",
      lang: "en",
      answers: { housing: "rent", lost_work_or_self_employed: true, on_snap: false, household_size: 1 },
    });
  });

  it("shows Spanish questions and tier and date labels", async () => {
    const api = mockResponse(true);
    await answerForm(setup(), "es");
    const articles = await screen.findAllByRole("article");
    expect(articles.map((article) => article.querySelector("[data-tier]")?.getAttribute("data-tier"))).toEqual([
      "check_now", "open", "likely", "optional",
    ]);
    for (const [index, label] of ["Revisar ahora", "Abierto", "Podría aplicar", "Opcional"].entries()) {
      expect(articles[index]).toHaveTextContent(label);
    }
    expect(articles[0]).toHaveTextContent("No hay una fecha exacta confirmada. El plazo puede ser corto, así que consulta ahora.");
    expect(articles[1]).toHaveTextContent("Solicítelo antes del:");
    expect(articles[1]).toHaveTextContent("Cómo solicitar: Apply online.");
    expect(articles[1]).toHaveTextContent("Verificado: 23 de septiembre de 2026");
    expect(JSON.parse(api.mock.calls[1][1]?.body as string).lang).toBe("es");
  });

  it("offers a retry after a lookup error", async () => {
    const api = vi.spyOn(client, "apiRequest");
    api.mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce(location as never)
      .mockResolvedValueOnce({ request_id: "r2", cards } as never);
    await answerForm(setup(), "en", "No");
    expect(await screen.findByRole("alert")).toHaveTextContent(/could not load/i);
    await userEvent.setup().click(screen.getByRole("button", { name: "Try again" }));
    expect(await screen.findAllByRole("article")).toHaveLength(4);
  });
});
