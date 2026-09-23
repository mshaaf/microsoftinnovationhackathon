import healthExample from "../../../../contracts/examples/health.json";
import declarationsExample from "../../../../contracts/examples/declarations.json";
import { describe, expect, it, vi } from "vitest";
import { apiRequest } from "./client";

describe("apiRequest", () => {
  it("serves the matching contract example in mock mode", async () => {
    await expect(apiRequest("/api/health", { mock: true })).resolves.toEqual(
      healthExample,
    );
  });

  it("sends query parameters with live requests", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => declarationsExample,
    } as Response);

    try {
      await apiRequest("/api/declarations", {
        mock: false,
        params: new URLSearchParams({
          state: "XX",
          county_fips: "99001",
          lang: "es",
        }),
      });

      expect(fetchMock).toHaveBeenCalledWith(
        "/api/declarations?state=XX&county_fips=99001&lang=es",
        {},
      );
    } finally {
      fetchMock.mockRestore();
    }
  });
});
