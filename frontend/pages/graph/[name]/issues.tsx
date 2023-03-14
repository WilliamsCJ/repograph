import React from "react";

// Components
import Issues from "../../../components/graph/issues";
import { DefaultLayout } from "../../../components/core/layout";

// Types
import { GetServerSideProps, NextPage } from "next";
import {
  getCyclicalDependencies,
  getIncorrectAndMissingDocstrings,
  getMissingDependencies,
} from "../../../lib/issues";
import { CircularDependencyResult, MissingDependencyResult } from "../../../types/graph";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;

  const docstrings = await getIncorrectAndMissingDocstrings(name);

  return {
    props: {
      cyclicalDependencies: await getCyclicalDependencies(name),
      missingDependencies: await getMissingDependencies(name),
      incorrectDocstrings: docstrings[0],
      missingDocstrings: docstrings[1],
    },
  };
};

export type GraphIssuesPageProps = {
  cyclicalDependencies: CircularDependencyResult;
  missingDependencies: MissingDependencyResult;
  incorrectDocstrings: number;
  missingDocstrings: number;
};

const GraphIssues: NextPage<GraphIssuesPageProps> = (props: GraphIssuesPageProps) => {
  return (
    <DefaultLayout buttons={[]} heading="Issues">
      <Issues {...props} />
    </DefaultLayout>
  );
};

export default GraphIssues;
