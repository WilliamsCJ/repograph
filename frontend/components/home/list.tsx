import React from "react";

import tw from "twin.macro";
import moment from "moment";

import { List, ListRow } from "../core/list";
import { CalendarIcon, ChevronRightIcon } from "@heroicons/react/24/outline";
import { DetailText, SmallHeading } from "../core/text";
import IconWrapper from "../core/icon";

export type GraphEntry = {
  id: string;
  name: string;
  href: string;
  createdAt: string;
};

// GraphList

export type GraphListProps = {
  graphs: GraphEntry[];
};

const GraphList: React.FC<GraphListProps> = ({ graphs }) => {
  const rows = graphs.map((graph, index) => (
    <GraphListRow graph={graph} index={index} total={graphs.length} />
  ));

  return <List rows={rows} />;
};

// GraphListRow

export type GraphListRowProps = {
  graph: GraphEntry;
  index: number;
  total: number;
};

const GraphListRow: React.FC<GraphListRowProps> = ({ graph, index, total }) => {
  const left = <GraphEntry createdAt={graph.createdAt} name={graph.name} />;

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
      href={`/graph/${graph.id}`}
      leftComponent={left}
      rightComponent={right}
    />
  );
};

// GraphEntry

export type GraphEntryProps = {
  name: string;
  createdAt: Date;
};

const GraphEntry: React.FC<GraphEntryProps> = ({ createdAt, name }) => {
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
              Created on <time>{moment().format("DD-MM-YYYY")}</time>
            </DetailText>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphList;
