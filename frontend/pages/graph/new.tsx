import React from "react";
import { DefaultLayout } from "../../components/core/layout";
import NewGraphForm from "../../components/graph/new";
import Head from "next/head";

export default function NewGraph() {
  return (
    <DefaultLayout buttons={[]} heading="Create Graph">
      <Head>
        <title>RepoGraph - Upload</title>
      </Head>
      <NewGraphForm />
    </DefaultLayout>
  );
}
