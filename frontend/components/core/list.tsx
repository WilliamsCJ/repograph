import React from "react";

import tw from "twin.macro";
import { Card } from "./card";
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
  active: boolean
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
  active
}) => {
  let round = null;

  if (index === 0) {
    round = tw`rounded-t-lg`;
  } else if (index === total - 1) {
    round = tw`rounded-b-lg`;
  }

  return (
    <li key={index}>
      <a href={active ? href : ''} css={[tw`block`, active ? Hover : tw`cursor-not-allowed pointer-events-none`, round]}>
        <div tw="flex items-center px-4 py-4 sm:px-6">
          {leftComponent}
          {rightComponent}
        </div>
      </a>
    </li>
  );
};

export { List, ListRow };
