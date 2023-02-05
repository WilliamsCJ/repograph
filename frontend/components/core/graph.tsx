import React, { useState } from "react";

/* Next */
import dynamic from "next/dynamic";

import tw, { TwStyle } from "twin.macro"

/* External dependencies */
const Graph = dynamic(() => import("./force-graph"), {
  ssr: false,
});

/* Components */
import { Border } from "./border";
import { Network, NetworkEvents } from "vis";

/**
 * GraphCard props
 */
type GraphCardProps = {
  data: any;
  styles: TwStyle
};

/**
 * Card to display graph of data.
 * @param data
 * @param styles
 * @constructor
 */
const GraphCard: React.FC<GraphCardProps> = ({ data, styles }) => {
  const [network, setNetwork] = useState<Network | null>(null);

  const options = {
    layout: {
      hierarchical: false
    },
    edges: {
      color: "#000000"
    },
    physics: {
      forceAtlas2Based: {
        gravitationalConstant: -26,
        centralGravity: 0.005,
        springLength: 230,
        springConstant: 0.18,
      },
      maxVelocity: 146,
      solver: "forceAtlas2Based",
      timestep: 0.35,
      stabilization: {
        enabled: true,
        iterations: 2000,
        updateInterval: 25,
      },
    }
  };

  const events = {
    doubleClick: function() {
      if (network !== null) network.fit();
    },
    // select: function(event: NetworkEvents) {
    //   var { nodes, edges } = event;
    // },
    stabilized: () => {
      if (network) { // Network will be set using getNetwork event from the Graph component
        network.setOptions({ physics: false }); // Disable physics after stabilization
        network.fit();
      }
    }
  };

  return (
    <Border css={[styles]}>
      <Graph
      graph={data}
      options={options}
      events={events}
      getNetwork={network => {
        setNetwork(network);
      }}
      />
    </Border>
  );
};

export default GraphCard;
