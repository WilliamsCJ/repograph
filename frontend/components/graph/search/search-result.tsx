import React, { useState } from "react";

// Styling
import tw from "twin.macro";

// Data fetching
import useSWR from "swr";

// Types
import { SearchResult } from "../../../types/search";

// Components
import { JustifiedRow } from "../../core/layout";
import { CodeBlock } from "../../core/code";
import { BuiltInBadge, FunctionBadge, MethodBadge } from "../../core/badge";
import GraphCard from "../../core/graph";
import { Card } from "../../core/card";
import { AccentText, BoldDetailText, DetailText, SmallHeading } from "../../core/text";
import fetcher from "../../../utils/fetcher";
import { Divide } from "../../core/constants";
import CodeViewModal from "./code-view";

/**
 * Props for SearchResultCardSection
 */
type SearchResultCardSectionProps = {
  heading: string;
  children: JSX.Element;
  link?: JSX.Element;
};

/**
 * Section within a SearchResultCard (that is divided into 3 sections)
 * @param heading
 * @param children
 * @param link
 * @constructor
 */
const SearchResultCardSection: React.FC<SearchResultCardSectionProps> = ({
  heading,
  children,
  link,
}) => (
  <div tw="py-2 px-3 max-h-full flex flex-col space-y-1">
    <div tw="flex flex-row justify-between">
      <SmallHeading tw="">{heading}</SmallHeading>
      {link}
    </div>
    {children}
  </div>
);

/**
 * Props for DetailsSection components
 */
type DetailsSectionProps = {
  detailName: string;
  detail: string | JSX.Element;
};

/**
 * DetailSection within SearchResultCardSection
 * @param detailName
 * @param detail
 * @constructor
 */
const DetailsSection: React.FC<DetailsSectionProps> = ({
  detailName,
  detail,
}) => (
  <div>
    <BoldDetailText>{detailName}</BoldDetailText>
    <DetailText tw="truncate">{detail}</DetailText>
  </div>
);

function createResultTypes(result: SearchResult) {
  return (
    <>
      {result.function.type === "Function" && <FunctionBadge />}
      {result.function.type === "Method" && <MethodBadge />}
      {result.function.builtin && <BuiltInBadge />}
    </>
  );
}

/**
 * Props for SearchResultCard.
 */
export type SearchResultCardProps = {
  result: SearchResult;
  index: number;
  graph: string;
};

/**
 * Card containing a single Semantic Search result.
 * @param result
 * @param index
 * @param graph
 * @constructor
 */
const SearchResultCard: React.FC<SearchResultCardProps> = ({
  result,
  index,
  graph,
}) => {
  const url = `/graph/${graph}/node/${result.function.id}/call_graph`;
  const { data, error } = useSWR(url, fetcher);
  const [ openModal, setOpenModal ] = useState(false);

  return (
    <div tw="w-full">
      <JustifiedRow tw="mb-1 mx-2">
        <BoldDetailText>{`${result.function.repository_name} > ${result.function.canonical_name}`}</BoldDetailText>
        <BoldDetailText>{`#${index + 1} (${result.score})`}</BoldDetailText>
      </JustifiedRow>
      <Card size={tw`w-full h-48`}>
        <div
          css={[
            tw`w-full h-full grid grid-cols-3 grid-rows-1 divide-x`,
            Divide,
          ]}
        >
          {/* Details Section */}
          <SearchResultCardSection heading="Details">
            <div tw="flex flex-col space-y-2">
              <DetailsSection
                detailName="Type"
                detail={createResultTypes(result)}
              />
              <DetailsSection
                detailName="Line Numbers"
                detail={`${result.function.min_line_number} - ${result.function.max_line_number}`}
              />
              <DetailsSection
                detailName="Summary"
                detail={result.summarization}
              />
            </div>
          </SearchResultCardSection>

          {/* Source Code Section*/}
          <SearchResultCardSection
            heading="Source Code"
            link={<AccentText tw="text-sm hover:cursor-pointer" onClick={() => setOpenModal(true)}>Expand</AccentText>}
          >
            <>
              {result.function.source_code && (
                <CodeBlock
                  source_code={result.function.source_code}
                  styles={tw`grow`}
                  hideScrollBar={true}
                />
              )}
            </>
          </SearchResultCardSection>

          {/* Subgraph Section */}
          <SearchResultCardSection heading="Subgraph">
            <GraphCard
              data={data}
              styles={tw`grow`}
              error={error}
              root_id={result.function.id}
            />
          </SearchResultCardSection>
        </div>
      </Card>
      {result.function.source_code &&
        <CodeViewModal source_code={result.function.source_code} open={openModal} setOpen={setOpenModal} />
      }
    </div>
  );
};

export { SearchResultCard };
