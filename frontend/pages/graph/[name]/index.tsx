import React from "react";
import type { GetServerSideProps, NextPage } from "next";
import { CloudArrowDownIcon } from "@heroicons/react/24/outline";

import { Button } from "../../../components/core/button";
import { DefaultLayout } from "../../../components/core/layout";
import Summary from "../../../components/graph/summary";

import { getSummary } from "../../../lib/summary";
import { GraphSummary } from "../../../types/graph";

const ExportButton = () => (
  <Button icon={<CloudArrowDownIcon />} text="Delete" />
);

export const getServerSideProps: GetServerSideProps = async (context) => {
  // @ts-ignore
  const { name } = context.params;
  const summary = await getSummary(name);

  return {
    props: {
      summary: summary,
    },
  };
};

export type GraphHomePageProps = {
  summary: GraphSummary;
};

const RepositoryHome: NextPage<GraphHomePageProps> = ({ summary }) => {
  return (
    <DefaultLayout buttons={[<ExportButton />]} heading="Summary">
      <Summary summary={summary} />
    </DefaultLayout>
  );
};

export default RepositoryHome;
