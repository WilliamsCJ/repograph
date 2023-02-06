import React, { useRef, useState } from "react";

// Next.js
import { NextPage } from "next";

import tw from "twin.macro";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SemanticSearch } from "../../../components/graph/search/semantic-search";

const Search: NextPage = () => {
  const [results, setResults] = useState([]);
  const topRef = useRef(null);

  let options = ["Natural", "Favourites", "Manual"];
  let panels = [
    <SemanticSearch key={"Natural"} topRef={topRef} />,
    <SemanticSearch key={"Favourites"} />,
    <SemanticSearch key={"Manual"} />,
  ];

  return (
    <DefaultLayout buttons={[]} heading="Search" topRef={topRef}>
      <TabGroup titles={options} panels={panels} />
    </DefaultLayout>
  );
};

export default Search;
