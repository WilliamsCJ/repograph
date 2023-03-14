import React, { useState } from "react";

// Styling
import tw from "twin.macro";

// Components
import { GreenCard, RedCard } from "../core/card";
import { BoldDetailText, NumericalValue, Text } from "../core/text";
import IconWrapper from "../core/icon";

// Icons
import {
  ShieldCheckIcon,
  ShieldExclamationIcon,
} from "@heroicons/react/24/outline";

// Types
import { StatsCardProps } from "./summary";
import { Table, TableBody, TableCell, TableHeader, TableHeaderCell, TableRow } from "../core/table";
import { CircularDependencyResult, IssuesResult } from "../../types/graph";

/**
 * Props for Issues component.
 */
export type IssuesProps = {
  cyclicalDependencies: CircularDependencyResult;
  missingDependencies: number;
  incorrectDocstrings: number;
  missingDocstrings: number;
};

/**
 * IssueCardProps for IssueCard component
 */
export type IssueCardProps = {
  title: string;
  value: number;
  onClick: any;
};

/**
 * IssueCard component makes up a single issue metric within the Issues component.
 * @param title
 * @param value
 * @constructor
 */
const IssueCard: React.FC<IssueCardProps> = ({ title, value, onClick }) => {
  if (value === 0) {
    return (
      <GreenCard size={tw`shadow-sm col-span-1 row-span-2`}>
        <div css={[tw`h-full w-full p-4 overflow-hidden relative`]}>
          <Text tw="truncate">{title}</Text>
          <NumericalValue tw="mt-2">{value}</NumericalValue>
          <IconWrapper
            size="lg"
            color="detail"
            icon={<ShieldCheckIcon />}
            additional={tw`absolute top-4 right-4`}
          />
        </div>
      </GreenCard>
    );
  } else {
    return (
      <RedCard size={tw`shadow-sm col-span-1 row-span-2 cursor-pointer`} onClick={onClick}>
        <div css={[tw`h-full w-full p-4 overflow-hidden relative`]}>
          <Text tw="truncate">{title}</Text>
          <NumericalValue tw="mt-2">{value}</NumericalValue>
          <IconWrapper
            size="lg"
            color="detail"
            icon={<ShieldExclamationIcon />}
            additional={tw`absolute top-4 right-4`}
          />
        </div>
      </RedCard>
    );
  }
};

/**
 * Summary component contains an array of StatsCards
 * @constructor
 * @param props
 */
const Issues: React.FC<IssuesProps> = (props) => {
  const [ data, setData ] = useState<IssuesResult|null>(null);

  return (
    <>
      <dl tw="grid grid-cols-2 gap-4">
        <IssueCard
          title="Circular Dependencies"
          value={props.cyclicalDependencies.data.length}
          onClick={() => setData(props.cyclicalDependencies)}
        />
        <IssueCard
          title="Missing Dependencies"
          value={props.missingDependencies}
          onClick={() => alert("hi")}
        />
        <IssueCard
          title="Possible Incorrect Docstrings"
          value={props.incorrectDocstrings}
          onClick={() => alert("hi")}
        />
        <IssueCard
          title="Missing Docstrings"
          value={props.missingDocstrings}
          onClick={() => alert("hi")}
        />
      </dl>
      {data ?
        <Table>
          <TableHeader>
            <>
              <TableHeaderCell>#</TableHeaderCell>
              {data.columns.map((column: string) => (
              <TableHeaderCell>{column}</TableHeaderCell>
              ))}
            </>
          </TableHeader>
          <TableBody>
            {data.data
            // .slice(offset, offset + limit)
            .map((row: any, index: number) => (
            <TableRow key={index}>
              <>
                <TableCell>{index + 1}</TableCell>
                {Object.values(row).map((item) => (
                <TableCell>{item as string}</TableCell>
                ))}
              </>
            </TableRow>
            ))}
          </TableBody>
        </Table>
        :
        <BoldDetailText>Select an issue for more detail</BoldDetailText>
      }
    </>
  );
};

export default Issues;
