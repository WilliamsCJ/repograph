import React from "react";
import type { GetServerSideProps, NextPage } from 'next'
import { CloudArrowDownIcon } from "@heroicons/react/24/outline";

import { Button } from "../../../components/core/button";
import { DefaultLayout } from "../../../components/core/layout";
import Summary from "../../../components/graph/summary";

import { getSummary } from "../../../server/summary";
import { GraphSummary } from "../../../types/components/home/summary";

const ExportButton = () => (
<Button icon={<CloudArrowDownIcon />} text="Export"/>
);


export const getServerSideProps: GetServerSideProps = async (context) => {
  const summary = await getSummary();
  return {
    props: {
      summary: summary
    }
  }
}

export type GraphHomePageProps = {
  summary: GraphSummary
}

const RepositoryHome: NextPage<GraphHomePageProps> = ({summary}) => {
  return (
  <DefaultLayout
  buttons={[<ExportButton />]}
  heading="Graph"
  >
    <Summary summary={summary} />
    {/*<GraphCard data={data} />*/}
  </DefaultLayout>
  )
}

export default RepositoryHome;
