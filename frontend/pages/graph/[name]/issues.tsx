import { NextPage } from "next";
import { DefaultLayout } from "../../../components/core/layout";
import React from "react";

import Issues from "../../../components/graph/issues";

const GraphIssues: NextPage = () => {
  return (
    <DefaultLayout buttons={[]} heading="Issues">
      <Issues />
    </DefaultLayout>
  );
};

export default GraphIssues;
