import React, { useState } from "react";

// Next.js
import { NextPage } from "next";

import tw from "twin.macro";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SearchBar } from "../../../components/graph/search/searchbar";
import { getSemanticSearchQuery } from "../../../server/search";
import { SearchResultCard } from "../../../components/graph/search/search-result";
import { Pagination } from "../../../components/graph/search/pagination";

const Search: NextPage = () => {
  const [results, setResults] = useState([]);

  let options = ["Natural", "Favourites", "Manual"];
  let searchBars = [
    <SearchBar
      label="Search"
      placeholder="Functions that do..."
      setResults={setResults}
      executeQuery={getSemanticSearchQuery}
    />,
    <SearchBar
      label="Search"
      placeholder="Select a query"
      setResults={setResults}
      executeQuery={getSemanticSearchQuery}
    />,
    <SearchBar
      label="Search"
      placeholder="MATCH ..."
      setResults={setResults}
      executeQuery={getSemanticSearchQuery}
    />,
  ];

  return (
    <DefaultLayout buttons={[]} heading="Search">
      <TabGroup titles={options} panels={searchBars} />
      <div tw="flex flex-col space-y-4">
        {results &&
        results.map((result, index) => (
        <SearchResultCard result={result} index={index} />
        ))}
      </div>
      <Pagination />
    </DefaultLayout>
  );
};

export default Search;
