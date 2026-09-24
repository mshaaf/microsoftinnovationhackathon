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
        onClick={() =>
          updateJourney({
            answers: { lost_id: true, household_size: 3 },
          })
        }
      >
        Save answers
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

    await user.click(screen.getByRole("button", { name: "Save answers" }));
    expect(screen.getByText("true:3")).toBeInTheDocument();
  });
});
