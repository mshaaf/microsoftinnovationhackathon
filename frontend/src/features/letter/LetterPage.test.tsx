import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";
import { LanguageProvider } from "../../app/LanguageContext";
import { LanguageToggle } from "../../app/LanguageToggle";
import * as client from "../../shared/api/client";
import { LetterPage } from "./LetterPage";

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

function setup() {
  render(<MemoryRouter><LanguageProvider><LanguageToggle /><LetterPage /></LanguageProvider></MemoryRouter>);
  return userEvent.setup();
}

async function upload(user: ReturnType<typeof userEvent.setup>) {
  await user.upload(screen.getByLabelText("Choose a letter"), new File(["sample"], "L03.jpg", { type: "image/jpeg" }));
}

it("can continue to the deadline step without uploading a letter", () => {
  setup();
  expect(screen.getByRole("link", { name: "Continue" })).toHaveAttribute("href", "/deadline");
});

it("offers camera and file input, then shows the contract result and local draft", async () => {
  const user = setup();
  expect(screen.getByLabelText("Take a photo")).toHaveAttribute("capture", "environment");
  await upload(user);
  expect(await screen.findByText("What we removed")).toBeInTheDocument();
  expect(screen.getByText("7 personal details removed")).toBeInTheDocument();
  expect(screen.getByText("Person, Address, Phone number, Other")).toBeInTheDocument();
  expect(screen.getByText(/final insurance decision/)).toBeInTheDocument();
  expect(screen.getByText(/Send the final decision/)).toBeInTheDocument();
  expect(screen.getByText("October 31, 2026")).toBeInTheDocument();
  expect(screen.getByText(/38 days left/)).toBeInTheDocument();
  await user.type(screen.getByLabelText("Your name (optional)"), "Jordan Lee");
  await user.type(screen.getByLabelText("FEMA registration number (optional)"), "123456789");
  expect((screen.getByLabelText("Appeal draft") as HTMLTextAreaElement).value).toContain("Jordan Lee");
  expect((screen.getByLabelText("Appeal draft") as HTMLTextAreaElement).value).toContain("123456789");
  expect(screen.getByRole("button", { name: "Copy draft" })).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Print draft" })).toBeInTheDocument();
  expect(JSON.stringify(localStorage) + JSON.stringify(sessionStorage)).not.toContain("Jordan Lee");
});

it("shows progress in order and offers retry after an error", async () => {
  let resolve!: (value: never) => void;
  vi.spyOn(client, "apiRequest").mockImplementationOnce(() => new Promise((r) => { resolve = r; }));
  const user = setup();
  await upload(user);
  expect(screen.getByRole("status")).toHaveTextContent("Reading your letter");
  resolve((await import("../../../../contracts/examples/letter-decode.json")).default as never);
  expect(await screen.findByText("Removing personal details...")).toBeInTheDocument();
  expect(await screen.findByText("Explaining the decision...")).toBeInTheDocument();
  await screen.findByText("What we removed");
  const spy = vi.spyOn(client, "apiRequest").mockRejectedValueOnce(new Error("offline"));
  await upload(user);
  expect(await screen.findByRole("alert")).toHaveTextContent("Try again");
  await user.click(screen.getByRole("button", { name: "Try again" }));
  await waitFor(() => expect(spy).toHaveBeenCalled());
  expect(await screen.findByText("What we removed")).toBeInTheDocument();
});

it("shows a human handoff for an unclear result", async () => {
  const result = (await import("../../../../contracts/examples/letter-decode.json")).default;
  vi.spyOn(client, "apiRequest").mockResolvedValueOnce({ ...result, handoff: "low_confidence" } as never);
  const user = setup();
  await upload(user);
  expect(await screen.findByRole("heading", { name: "Talk to a person" })).toBeInTheDocument();
  expect(screen.queryByLabelText("Appeal draft")).not.toBeInTheDocument();
});

it("calls a zero-day deadline due today and formats the date in Spanish", async () => {
  const result = (await import("../../../../contracts/examples/letter-decode.json")).default;
  vi.spyOn(client, "apiRequest").mockResolvedValueOnce({ ...result, deadline: { ...result.deadline, days_left: 0 } } as never);
  const user = setup();
  await user.click(screen.getByRole("button", { name: /espa/i }));
  await user.upload(screen.getByLabelText("Elige una carta"), new File(["sample"], "L03.jpg", { type: "image/jpeg" }));
  expect(await screen.findByText("Lo que quitamos")).toBeInTheDocument();
  expect(screen.getByText("Persona, Dirección, Número de teléfono, Otro")).toBeInTheDocument();
  expect(screen.getByText("31 de octubre de 2026")).toBeInTheDocument();
  expect(screen.getByText(/Vence hoy/)).toBeInTheDocument();
  expect(screen.queryByText(/ya pasó/)).not.toBeInTheDocument();
});

it("shows the redacted preview as text, never HTML", async () => {
  const result = (await import("../../../../contracts/examples/letter-decode.json")).default;
  vi.spyOn(client, "apiRequest").mockResolvedValueOnce({ ...result, redacted_preview: "Dear [PERSON], <img src=x onerror=alert(1)> at [ADDRESS]." } as never);
  const user = setup();
  await upload(user);
  const preview = await screen.findByLabelText("Redacted preview");
  expect(preview).toHaveTextContent("<img src=x onerror=alert(1)>");
  expect(preview.querySelector("img")).toBeNull();
});

it.each([
  ["en", "Choose a letter", "Email, Social Security number, FEMA registration number, Other personal detail"],
  ["es", "Elige una carta", "Correo electrónico, Número de Seguro Social, Número de registro de FEMA, Otro dato personal"],
])("shows readable %s labels for Azure and unknown categories", async (lang, fileLabel, expected) => {
  const result = (await import("../../../../contracts/examples/letter-decode.json")).default;
  vi.spyOn(client, "apiRequest").mockResolvedValueOnce({
    ...result,
    redaction: { entities_removed: 4, categories: ["Email", "USSocialSecurityNumber", "RegistrationNumber", "FutureAzureCategory"] },
  } as never);
  const user = setup();
  if (lang === "es") await user.click(screen.getByRole("button", { name: /espa/i }));
  await user.upload(screen.getByLabelText(fileLabel), new File(["sample"], "L03.jpg", { type: "image/jpeg" }));
  expect(await screen.findByText(expected)).toBeInTheDocument();
});

it.each([
  ["en", "Choose a letter", "ZIP code"],
  ["es", "Elige una carta", "Código postal"],
])("labels a removed ZIP code in %s", async (lang, fileLabel, expected) => {
  const result = (await import("../../../../contracts/examples/letter-decode.json")).default;
  vi.spyOn(client, "apiRequest").mockResolvedValueOnce({
    ...result,
    redaction: { entities_removed: 1, categories: ["ZipCode"] },
  } as never);
  const user = setup();
  if (lang === "es") await user.click(screen.getByRole("button", { name: /espa/i }));
  await user.upload(screen.getByLabelText(fileLabel), new File(["sample"], "L03.jpg", { type: "image/jpeg" }));
  expect(await screen.findByText(expected)).toBeInTheDocument();
});
