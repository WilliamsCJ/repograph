import React from "react";

// Next
import type { GetServerSideProps, NextPage } from "next";

// Icons
import { FolderPlusIcon, PlusIcon } from "@heroicons/react/24/outline";

// Components
import { AccentLinkButton } from "../components/core/button";
import { DefaultLayout } from "../components/core/layout";
import GraphListingComponent from "../components/home/index";

// Functions
import { getGraphListings } from "../lib/home";

// Types
import { SWRConfig } from "swr";

/**
 * Page props.
 */
export type HomePageProps = {
  fallback: any;
};

/**
 * New graph button
 * @constructor
 */
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
      fallback: {
        "/metadata/graphs": graphs,
      },
    },
  };
};

const Home: NextPage<HomePageProps> = ({ fallback }) => {
  return (
    <DefaultLayout buttons={[<NewButton />]} heading="Your Graphs">
      <SWRConfig value={{ fallback }}>
        <GraphListingComponent />
      </SWRConfig>
    </DefaultLayout>
  );
};

export default Home;
