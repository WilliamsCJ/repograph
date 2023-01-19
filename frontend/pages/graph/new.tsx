import React from 'react';
import { NextPage } from "next";
import { DefaultLayout } from "../../components/core/layout";
import NewGraphForm from "../../components/graph/new";

const NewGraph: NextPage = () => {
  return (
  <DefaultLayout
  buttons={[]}
  heading="Create Graph"
  >
    <NewGraphForm />
  </DefaultLayout>
  )
}

export default NewGraph;
