/**
 * Delete the specified graph
 * @param graphName
 */
export async function deleteGraph(graphName: string): Promise<void> {
  const res = await fetch(
  process.env.NEXT_PUBLIC_BACKEND_URL + `/graph/${graphName}`,
  { method: "DELETE"}
  );

  if (res.status !== 204) {
   throw new Error("Couldn't delete graph")
  }
}
