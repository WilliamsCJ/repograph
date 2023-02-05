import React, { useRef, useState } from "react";

import tw from "twin.macro";

// Components
import { Card } from "../../core/card";
import { BlockText, BlockTextAccent, BlockTextLight, SmallHeading } from "../../core/text";
import "twin.macro";
import useDimensions from "react-use-dimensions";
const Graph = dynamic(() => import("../../core/force-graph"), {
  ssr: false,
});


// Types
import { SearchResult } from "../../../types/search";
import { JustifiedRow } from "../../core/layout";
import { CodeBlock } from "../../core/code";
import { BuiltInBadge, FunctionBadge, MethodBadge } from "../../core/badge";
import dynamic from "next/dynamic";
import GraphCard from "../../core/graph";

const data = {
  nodes: [
    { id: "Myriel", label: "Myriel" },
    { id: "Napoleon", label: "Myriel" },
    { id: "Mlle.Baptistine", label: "Myriel" },
  ],
  edges: [
    { from: "Napoleon", to: "Myriel" },
    { from: "Mlle.Baptistine", to: "Myriel"},
  ],
};

/**
 * Props for SearchResultCardSection
 */
type SearchResultCardSectionProps = {
  heading: string
  children: JSX.Element
}

/**
 * Section within a SearchResultCard (that is divided into 3 sections)
 * @param heading
 * @param children
 * @constructor
 */
const SearchResultCardSection: React.FC<SearchResultCardSectionProps> = ({ heading, children }) => (
  <div tw="py-2 px-3 max-h-full flex flex-col space-y-1">
    <SmallHeading tw="">{heading}</SmallHeading>
    {children}
  </div>
)

/**
 * Props for DetailsSection components
 */
type DetailsSectionProps = {
  detailName: string
  detail: string | JSX.Element
}

/**
 * DetailSection within SearchResultCardSection
 * @param detailName
 * @param detail
 * @constructor
 */
const DetailsSection: React.FC<DetailsSectionProps> = ({ detailName, detail}) => (
  <div>
    <BlockText>{detailName}</BlockText>
    <BlockTextLight>{detail}</BlockTextLight>
  </div>
)

function createResultTypes(result: SearchResult) {
  return (
  <>
    {result.function.type === "Function" && <FunctionBadge />}
    {result.function.type === "Method" && <MethodBadge />}
    {result.function.builtin && <BuiltInBadge />}
  </>
  )
}

/**
 * Props for SearchResultCard.
 */
export type SearchResultCardProps = {
  result: SearchResult;
  index: number;
};

/**
 * Card containing a single Semantic Search result.
 * @param result
 * @param index
 * @constructor
 */
const SearchResultCard: React.FC<SearchResultCardProps> = ({
  result,
  index,
}) => {
  return (
    <div tw="w-full">
      <JustifiedRow tw="mb-1 mx-2">
        <BlockText>{`${result.repository} > ${result.function.canonical_name}`}</BlockText>
        <BlockText>{`#${index} (${result.score})`}</BlockText>
      </JustifiedRow>
      <Card size={tw`w-full h-48`}>
        <div tw="w-full h-full grid grid-cols-3 grid-rows-1 divide-x">

          {/* Details Section */}
          <SearchResultCardSection heading="Details" >
            <div tw="flex flex-col space-y-2">
              <DetailsSection detailName="Type" detail={createResultTypes(result)} />
              <DetailsSection detailName="Line Numbers" detail={`${result.function.min_line_number} - ${result.function.max_line_number}`} />
              <DetailsSection detailName="Summary" detail={result.summarization} />
            </div>
          </SearchResultCardSection>

          {/* Source Code Section*/}
          <SearchResultCardSection heading="Source Code">
            <>
              {result.function.source_code &&
                  <CodeBlock source_code={result.function.source_code} styles={tw`grow`}/>
              }
              <BlockTextAccent>Expand</BlockTextAccent>
            </>
          </SearchResultCardSection>

          {/* Subgraph Section */}
          <SearchResultCardSection heading="Subgraph">
            <GraphCard />
          </SearchResultCardSection>
        </div>
      </Card>
    </div>
  );
};

const Pagination = () => {
  return (
    <nav
    tw="flex items-center justify-between py-4"
    aria-label="Pagination"
    >
      <div tw="hidden sm:block">
        <p tw="text-sm text-gray-700">
          Showing <span tw="font-medium">1</span> to <span tw="font-medium">10</span> of{' '}
          <span tw="font-medium">20</span> results
        </p>
      </div>
      <div tw="flex flex-1 justify-between sm:justify-end">
        <a
        href="#"
        tw="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Previous
        </a>
        <a
        href="#"
        tw="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Next
        </a>
      </div>
    </nav>
  )
}

export { SearchResultCard, Pagination };
