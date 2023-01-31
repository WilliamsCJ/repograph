import { GraphSummary } from "../types/components/home/summary";

export async function getSummary(): Promise<GraphSummary> {
  const res = await fetch(
    process.env.NEXT_PUBLIC_BACKEND_URL + "/ggraph/summary"
  );
  return (await res.json()) as GraphSummary;
}
