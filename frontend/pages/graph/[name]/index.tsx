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
import { CallGraph, GraphSummary } from "../../../types/graph";
import GraphCard from "../../../components/core/graph";
import { Card } from "../../../components/core/card";

import tw from "twin.macro";
import useSWR from "swr";
import fetcher from "../../../utils/fetcher";

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
  const { data, error } = useSWR(`/graph/${name}`, fetcher);

  return (
    <DefaultLayout
      buttons={[<DeleteGraphButton graphName={name} />]}
      heading="Summary"
    >
      <Summary summary={summary} />
      <Card size={tw`h-full`}>
        <GraphCard
          data={data}
          error={error}
          root_id={0}
          styles={tw`min-h-full`}
        />
      </Card>
    </DefaultLayout>
  );
};

export default GraphHome;
