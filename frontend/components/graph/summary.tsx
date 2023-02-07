import React from "react";

import tw from "twin.macro";
import { Card } from "../core/card";
import { GraphSummary } from "../../types/graph";
import { NumericalValue, Text } from "../core/text";

/**
 * StatsCardProps for StatsCard component
 */
export type StatsCardProps = {
  title: string;
  value: number;
};

/**
 * StatsCard component
 * @param title {string}: The Card title
 * @param value {number}: The value of the
 * @constructor
 */
const StatsCard: React.FC<StatsCardProps> = ({ title, value }) => {
  return (
    <Card size={tw`shadow-sm`}>
      <div tw="h-full w-full p-4 overflow-hidden">
        <Text>{title}</Text>
        <NumericalValue tw="mt-2">{value}</NumericalValue>
      </div>
    </Card>
  );
};

/**
 * Summary component contains an array of StatsCards
 * @param summary {GraphSummary}: The Summary details
 * @constructor
 */
const Summary = ({ summary }: { summary: GraphSummary }) => {
  return (
    <>
      <dl tw="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard title="Total Nodes" value={summary.nodes_total} />
        <StatsCard title="Total Relationships" value={summary.relationships_total} />
        <StatsCard title="Repositories" value={summary.repositories} />
      </dl>
      <dl tw="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard title="Packages" value={summary.packages} />
        <StatsCard title="Modules" value={summary.modules} />
        <StatsCard title="Functions" value={summary.functions} />
        <StatsCard title="Classes" value={summary.classes} />
      </dl>
    </>
  );
};

export default Summary;
