import React, { useRef } from "react";

/* Next */
import dynamic from "next/dynamic";

/* External dependencies */
import "twin.macro";
import useDimensions from "react-use-dimensions";
const ForceGraph2D = dynamic(() => import("./force-graph"), {
  ssr: false,
});

/* Components */
import { FullWidthCard } from "./card";
import { FullContainer } from "./layout";

/**
 * GraphCard props
 */
type GraphCardProps = {
  data: any;
};

/**
 * Card to display graph of data.
 * @param data
 * @constructor
 */
const GraphCard: React.FC<GraphCardProps> = ({ data }) => {
  // @ts-ignore - TODO: Fix this error
  const [ref, { x, y, width, height }] = useDimensions();
  const fgRef = useRef();

  return (
    <FullWidthCard>
      <FullContainer ref={ref}>
        <ForceGraph2D
          ref={fgRef}
          graphData={data}
          width={width}
          height={height}
          // @ts-ignore - TODO: Look into this
          onEngineStop={() => fgRef.current.zoomToFit(400)}
        />
      </FullContainer>
    </FullWidthCard>
  );
};

export default GraphCard;
