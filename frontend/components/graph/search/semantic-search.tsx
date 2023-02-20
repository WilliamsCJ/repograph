import React, { MutableRefObject, useEffect, useState } from "react";

// Styling
import tw from "twin.macro";

// Dependencies
import toast from "react-hot-toast";

// Components
import { SearchBar } from "./searchbar";
import { getSemanticSearchQuery } from "../../../lib/search";
import { SearchResultCard } from "./search-result";
import { Pagination } from "./pagination";

// Search
import { SearchResultSet } from "../../../types/search";

/**
 * Semantic search bar and results component
 * @param topRef
 * @param graph
 * @constructor
 */
export const SemanticSearch = ({
  topRef,
  graph,
}: {
  topRef: MutableRefObject<any>;
  graph: string;
}) => {
  // Query state
  const [query, setQuery] = useState<string | null>(null);
  // Results state
  const [results, setResults] = useState<SearchResultSet | undefined>(
    undefined
  );

  // Pagination state
  const [offset, setOffset] = useState(0);
  const limit = 5;

  // Query executor
  const executeQuery = async (query: string) => {
    setQuery(query);
    try {
      const res = await getSemanticSearchQuery(graph, query, limit, offset);
      setResults(res);
    } catch (e) {
      toast.error("An error occurred!", { duration: 6000 });
    }
  };

  // Effects hook to re-execute query on pagination
  useEffect(() => {
    if (results && query) {
      executeQuery(query).then();
      topRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [offset]);

  console.log(results)

  return (
    <>
      <SearchBar
        label="Search"
        placeholder="Functions that do..."
        executeQuery={executeQuery}
      />
      {results && (
        <>
          <div css={tw`mt-6 flex flex-col space-y-8`}>
            {results.results.map((result, index) => (
              <SearchResultCard result={result} index={index} graph={graph} />
            ))}
          </div>
          <Pagination
            offset={offset}
            setOffset={setOffset}
            limit={limit}
            total={results.total}
          />
        </>
      )}
    </>
  );
};
