import React, { useRef } from "react";

// Next.js
import { GetServerSideProps, NextPage } from "next";

import tw from "twin.macro";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SemanticSearch } from "../../../components/graph/search/semantic-search";
import CypherSearch from "../../../components/graph/search/cypher-search";

// Functions
import { getAvailableSearchQueries } from "../../../lib/search";

// Types
import { AvailableSearchQuery } from "../../../types/search";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;
  const availableQueries = await getAvailableSearchQueries(name);

  return {
    props: {
      graph: name,
      availableQueries: availableQueries
    },
  };
};

export type GraphSearchPageProps = {
  graph: string;
  availableQueries: AvailableSearchQuery[]
};

const GraphSearch: NextPage<GraphSearchPageProps> = ({ graph, availableQueries }) => {
  const topRef = useRef(null);

  let options = ["Natural", "Favourites"];
  let panels = [
    <SemanticSearch key={"Natural"} topRef={topRef} graph={graph} />,
    <CypherSearch key={"Favourites"} topRef={topRef} graph={graph} available={availableQueries} />,
  ];

  return (
    <DefaultLayout buttons={[]} heading="Search" topRef={topRef}>
      <TabGroup titles={options} panels={panels} />
    </DefaultLayout>
  );
};

export default GraphSearch;
