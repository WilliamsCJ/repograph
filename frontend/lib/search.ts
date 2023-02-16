import { SearchResultSet } from "../types/search";
import { CallGraph } from "../types/graph";

export async function getSemanticSearchQuery(
  graph: string,
  query: string,
  limit: number,
  offset: number
): Promise<SearchResultSet> {
  const url = new URL(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/graph/${graph}/search/semantic`
  );
  const params = {
    query: query,
    limit: limit,
    offset: offset,
  };
  // @ts-ignore
  url.search = new URLSearchParams(params).toString();

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error("An error occurred!");
  }

  return (await res.json()) as SearchResultSet;
}

export async function getFunctionCallGraph(
  graph: string,
  id: string
): Promise<CallGraph> {
  const url = new URL(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/graph/${graph}/node/${id}/call_graph`
  );

  const res = await fetch(url);
  return (await res.json()) as CallGraph;
}