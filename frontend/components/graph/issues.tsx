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
import {
  CircularDependencyResult,
  IssuesResult,
  MissingDependencyResult, MissingDocstringResult,
  PossibleIncorrectDocstringResult
} from "../../types/graph";
import { Pagination } from "./search/pagination";

/**
 * Props for Issues component.
 */
export type IssuesProps = {
  cyclicalDependencies: CircularDependencyResult;
  missingDependencies: MissingDependencyResult;
  incorrectDocstrings: PossibleIncorrectDocstringResult;
  missingDocstrings: MissingDocstringResult;
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
 * @param onClick
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
  const [ title, setTitle ] = useState<string|null>(null);
  const [offset, setOffset] = useState(0);
  const limit = 10;

  return (
    <>
      <dl tw="grid grid-cols-2 gap-4">
        <IssueCard
          title="Circular Dependencies"
          value={props.cyclicalDependencies.data.length}
          onClick={() => {
            setData(props.cyclicalDependencies)
            setTitle("Cyclical Dependencies")
          }}
        />
        <IssueCard
          title="Missing Dependencies"
          value={props.missingDependencies.data.length}
          onClick={() => {
            setData(props.missingDependencies)
            setTitle("Missing Dependencies")
          }}
        />
        <IssueCard
          title="Possible Incorrect Docstrings"
          value={props.incorrectDocstrings.data.length}
          onClick={() => {
            setData(props.incorrectDocstrings)
            setTitle("Incorrect Docstrings")
          }}
        />
        <IssueCard
          title="Missing Docstrings"
          value={props.missingDocstrings.data.length}
          onClick={() => {
            setData(props.missingDocstrings)
            setTitle("Missing Docstrings")
          }}
        />
      </dl>
      {title && <BoldDetailText>{title}</BoldDetailText>}
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
            .slice(offset, offset + limit)
            .map((row: any, index: number) => (
            <TableRow key={index}>
              <>
                <TableCell>{(index + 1).toString()}</TableCell>
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
      {data && data.data.length > limit && (
        <Pagination
          offset={offset}
          setOffset={setOffset}
          limit={limit}
          total={data.data.length}
        />
      )}
    </>
  );
};

export default Issues;
