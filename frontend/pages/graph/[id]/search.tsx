import React, { useState } from "react";

// Next.js
import { NextPage } from "next";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SearchBar } from "../../../components/graph/search";
import { getSemanticSearchQuery } from "../../../server/search";

const Search: NextPage = () => {
  const [results, setResults] = useState([]);

  let options = ["Natural", "Favourites", "Manual"];
  let searchBars = [
    <SearchBar label="Search" placeholder="Functions that do..." setResults={setResults} executeQuery={getSemanticSearchQuery}/> ,
    <SearchBar label="Search" placeholder="Select a query" setResults={setResults} executeQuery={getSemanticSearchQuery}/> ,
    <SearchBar label="Search" placeholder="MATCH ..." setResults={setResults} executeQuery={getSemanticSearchQuery}/>
  ];

  return (
  <DefaultLayout buttons={[]} heading="Search">
    <TabGroup titles={options} panels={searchBars} />
    {/* TODO: Render results */}
  </DefaultLayout>
  );
};

export default Search;
