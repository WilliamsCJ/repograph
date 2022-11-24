import "twin.macro";
import { CloudArrowDownIcon } from "@heroicons/react/24/outline";
// @ts-ignore
import data from "./data";
import { GraphCard } from "../components/graph";
import {
  ApplicationShell,
  HeadingRow,
  MainContainer,
  MainLayout,
} from "../components/layout";
import NavigationBar from "../components/navigation";
import { Heading } from "../components/text";
import Button from "../components/button";

function App() {
  return (
    <ApplicationShell>
      <NavigationBar />
      <MainContainer>
        <MainLayout>
          <HeadingRow>
            <Heading>Your Repository</Heading>
            <Button type="button">
              <CloudArrowDownIcon tw="h-5 w-5" />
              <span>Export</span>
            </Button>
          </HeadingRow>
          <GraphCard data={data} />
        </MainLayout>
      </MainContainer>
    </ApplicationShell>
  );
}

export default App;
