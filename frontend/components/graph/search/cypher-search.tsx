import React, { MutableRefObject, useEffect, useState } from 'react';
import { SearchBar } from "./searchbar";
import "twin.macro";
import { SearchResultSet } from "../../../types/search";
import toast from "react-hot-toast";
import { Table, TableBody, TableCell, TableHeader, TableHeaderCell, TableRow } from "../../core/table";
import ComboSearchBar from "./combo-searchbar";

const CypherSearch = ({
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
      // TODO: Replace
      // const res = await getSemanticSearchQuery(graph, query, limit, offset);
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
      placeholder="MATCH..."
      executeQuery={() => alert('hi')}
    />
    {/*<div tw="mt-6">*/}
    {/*  <Table>*/}
    {/*    <TableHeader>*/}
    {/*      <TableHeaderCell>1</TableHeaderCell>*/}
    {/*      <TableHeaderCell>2</TableHeaderCell>*/}
    {/*      <TableHeaderCell>3</TableHeaderCell>*/}
    {/*    </TableHeader>*/}
    {/*    <TableBody>*/}
    {/*      <TableRow key={1}>*/}
    {/*        <TableCell>a</TableCell>*/}
    {/*        <TableCell>b</TableCell>*/}
    {/*        <TableCell>c</TableCell>*/}
    {/*      </TableRow>*/}
    {/*      <TableRow key={1}>*/}
    {/*        <TableCell>a</TableCell>*/}
    {/*        <TableCell>b</TableCell>*/}
    {/*        <TableCell>c</TableCell>*/}
    {/*      </TableRow>*/}
    {/*    </TableBody>*/}
    {/*  </Table>*/}
    {/*</div>*/}
    {/*{results && (*/}
    {/*<>*/}
    {/*  <div css={tw`mt-6 flex flex-col space-y-8`}>*/}
    {/*    {results.results.map((result, index) => (*/}
    {/*    <SearchResultCard result={result} index={index} graph={graph} />*/}
    {/*    ))}*/}
    {/*  </div>*/}
    {/*  <Pagination*/}
    {/*  offset={offset}*/}
    {/*  setOffset={setOffset}*/}
    {/*  limit={limit}*/}
    {/*  total={results.total}*/}
    {/*  />*/}
    {/*</>*/}
    {/*)}*/}
  </>
  )
}

export default CypherSearch;