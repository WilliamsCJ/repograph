import React from "react";

import tw from "twin.macro";
import { Card } from "./card";
import { IconWrapper } from "./icon";
import { ChevronRightIcon } from "@heroicons/react/24/outline";
import { GraphEntry } from "../home/list";

export type ListProps = {
  rows: any[];
};

export type ListRowProps = {
  index: number;
  href: string;
  leftComponent: React.ReactNode;
  rightComponent: React.ReactNode;
};

const List: React.FC<ListProps> = ({ rows }) => {
  return (
    <Card>
      <ul role="list" tw="divide-y divide-gray-200">
        {rows}
      </ul>
    </Card>
  );
};

const ListRow: React.FC<ListRowProps> = ({
  index,
  href,
  leftComponent,
  rightComponent,
}) => {
  return (
    <li key={index}>
      <a href={href} tw="block rounded hover:bg-gray-50">
        <div tw="flex items-center px-4 py-4 sm:px-6">
          {leftComponent}
          {rightComponent}
        </div>
      </a>
    </li>
  );
};

export { List, ListRow };
