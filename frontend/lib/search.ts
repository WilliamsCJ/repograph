import {
  AvailableSearchQuery,
  SearchQueryResult,
  SearchResultSet,
} from "../types/search";
import { CallGraph } from "../types/graph";

export async function getSemanticSearchQuery(
  graph: string,
  query: string,
  limit: number,
  offset: number
): Promise<SearchResultSet> {
  const url = new URL(`http://localhost:3000/graph/${graph}/search/semantic`);
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
    `http://localhost:3000/graph/${graph}/node/${id}/call_graph`
  );

  const res = await fetch(url);
  return (await res.json()) as CallGraph;
}

/**
 * GET available search queries for query-based search.
 * @param graph
 */
export async function getAvailableSearchQueries(
  graph: string
): Promise<AvailableSearchQuery[]> {
  const url = new URL(
    `http://repograph-backend:3000/graph/${graph}/search/query/available`
  );

  const res = await fetch(url);
  return (await res.json()) as AvailableSearchQuery[];
}

export async function getSearchQuery(
  graph: string,
  repository: string,
  queryID: number,
  limit: number,
  offset: number
): Promise<SearchQueryResult> {
  const url = new URL(
    `http://localhost:3000/graph/${graph}/search/query/${queryID}`
  );

  if (repository !== null) {
    const params = {
      repository: repository,
    };

    // @ts-ignore
    url.search = new URLSearchParams(params).toString();
  }

  const res = await fetch(url);
  return (await res.json()) as SearchQueryResult;
}

export async function getRepositories(graph: string): Promise<string[]> {
  const url = new URL(
    `http://repograph-backend:3000/graph/${graph}/repositories`
  );

  const res = await fetch(url);
  return (await res.json()) as string[];
}
