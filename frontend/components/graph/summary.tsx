import React from "react";

// Styling
import tw from "twin.macro";

// Components
import { Card } from "../core/card";
import { NumericalValue, Text } from "../core/text";

// Types
import { GraphSummary } from "../../types/graph";

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
export const StatsCard: React.FC<StatsCardProps> = ({ title, value }) => {
  return (
    <Card size={tw`shadow-sm col-span-1 row-span-2`}>
      <div tw="h-full w-full p-4 overflow-hidden">
        <Text tw="truncate">{title}</Text>
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
        <StatsCard
          title="Total Relationships"
          value={summary.relationships_total}
        />
        <StatsCard title="Repositories" value={summary.repositories} />
        <StatsCard title="Packages" value={summary.packages} />
        <StatsCard title="Modules" value={summary.modules} />
        <StatsCard title="Functions" value={summary.functions} />
        <StatsCard title="Classes" value={summary.classes} />
      </dl>
    </>
  );
};

export default Summary;
