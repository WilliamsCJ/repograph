import React from "react";

// Styling
import tw from "twin.macro";

// Components
import { GreenCard, RedCard } from "../core/card";
import { NumericalValue, Text } from "../core/text";
import IconWrapper from "../core/icon";

// Icons
import {
  ShieldCheckIcon,
  ShieldExclamationIcon,
} from "@heroicons/react/24/outline";

// Types
import { StatsCardProps } from "./summary";

/**
 * Props for Issues component.
 */
export type IssuesProps = {
  cyclicalDependencies: number;
  missingDependencies: number;
};

/**
 * IssueCard component makes up a single issue metric within the Issues component.
 * @param title
 * @param value
 * @constructor
 */
const IssueCard: React.FC<StatsCardProps> = ({ title, value }) => {
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
      <RedCard size={tw`shadow-sm col-span-1 row-span-2`}>
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
  return (
    <>
      <dl tw="grid grid-cols-2 gap-4">
        <IssueCard
          title="Circular Dependencies"
          value={props.cyclicalDependencies}
        />
        <IssueCard title="Missing Dependencies" value={props.missingDependencies} />
      </dl>
    </>
  );
};

export default Issues;
