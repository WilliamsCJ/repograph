import React from "react";

import type { GetServerSideProps, NextPage } from "next";
import { FolderPlusIcon, PlusIcon } from "@heroicons/react/24/outline";

import { AccentLinkButton } from "../components/core/button";
import { DefaultLayout } from "../components/core/layout";
import GraphList from "../components/home/list";
import { EmptyState } from "../components/core/empty";
import { getGraphListings } from "../lib/home";
import { GraphListing } from "../types/graph";

export type HomePageProps = {
  graphs: GraphListing[];
};

const NewButton = () => (
  <AccentLinkButton
    icon={<FolderPlusIcon />}
    text="Create a graph"
    href="/graph/new"
  />
);

export const getServerSideProps: GetServerSideProps = async (context) => {
  const graphs = await getGraphListings();

  return {
    props: {
      graphs: graphs.filter(
        (graph: GraphListing) => graph.status !== "PENDING"
      ),
    },
  };
};

const Home: NextPage<HomePageProps> = ({ graphs }) => {
  return (
    <DefaultLayout
      buttons={graphs.length === 0 ? [] : [<NewButton />]}
      heading="Your Graphs"
    >
      {graphs.length === 0 ? (
        <EmptyState
          icon={<FolderPlusIcon />}
          heading="No graphs"
          description="Get started by uploading a repository"
          buttonText="Upload"
          buttonIcon={<PlusIcon />}
        />
      ) : (
        <GraphList graphs={graphs} />
      )}
    </DefaultLayout>
  );
};

export default Home;
