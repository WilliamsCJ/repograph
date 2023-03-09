import type { GraphListing } from "../types/graph";

export async function getGraphListings(): Promise<GraphListing[]> {
  const url = new URL(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/metadata/graphs`
  );

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error("An error occurred!");
  }

  return (await res.json()) as GraphListing[];
}
