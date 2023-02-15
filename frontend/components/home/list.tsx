import React from "react";

// Styling
import tw from "twin.macro";

// 3rd Party dependencies
import { CalendarIcon, ChevronRightIcon } from "@heroicons/react/24/outline";
import moment from "moment";

// Components
import { List, ListRow } from "../core/list";
import { DetailText, SmallHeading } from "../core/text";
import IconWrapper from "../core/icon";

// Types
import { GraphListing } from "../../types/graph";

// GraphList

/**
 * Props for the GraphList component
 */
export type GraphListProps = {
  graphs: GraphListing[];
};

/**
 * GraphList displays the list of created graphs.
 * @param graphs
 * @constructor
 */
const GraphList: React.FC<GraphListProps> = ({ graphs }) => {
  const rows = graphs.map((graph, index) => (
    <GraphListRow graph={graph} index={index} total={graphs.length} />
  ));

  return <List rows={rows} />;
};

// GraphListRow

/**
 * Props for the GraphListRow component.
 */
export type GraphListRowProps = {
  graph: GraphListing;
  index: number;
  total: number;
};

/**
 * A row in the GraphList component
 * @param graph
 * @param index
 * @param total
 * @constructor
 */
const GraphListRow: React.FC<GraphListRowProps> = ({ graph, index, total }) => {
  const left = <GraphEntry created={graph.created} name={graph.name} />;

  const right = (
    <IconWrapper
      aria-hidden="true"
      additional={tw`ml-5 flex-shrink-0`}
      size="sm"
      color="detail"
      icon={<ChevronRightIcon />}
    />
  );

  return (
    <ListRow
      index={index}
      total={total}
      href={`/graph/${graph.neo4j_name}`}
      leftComponent={left}
      rightComponent={right}
    />
  );
};

// GraphEntry

/**
 * Props for the GraphEntry component.
 */
export type GraphEntryProps = {
  name: string;
  created: string;
};

/**
 * The metadata for a single graph.
 * @param created
 * @param name
 * @constructor
 */
const GraphEntry: React.FC<GraphEntryProps> = ({ created, name }) => {
  return (
    <div tw="min-w-0 flex-1 sm:flex sm:items-center sm:justify-between">
      <div tw="truncate">
        <SmallHeading>{name}</SmallHeading>
        <div tw="mt-2 flex">
          <div tw="flex items-center">
            <IconWrapper
              aria-hidden="true"
              additional={tw`mr-1.5 flex-shrink-0`}
              size="sm"
              color="detail"
              icon={<CalendarIcon />}
            />
            <DetailText>
              Created <time>{moment(created).fromNow()}</time>
            </DetailText>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphList;
