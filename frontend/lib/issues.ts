import {
  CircularDependencyResult,
  IncorrectAndMissingDocstringsResult,
  MissingDependencyResult, MissingDocstringResult,
  PossibleIncorrectDocstringResult
} from "../types/graph";

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
): Promise<MissingDependencyResult> {
  const res = await fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}/missing-dependencies`
  );

  return (await res.json()) as MissingDependencyResult;
}

export async function getIncorrectDocstrings(
  graphName: string
): Promise<PossibleIncorrectDocstringResult> {
  const res = await fetch(
    `http://${
      process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
    }:3000/graph/${graphName}/incorrect-docstrings`
  );

  return (await res.json()) as PossibleIncorrectDocstringResult;
}

export async function getMissingDocstrings(
graphName: string
): Promise<MissingDocstringResult> {
  const res = await fetch(
  `http://${
  process.env.NODE_ENV == "development" ? "localhost" : "repograph-backend"
  }:3000/graph/${graphName}/missing-docstrings`
  );

  return (await res.json()) as MissingDocstringResult;
}