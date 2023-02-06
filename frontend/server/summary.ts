import { GraphSummary } from "../types/summary";

export async function getSummary(): Promise<GraphSummary> {
  const res = await fetch(
    process.env.NEXT_PUBLIC_BACKEND_URL + "/graph/summary"
  );
  return (await res.json()) as GraphSummary;
}
