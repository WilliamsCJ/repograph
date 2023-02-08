import React from "react";

import tw from "twin.macro";
import { Card } from "./card";
import IconWrapper from "./icon";
import { ChevronRightIcon } from "@heroicons/react/24/outline";
import { GraphEntry } from "../home/list";
import { Divide, Hover } from "./constants";

export type ListProps = {
  rows: any[];
};

export type ListRowProps = {
  index: number;
  total: number;
  href: string;
  leftComponent: React.ReactNode;
  rightComponent: React.ReactNode;
};

const List: React.FC<ListProps> = ({ rows }) => {
  return (
    <Card>
      <ul role="list" css={[tw`divide-y`, Divide]}>
        {rows}
      </ul>
    </Card>
  );
};

const ListRow: React.FC<ListRowProps> = ({
  index,
  total,
  href,
  leftComponent,
  rightComponent,
}) => {
  let round = null;

  if (index === 0) {
    round = tw`rounded-t-lg`;
  } else if (index === total - 1) {
    round = tw`rounded-b-lg`;
  }

  return (
    <li key={index}>
      <a href={href} css={[tw`block`, Hover, round]}>
        <div tw="flex items-center px-4 py-4 sm:px-6">
          {leftComponent}
          {rightComponent}
        </div>
      </a>
    </li>
  );
};

export { List, ListRow };
