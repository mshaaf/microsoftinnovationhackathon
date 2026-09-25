import { expect, it } from "vitest";
import { loadMessages } from "./messages";

it("keeps every reviewed interface message available in Spanish", () => {
  const english = loadMessages("en");
  const spanish = loadMessages("es");

  expect(Object.keys(spanish).sort()).toEqual(Object.keys(english).sort());
  expect(Object.values(spanish).every((message) => message.trim().length > 0)).toBe(
    true,
  );
});
