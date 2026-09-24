import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";
import App from "./App";

afterEach(() => {
  cleanup();
  window.history.replaceState({}, "", "/");
});

describe("app shell", () => {
  it.each([
    ["/", "Start with your ZIP code"],
    ["/help-here", "Start with your ZIP code"],
    ["/apply", "Get ready to apply"],
    ["/letter", "Understand your FEMA letter"],
    ["/deadline", "Know your deadline"],
    ["/programs", "Other help you may qualify for"],
    ["/about", "About this navigator"],
  ])("renders the placeholder for %s", (path, title) => {
    window.history.replaceState({}, "", path);
    render(<App />);

    expect(screen.getByRole("heading", { name: title })).toBeInTheDocument();
  });

  it("marks the current stage and lets people go back", async () => {
    window.history.replaceState({}, "", "/letter");
    const user = userEvent.setup();
    render(<App />);

    expect(screen.getByRole("link", { name: /Letter/ })).toHaveAttribute(
      "aria-current",
      "step",
    );
    await user.click(screen.getByRole("link", { name: /Help here/ }));
    expect(screen.getByRole("link", { name: /Help here/ })).toHaveAttribute(
      "aria-current",
      "step",
    );
  });

  it("switches the persistent disclaimer to Spanish", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      screen.getByText("Not a government website. Not FEMA. FEMA makes all decisions."),
    ).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Español" }));

    expect(
      await screen.findByText(
        "Este no es un sitio web del gobierno. No es FEMA. FEMA toma todas las decisiones.",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Comienza con tu código postal" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("navigation", { name: "Pasos para recuperarse" }),
    ).toBeInTheDocument();
  });

  it("shows every service from the health contract on /status", async () => {
    window.history.replaceState({}, "", "/status");
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "Service status" }),
    ).toBeInTheDocument();
    for (const service of [
      "OpenFEMA",
      "Geo",
      "Search",
      "Model",
      "OCR",
      "PII",
      "Translator",
      "Safety",
    ]) {
      expect(screen.getByText(service)).toBeInTheDocument();
    }
  });
});
