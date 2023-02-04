import { SearchResultSet } from "../types/search";

export async function getSemanticSearchQuery(
  graph: string,
  query: string
): Promise<SearchResultSet> {
  const url = new URL(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/graph/${graph}/search/semantic`
  );
  const params = { query: query };
  url.search = new URLSearchParams(params).toString();

  const res = await fetch(url);
  return (await res.json()) as SearchResultSet;
}
