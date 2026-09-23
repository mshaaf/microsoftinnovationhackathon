import chatExample from "../../../../contracts/examples/chat.json";
import checklistExample from "../../../../contracts/examples/checklist.json";
import declarationsExample from "../../../../contracts/examples/declarations.json";
import errorExample from "../../../../contracts/examples/error.json";
import escalateExample from "../../../../contracts/examples/escalate.json";
import healthExample from "../../../../contracts/examples/health.json";
import letterDecodeExample from "../../../../contracts/examples/letter-decode.json";
import locationExample from "../../../../contracts/examples/location.json";
import programsExample from "../../../../contracts/examples/programs.json";

const examples = {
  "/api/health": healthExample,
  "/api/location": locationExample,
  "/api/declarations": declarationsExample,
  "/api/checklist": checklistExample,
  "/api/chat": chatExample,
  "/api/letter/decode": letterDecodeExample,
  "/api/programs": programsExample,
  "/api/escalate": escalateExample,
} as const;

export type ApiPath = keyof typeof examples;
export type ApiResponse<Path extends ApiPath> = (typeof examples)[Path];
export type ApiError = typeof errorExample;
type ApiOptions = RequestInit & { mock?: boolean; params?: URLSearchParams };

export async function apiRequest<Path extends ApiPath>(
  path: Path,
  options: ApiOptions = {},
): Promise<ApiResponse<Path>> {
  const { mock, params, ...requestOptions } = options;
  if (mock ?? import.meta.env.VITE_APP_MODE !== "live") {
    return structuredClone(examples[path]) as ApiResponse<Path>;
  }

  const query = params?.toString();
  const response = await fetch(query ? `${path}?${query}` : path, requestOptions);
  if (!response.ok) {
    const error = (await response.json()) as ApiError;
    throw new Error(error.error.message);
  }
  return (await response.json()) as ApiResponse<Path>;
}
