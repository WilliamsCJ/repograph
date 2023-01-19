import React from "react";

import type { GetServerSideProps, NextPage } from "next";
import { FolderPlusIcon, PlusIcon } from "@heroicons/react/24/outline";

import { LinkButton } from "../components/core/button";
import { DefaultLayout } from "../components/core/layout";
import GraphList, { GraphEntry } from "../components/home/list";
import { EmptyState } from "../components/core/empty";

export type HomePageProps = {
  graphs: GraphEntry[];
};

const NewButton = () => (
  <LinkButton
    primary={false}
    icon={<FolderPlusIcon />}
    text="New"
    href="/graph/new"
  />
);

export const getServerSideProps: GetServerSideProps = async (context) => {
  return {
    props: {
      graphs: [
        { id: 1, name: "fastapi", createdAt: "05-09-2023" },
        { id: 2, name: "pyLODE", createdAt: "05-10-2023" },
      ],
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
