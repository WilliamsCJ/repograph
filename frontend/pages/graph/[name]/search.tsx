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
import {
  getAvailableSearchQueries,
  getRepositories,
} from "../../../lib/search";

// Types
import { AvailableSearchQuery } from "../../../types/search";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;
  const availableQueries = await getAvailableSearchQueries(name);
  const repositories = await getRepositories(name);

  return {
    props: {
      graph: name,
      availableQueries: availableQueries,
      repositories: repositories,
    },
  };
};

export type GraphSearchPageProps = {
  graph: string;
  availableQueries: AvailableSearchQuery[];
  repositories: string[];
};

const GraphSearch: NextPage<GraphSearchPageProps> = ({
  graph,
  availableQueries,
  repositories,
}) => {
  const topRef = useRef(null);

  let options = ["Natural", "Favourites"];
  let panels = [
    <SemanticSearch key={"Natural"} topRef={topRef} graph={graph} />,
    <CypherSearch
      key={"Favourites"}
      topRef={topRef}
      graph={graph}
      available={availableQueries}
      repositories={repositories}
    />,
  ];

  return (
    <DefaultLayout buttons={[]} heading="Search" topRef={topRef}>
      <TabGroup titles={options} panels={panels} />
    </DefaultLayout>
  );
};

export default GraphSearch;
