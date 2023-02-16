import { GraphSummary } from "../types/graph";

/**
 * Retrieve summary for the provided unique graph_name
 * @param graphName
 */
export async function getSummary(graphName: string): Promise<GraphSummary> {
  const res = await fetch(
    process.env.NEXT_PUBLIC_BACKEND_URL + `/graph/${graphName}/summary`
  );
  return (await res.json()) as GraphSummary;
}
