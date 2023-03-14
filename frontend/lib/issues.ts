import { CircularDependencyResult } from "../types/graph";

export async function getCyclicalDependencies(
  graphName: string
): Promise<CircularDependencyResult> {
  const res = await fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}/cylical-dependencies`
  );

  return (await res.json()) as CircularDependencyResult;
}

export async function getMissingDependencies(
  graphName: string
): Promise<number> {
  const res = await fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}/missing-dependencies`
  );

  return (await res.json()) as number;
}

export async function getIncorrectAndMissingDocstrings(
  graphName: string
): Promise<number[]> {
  const res = await fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}/incorrect-and-missing-docstrings`
  );

  return (await res.json()) as number[];
}
