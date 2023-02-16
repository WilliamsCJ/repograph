import React from 'react';

import tw from "twin.macro";

import { EmptyState } from "../core/empty";
import { FolderPlusIcon, PlusIcon } from "@heroicons/react/24/outline";
import { SmallHeading } from "../core/text";
import GraphList from "./list";
import { GraphListing } from "../../types/graph";
import fetcher from "../../utils/fetcher";
import useSWR from "swr";

const GraphListingComponent = () => {
  const { data } = useSWR('/metadata/graphs', fetcher, { refreshInterval: 10 })

  if (data.length === 0) return (
    <EmptyState
    icon={<FolderPlusIcon />}
    heading="No graphs"
    description="Get started by uploading a repository"
    buttonText="Upload"
    buttonIcon={<PlusIcon />}
    href="/graph/new"
    />
  )

  const graphs = data.filter(
    (graph: GraphListing) => graph.status !== "PENDING"
  )

  const pending = data.filter(
    (graph: GraphListing) => graph.status === "PENDING"
  )

  return (
    <div tw="pb-4 flex flex-col space-y-4">
      {graphs.length > 0 &&
          <>
              <SmallHeading>Active</SmallHeading>
              <GraphList graphs={graphs} />
          </>
      }
      {pending.length > 0 &&
          <>
              <SmallHeading>Pending</SmallHeading>
              <GraphList graphs={pending} />
          </>
      }
    </div>
  )
}

export default GraphListingComponent;