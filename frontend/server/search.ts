export async function postSemanticSearchQuery(graph: string, query: string): Promise<> {
  const url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/graph/${graph}/search`)
  const params = {query: query}
  url.search = new URLSearchParams(params).toString();

  const res = await fetch(url)
  return await res.json() as
}