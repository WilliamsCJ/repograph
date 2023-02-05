import React, { useState } from "react";

/* Next */
import dynamic from "next/dynamic";

// Styling
import tw, { TwStyle } from "twin.macro"
import colors from "tailwindcss/colors";

/* External dependencies */
import ClipLoader from "react-spinners/ClipLoader";
const Graph = dynamic(() => import("./force-graph"), {
  ssr: false,
});

/* Components */
import { Border } from "./border";
import { Network, NetworkEvents } from "vis";
import { Center } from "./layout";
import { IconWrapper } from "./icon";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";
import { BlockText, BlockTextLight } from "./text";
import Script from "next/script";

/**
 * GraphCard props
 */
type GraphCardProps = {
  data: any;
  error: boolean
  styles?: TwStyle,
  root_id: number
};

/**
 * Card to display graph of data.
 * @param data
 * @param styles
 * @param error
 * @constructor
 */
const GraphCard: React.FC<GraphCardProps> = ({ data, styles, error, root_id }) => {
  const [network, setNetwork] = useState<Network | null>(null);

  // Options
  const options = {
    layout: {
      hierarchical: false,
    },
    edges: {
      color: "#000000",
      smooth: {
        enabled: true
      }
    }
  };
  
  // Events
  const events = {
    doubleClick: function() {
      if (network !== null) network.fit();
    },
    select: function(event: NetworkEvents) {
      var { nodes, edges } = event;
    },
    stabilized: () => {
      if (network) { // Network will be set using getNetwork event from the Graph component
        network.setOptions({ physics: false }); // Disable physics after stabilization
        network.fit();
      }
    }
  };

  return (
    <Border css={[styles, tw`flex max-h-full`]}>
      <Script type="text/javascript" src="ttps://visjs.github.io/vis-network/standalone/umd/vis-network.min.js" />
      {data ?
        <Graph
          autoResize={true}
          graph={data}
          options={options}
          events={events}
          css={tw`max-h-full bg-red-100`}
          getNetwork={network => {
            setNetwork(network);
          }}
        />
      :
        <Center>
          {error ?
            <div>
              <IconWrapper  color="dark" icon={<ExclamationCircleIcon />} size="md"/>
              <BlockText>Error</BlockText>
            </div>
          :
            <ClipLoader
              color={colors.gray["400"]}
              loading={true}
              size={24}
              aria-label="Loading Spinner"
              data-testid="loader"
            />
          }
        </Center>
      }
    </Border>
  );
};

export default GraphCard;
