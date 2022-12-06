import { GraphSummary } from "../types/components/home/summary";

export async function getSummary(): Promise<GraphSummary> {
  const res = await fetch(process.env.BACKEND_URL+ "/graph/summary")
  return await res.json() as GraphSummary
}