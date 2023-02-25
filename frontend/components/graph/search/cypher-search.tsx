import React, { MutableRefObject, useEffect, useState } from 'react';

// Styling
import "twin.macro";

// Functions
import { getSearchQuery } from "../../../lib/search";

// Types
import { AvailableSearchQuery, SearchQueryResult, SearchResultSet } from "../../../types/search";

// Toast
import toast from "react-hot-toast";

// Components
import { Table, TableBody, TableCell, TableHeader, TableHeaderCell, TableRow } from "../../core/table";
import ComboSearchBar from "./combo-searchbar";
import { Pagination } from "./pagination";



const CypherSearch = ({
  topRef,
  graph,
  available
}: {
  topRef: MutableRefObject<any>;
  graph: string;
  available: AvailableSearchQuery[]
}) => {
  // Query state
  const [query, setQuery] = useState<AvailableSearchQuery | null>(null);
  // Results state
  const [results, setResults] = useState<SearchQueryResult | undefined>(
  undefined
  );

  // Pagination state
  const [offset, setOffset] = useState(0);
  const limit = 10;

  // Query executor
  const executeQuery = async (query: AvailableSearchQuery) => {
    try {
      setQuery(query)
      const res = await getSearchQuery(graph, query.id, limit, offset);
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
    <ComboSearchBar
      label="Search"
      placeholder="Search..."
      executeQuery={executeQuery}
      available={available}
    />
    <div tw="mt-6">
      {results &&
        <>
          <Table>
            <TableHeader>
              {results.columns.map((column: string) => (
                <TableHeaderCell>{column}</TableHeaderCell>
              ))}
            </TableHeader>
            <TableBody>
              {results.data.slice(offset, offset + limit).map((row: any, index: number) => (
                <TableRow key={index}>
                  {Object.values(row).map(item => (
                    <TableCell>{item as string}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
          {results.data.length > limit &&
            <Pagination
              offset={offset}
              setOffset={setOffset}
              limit={limit}
              total={results.size}
            />
          }
        </>
      }
    </div>
  </>
  )
}

export default CypherSearch;