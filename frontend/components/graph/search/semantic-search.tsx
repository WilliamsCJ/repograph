import React, { MutableRefObject, useEffect, useState } from "react";
import { SearchBar } from "./searchbar";
import { getSemanticSearchQuery } from "../../../server/search";
import { SearchResultCard } from "./search-result";
import { Pagination } from "./pagination";
import toast from "react-hot-toast";
import { SearchResultSet } from "../../../types/search";

export const SemanticSearch = ({
  topRef,
}: {
  topRef: MutableRefObject<any>;
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
      const res = await getSemanticSearchQuery("any", query, limit, offset);
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

  return (
    <>
      <SearchBar
        label="Search"
        placeholder="Functions that do..."
        executeQuery={executeQuery}
      />
      {results && (
        <>
          <div tw="mt-4 flex flex-col space-y-4">
            {results.results.map((result, index) => (
              <SearchResultCard result={result} index={index} />
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
