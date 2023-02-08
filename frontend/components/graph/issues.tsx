import React from "react";
import { Card, GreenCard, RedCard } from "../core/card";
import tw from "twin.macro";
import { NumericalValue, Text } from "../core/text";
import { GraphSummary } from "../../types/graph";
import { StatsCardProps } from "./summary";
import { ShieldCheckIcon } from "@heroicons/react/24/outline";
import IconWrapper from "../core/icon";

const IssueCard: React.FC<StatsCardProps> = ({ title, value }) => {
  if (value === 0) {
    return (
      <GreenCard size={tw`shadow-sm col-span-1 row-span-2`}>
        <div css={[tw`h-full w-full p-4 overflow-hidden relative`]}>
          <Text tw="truncate">{title}</Text>
          <NumericalValue tw="mt-2">{value}</NumericalValue>
          <IconWrapper
            size="lg"
            color="green"
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
            color="red"
            icon={<ShieldCheckIcon />}
            additional={tw`absolute top-4 right-4`}
          />
        </div>
      </RedCard>
    );
  }
};

/**
 * Summary component contains an array of StatsCards
 * @param summary {GraphSummary}: The Summary details
 * @constructor
 */
const Issues = () => {
  return (
    <>
      <dl tw="grid grid-cols-2 gap-4">
        <IssueCard title="Circular Dependencies" value={0} />
        <IssueCard title="Missing Imports" value={1} />
      </dl>
    </>
  );
};

export default Issues;
