import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { LanguageProvider } from "../../app/LanguageContext";
import { HandoffCard } from "./HandoffCard";

it("shows steps and tel links", () => {
  render(
    <LanguageProvider>
      <HandoffCard
        card={{
          title: "Get help now",
          steps: ["Call 911."],
          phones: [{ label: "FEMA Helpline", number: "1-800-621-3362" }],
        }}
      />
    </LanguageProvider>,
  );
  expect(screen.getByRole("heading", { name: "Get help now" })).toBeInTheDocument();
  expect(screen.getByText("Call 911.")).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /FEMA Helpline/ })).toHaveAttribute(
    "href",
    "tel:18006213362",
  );
});
