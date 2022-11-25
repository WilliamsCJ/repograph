import "twin.macro";
import { CloudArrowDownIcon } from "@heroicons/react/24/outline";
// @ts-ignore
import data from "../data";
import { GraphCard } from "../components/graph";
import { DefaultLayout } from "../components/layout";
import { Button } from "../components/button";

const ExportButton = () => (
  <Button icon={<CloudArrowDownIcon />} text="Export" />
);

function Home() {
  return (
    <DefaultLayout
      buttons={[<ExportButton />, <ExportButton />]}
      heading="Your Repository"
    >
      <GraphCard data={data} />
    </DefaultLayout>
  );
}

export default Home;
