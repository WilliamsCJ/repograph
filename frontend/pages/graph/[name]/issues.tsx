import React from "react";

// Components
import Issues from "../../../components/graph/issues";
import { DefaultLayout } from "../../../components/core/layout";

// Types
import { GetServerSideProps, NextPage } from "next";
import { getCyclicalDependencies } from "../../../lib/issues";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;

  return {
    props: {
      cyclicalDependencies: await getCyclicalDependencies(name),
    },
  };
};

export type GraphIssuesPageProps = {
  cyclicalDependencies: number;
};

const GraphIssues: NextPage<GraphIssuesPageProps> = (props) => {
  return (
    <DefaultLayout buttons={[]} heading="Issues">
      <Issues {...props} />
    </DefaultLayout>
  );
};

export default GraphIssues;
