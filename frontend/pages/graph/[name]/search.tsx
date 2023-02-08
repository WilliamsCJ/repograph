import React, { useRef, useState } from "react";

// Next.js
import { GetServerSideProps, NextPage } from "next";

import tw from "twin.macro";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SemanticSearch } from "../../../components/graph/search/semantic-search";
import { getSummary } from "../../../lib/summary";
import { GraphSummary } from "../../../types/graph";

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;

  return {
    props: {
      graph: name,
    },
  };
};

export type SearchPageProps = {
  graph: string;
};

const Search: NextPage<SearchPageProps> = ({ graph }) => {
  const topRef = useRef(null);

  let options = ["Natural", "Favourites", "Manual"];
  let panels = [
    <SemanticSearch key={"Natural"} topRef={topRef} graph={graph} />,
    // <SemanticSearch key={"Favourites"} />,
    // <SemanticSearch key={"Manual"} />,
  ];

  return (
    <DefaultLayout buttons={[]} heading="Search" topRef={topRef}>
      <TabGroup titles={options} panels={panels} />
    </DefaultLayout>
  );
};

export default Search;
