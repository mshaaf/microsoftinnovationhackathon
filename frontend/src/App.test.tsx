import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("App", () => {
  it("shows the Survivor Journey Navigator title", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { name: "Survivor Journey Navigator" })
        .textContent,
    ).toBe("Survivor Journey Navigator");
  });
});
