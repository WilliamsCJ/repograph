import React from "react";

// Next.js
import type { GetServerSideProps, NextPage } from "next";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import Summary from "../../../components/graph/summary";
import DeleteGraphButton from "../../../components/graph/delete";

// Functions
import { getSummary } from "../../../lib/summary";

// Types
import { GraphSummary } from "../../../types/graph";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;
  const summary = await getSummary(name);

  return {
    props: {
      name: name,
      summary: summary,
    },
  };
};

export type GraphHomePageProps = {
  name: string;
  summary: GraphSummary;
};

const GraphHome: NextPage<GraphHomePageProps> = ({ name, summary }) => {
  return (
    <DefaultLayout
      buttons={[<DeleteGraphButton graphName={name} />]}
      heading="Summary"
    >
      <Summary summary={summary} />
    </DefaultLayout>
  );
};

export default GraphHome;
