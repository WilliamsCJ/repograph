import { CallGraph, GraphInfo, GraphSummary } from "../types/graph";

/**
 * Retrieve summary for the provided unique graph_name
 * @param graphName
 */
export async function getSummary(graphName: string): Promise<GraphSummary> {
  const res = await fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}/summary`
  );
  return (await res.json()) as GraphSummary;
}

export async function getGraphNodesAndRelationships(graphName: string): Promise<GraphInfo> {
  const res = await fetch(
  `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}`
  )

  return (await res.json()) as GraphInfo;
}