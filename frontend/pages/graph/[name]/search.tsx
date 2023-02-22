import React, { useRef } from "react";

// Next.js
import { GetServerSideProps, NextPage } from "next";

import tw from "twin.macro";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SemanticSearch } from "../../../components/graph/search/semantic-search";
import { getSummary } from "../../../lib/summary";
import { GraphSummary } from "../../../types/graph";
import CypherSearch from "../../../components/graph/search/cypher-search";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;

  return {
    props: {
      graph: name,
    },
  };
};

export type GraphSearchPageProps = {
  graph: string;
};

const GraphSearch: NextPage<GraphSearchPageProps> = ({ graph }) => {
  const topRef = useRef(null);

  let options = ["Natural", "Favourites"];
  let panels = [
    <SemanticSearch key={"Natural"} topRef={topRef} graph={graph} />,
    <CypherSearch key={"Favourites"} topRef={topRef} graph={graph} />,
    // <SemanticSearch key={"Manual"} />,
  ];

  return (
    <DefaultLayout buttons={[]} heading="Search" topRef={topRef}>
      <TabGroup titles={options} panels={panels} />
    </DefaultLayout>
  );
};

export default GraphSearch;
