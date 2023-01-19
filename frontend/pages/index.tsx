import React from "react";
import type { GetServerSideProps, NextPage } from 'next'
import { FolderPlusIcon, PlusIcon } from "@heroicons/react/24/outline";

import tw from "twin.macro";

import { Button } from "../components/core/button";
import { DefaultLayout } from "../components/core/layout";
import Summary from "../components/graph/summary";
import GraphCard from "../components/core/graph";

import { HomePageProps } from "../types/pages/home";

import GraphList from "../components/home";
import { EmptyState } from "../components/core/empty";

const NewButton = () => (
  <Button icon={<FolderPlusIcon />} text="New"/>
);


export const getServerSideProps: GetServerSideProps = async (context) => {
  return {
    props: {
      graphs: [
        {hello: 1}
      ]
    }
  }
}

const Home: NextPage<HomePageProps> = ({ graphs }) => {
  return (
    <DefaultLayout
    buttons={graphs.length === 0 ? [] : [<NewButton />]}
    heading="Your Graphs"
    >
      {graphs.length === 0 ?
        <EmptyState
          icon={<FolderPlusIcon />}
          heading="No graphs"
          description="Get started by uploading a repository"
          buttonText="Upload"
          buttonIcon={<PlusIcon />}
        />
      :
        <GraphList></GraphList>
      }
    </DefaultLayout>
  )
}

export default Home;
