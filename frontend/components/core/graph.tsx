import React from "react";

/* Next */
import Script from "next/script";

/* Styling */
import tw, { TwStyle } from "twin.macro";
const colors = require("tailwindcss/colors");

/* External dependencies */
import ClipLoader from "react-spinners/ClipLoader";
import useDimensions from "react-use-dimensions";
import { VisGraph, VisSingleContainer } from "@unovis/react";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";

/* Components */
import { InteriorBorder } from "./constants";
import { Center } from "./layout";
import IconWrapper from "./icon";
import { BoldDetailText } from "./text";

/* Types */
import {
  CallGraph,
  CallGraphFunction,
  CallGraphRelationship,
} from "../../types/graph";

import stringToColor from "../../utils/color-hash";


/**
 * GraphCard props
 */
type GraphCardProps = {
  data: CallGraph;
  error: boolean;
  styles?: TwStyle;
  root_id: number;
  border?: boolean;
};

/**
 * Card to display graph of data.
 * @param data
 * @param styles
 * @param error
 * @param root_id
 * @param border
 * @constructor
 */
const GraphCard: React.FC<GraphCardProps> = ({
  data,
  styles,
  error,
  root_id,
  border
}) => {
  // @ts-ignore
  const [ref, { height, width }] = useDimensions();

  const nodeIcon = (n: CallGraphFunction) => {
    if (n.type === "Method") return "Me";
    if (n.type === "Class") return "C";
    if (n.type === "Module") return "Mo";
    if (n.type === "Function") return "F";
    if (n.type === "Directory") return "D";
    if (n.type === "Repository") return "R";
    if (n.type === "Docstring") return "DS";
    return "N";
  };

  const nodeFill = (n: CallGraphFunction) => {
    let hash = 0;
    for (let i = 0; i < n.type.length; i++) {
      hash = n.type.charCodeAt(i) + ((hash << 5) - hash);
    }
    let colour = '#';
    for (let i = 0; i < 3; i++) {
      let value = (hash >> (i * 8)) & 0xFF;
      colour += ('00' + value.toString(16)).substr(-2);
    }
    return colour;
  };

  const linkLabel = (l: CallGraphRelationship) => ({
    text: l.type,
  });

  const nodeLabel = (n: CallGraphFunction) => n.name;

  return (
    <div ref={ref} css={[styles, tw`flex h-14`, border && InteriorBorder]}>
      <Script
        type="text/javascript"
        src="ttps://visjs.github.io/vis-network/standalone/umd/vis-network.min.js"
      />
      {data ? (
        <VisSingleContainer data={data} height={height} width={width}>
          <VisGraph
            nodeIcon={nodeIcon}
            nodeFill={nodeFill}
            nodeStrokeWidth={0}
            nodeLabel={nodeLabel}
            // @ts-ignore
            linkArrow={"single"}
            // @ts-ignore
            linkLabel={linkLabel}
            linkWidth={2}
            layoutAutofitTolerance={1}
            zoomScaleExtent={[0.0, 3]}
          />
        </VisSingleContainer>
      ) : (
        <Center>
          {error ? (
            <div>
              <IconWrapper
                color="strong"
                icon={<ExclamationCircleIcon />}
                size="md"
              />
              <BoldDetailText>Error</BoldDetailText>
            </div>
          ) : (
            <ClipLoader
              color={colors.gray["400"]}
              loading={true}
              size={24}
              aria-label="Loading Spinner"
              data-testid="loader"
            />
          )}
        </Center>
      )}
    </div>
  );
};

export default GraphCard;
