import { GraphSummary } from "../types/components/home/summary";

export async function getSummary(): Promise<GraphSummary> {
  const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL+ "/v1/graph/summary")
  return await res.json() as GraphSummary
}