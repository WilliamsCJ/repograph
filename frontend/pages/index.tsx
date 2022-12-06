import React from "react";
import type { GetServerSideProps, NextPage } from 'next'
import { CloudArrowDownIcon } from "@heroicons/react/24/outline";

import { Button } from "../components/core/button";
import { DefaultLayout } from "../components/core/layout";
import Summary from "../components/home/summary";
import GraphCard from "../components/core/graph";

import { getSummary } from "../server/summary";
import { HomePageProps } from "../types/pages/home";

import data from "../data";

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


const Home: NextPage<HomePageProps> = ({summary}) => {
  return (
    <DefaultLayout
    buttons={[<ExportButton />]}
    heading="Your Repository"
    >
      <Summary summary={summary} />
      {/*<GraphCard data={data} />*/}
    </DefaultLayout>
  )
}

export default Home;

// : Promise<HomePageProps>