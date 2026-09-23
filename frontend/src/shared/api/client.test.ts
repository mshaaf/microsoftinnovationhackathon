import healthExample from "../../../../contracts/examples/health.json";
import { describe, expect, it } from "vitest";
import { apiRequest } from "./client";

describe("apiRequest", () => {
  it("serves the matching contract example in mock mode", async () => {
    await expect(apiRequest("/api/health", { mock: true })).resolves.toEqual(
      healthExample,
    );
  });
});
