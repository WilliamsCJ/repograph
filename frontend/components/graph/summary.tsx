import React from "react";

import tw from "twin.macro";
import { Card } from "../core/card";
import {
  GraphSummary,
  StatsCardProps,
} from "../../types/components/home/summary";

const StatsCard: React.FC<StatsCardProps> = ({ title, value }) => {
  return (
    <Card size={tw`shadow-sm h-24`}>
      <div tw="h-full w-full p-4 overflow-hidden">
        <dt tw="truncate text-sm font-medium text-gray-500">{title}</dt>
        <dd tw="mt-2 text-3xl font-semibold tracking-tight text-gray-900">
          {value}
        </dd>
      </div>
    </Card>
  );
};

const Summary = ({ summary }: { summary: GraphSummary }) => {
  return (
    <dl tw="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatsCard title="Packages" value={summary.packages} />
      <StatsCard title="Modules" value={summary.modules} />
      <StatsCard title="Functions" value={summary.functions} />
      <StatsCard title="Classes" value={summary.classes} />
    </dl>
  );
};

export default Summary;
