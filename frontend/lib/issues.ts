export async function getCyclicalDependencies(
  graphName: string
): Promise<number> {
  const res = await fetch(
    process.env.NEXT_PUBLIC_BACKEND_URL +
      `/graph/${graphName}/cylical-dependencies`
  );

  return (await res.json()) as number;
}
