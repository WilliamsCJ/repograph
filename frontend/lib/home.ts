import type { GraphListing } from "../types/graph";

export async function getGraphListings(): Promise<GraphListing[]> {
  const url = new URL(
  `${process.env.NEXT_PUBLIC_BACKEND_URL}/metadata/graphs`
  );

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error("An error occurred!");
  }

  return (await res.json()) as GraphListing[];
}