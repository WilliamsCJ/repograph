import React, { useRef } from "react";

/* External dependencies */
import "twin.macro";
import { ForceGraph2D } from "react-force-graph";
import useDimensions from "react-use-dimensions";

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
  // @ts-ignore
  const [ref, { x, y, width, height }] = useDimensions(); // TODO: Fix this error
  const fgRef = useRef();

  return (
    <FullWidthCard>
      <FullContainer ref={ref}>
        <ForceGraph2D
          ref={fgRef}
          graphData={data}
          width={width}
          height={height}
          onEngineStop={() => fgRef.current.zoomToFit(400)}
        />
      </FullContainer>
    </FullWidthCard>
  );
};

export { GraphCard };
