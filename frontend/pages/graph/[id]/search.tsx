import React, { useState } from "react";

// Next.js
import { NextPage } from "next";

import tw from "twin.macro";

// Components
import { DefaultLayout } from "../../../components/core/layout";
import { TabGroup } from "../../../components/core/tabs";
import { SearchBar } from "../../../components/graph/search/searchbar";
import { getSemanticSearchQuery } from "../../../server/search";
import { Card, FullWidthCard } from "../../../components/core/card";
import { Heading, TextAccent, TextLight } from "../../../components/core/text";
import { Pagination, SearchResultCard } from "../../../components/graph/search/search-result";

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
      {/* TODO: Render results */}
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
