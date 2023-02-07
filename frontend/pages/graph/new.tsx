import React from "react";
import { DefaultLayout } from "../../components/core/layout";
import NewGraphForm from "../../components/graph/new";

export default function NewGraph() {
  return (
    <DefaultLayout buttons={[]} heading="Create Graph">
      <NewGraphForm />
    </DefaultLayout>
  );
};
