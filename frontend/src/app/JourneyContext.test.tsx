import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { JourneyProvider, useJourney } from "./JourneyContext";

function JourneyProbe() {
  const { journey, updateJourney } = useJourney();

  return (
    <>
      <output>{`${journey.answers.lost_id}:${journey.answers.household_size}`}</output>
      <button
        type="button"
        onClick={() => updateJourney({ answers: { lost_id: true } })}
      >
        Set lost ID
      </button>
      <button
        type="button"
        onClick={() => updateJourney({ answers: { household_size: 3 } })}
      >
        Set household size
      </button>
    </>
  );
}

describe("journey state", () => {
  it("keeps boolean and numeric answers in memory", async () => {
    const user = userEvent.setup();
    render(
      <JourneyProvider>
        <JourneyProbe />
      </JourneyProvider>,
    );

    await user.click(screen.getByRole("button", { name: "Set lost ID" }));
    await user.click(screen.getByRole("button", { name: "Set household size" }));
    expect(screen.getByText("true:3")).toBeInTheDocument();
  });
});
