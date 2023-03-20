import React from "react";

// Components
import Issues from "../../../components/graph/issues";
import { DefaultLayout } from "../../../components/core/layout";

// Types
import { GetServerSideProps, NextPage } from "next";
import {
  getCyclicalDependencies,
  getIncorrectDocstrings,
  getMissingDependencies,
  getMissingDocstrings,
} from "../../../lib/issues";
import {
  CircularDependencyResult,
  MissingDependencyResult,
  MissingDocstringResult,
  PossibleIncorrectDocstringResult,
} from "../../../types/graph";
import Head from "next/head";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;

  return {
    props: {
      name: name,
      cyclicalDependencies: await getCyclicalDependencies(name),
      missingDependencies: await getMissingDependencies(name),
      incorrectDocstrings: await getIncorrectDocstrings(name),
      missingDocstrings: await getMissingDocstrings(name),
    },
  };
};

export type GraphIssuesPageProps = {
  name: string;
  cyclicalDependencies: CircularDependencyResult;
  missingDependencies: MissingDependencyResult;
  incorrectDocstrings: PossibleIncorrectDocstringResult;
  missingDocstrings: MissingDocstringResult;
};

const GraphIssues: NextPage<GraphIssuesPageProps> = (
  props: GraphIssuesPageProps
) => {
  return (
    <DefaultLayout buttons={[]} heading="Issues">
      <Head>
        <title>{`RepoGraph - ${props.name} - Issues`}</title>
      </Head>
      <Issues {...props} />
    </DefaultLayout>
  );
};

export default GraphIssues;
