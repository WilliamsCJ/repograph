import React, { useState } from "react";

/* Next */
import dynamic from "next/dynamic";

// Styling
import tw, { TwStyle } from "twin.macro";

/* External dependencies */
import ClipLoader from "react-spinners/ClipLoader";
// const Graph = dynamic(() => import("./force-graph"), {
//   ssr: false,
// });

/* Components */
import { Border, InteriorBorder } from "./constants";
import { Network, NetworkEvents } from "vis";
import { Center } from "./layout";
import IconWrapper from "./icon";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";
import { BoldDetailText, DetailText } from "./text";
import Script from "next/script";
import { VisGraph, VisSingleContainer } from "@unovis/react";
import useDimensions from "react-use-dimensions";
import { CallGraph, CallGraphFunction } from "../../types/graph";
import { useTheme } from "next-themes";
const colors = require('tailwindcss/colors')

/**
 * GraphCard props
 */
type GraphCardProps = {
  data: any;
  error: boolean;
  styles?: TwStyle;
  root_id: number;
};

/**
 * Card to display graph of data.
 * @param data
 * @param styles
 * @param error
 * @constructor
 */
const GraphCard: React.FC<GraphCardProps> = ({
  data,
  styles,
  error,
  root_id,
}) => {
  // @ts-ignore
  const [ref, { height, width }] = useDimensions();
  const dark = useTheme();

  const nodeIcon = (n: CallGraphFunction) => {
    if (n.type === "METHOD") return 'Me';
    if (n.type === "CLASS") return 'C';
    if (n.type === "MODULE") return 'Mo';
    return 'F';
  }

  const nodeFill = (n: CallGraphFunction) => {
    if (n.type === "METHOD") return dark ? colors.purple[400] : colors.purple[100];
    if (n.type === "CLASS") return dark ? colors.yellow[400] : colors.yellow[100];
    if (n.type === "MODULE") return dark ? colors.green[400] : colors.green[100];
    return dark ? colors.blue[400] : colors.blue[100];
  }

  const nodeStroke = (n: CallGraphFunction) => {
    if (n.type === "METHOD") return dark ? colors.purple[300] : colors.purple[800];
    if (n.type === "CLASS") return dark ? colors.yellow[300] : colors.yellow[800];
    if (n.type === "MODULE") return dark ? colors.green[300] : colors.green[800];
    return dark ? colors.blue[300] : colors.blue[800];
  }

  const nodeLabel = (n: CallGraphFunction) => n.label;


  return (
    <div ref={ref} css={[styles, tw`flex max-h-full`, InteriorBorder]}>
      <Script
        type="text/javascript"
        src="ttps://visjs.github.io/vis-network/standalone/umd/vis-network.min.js"
      />
      {data ? (
        <VisSingleContainer data={data} height={height} width={width}>
          <VisGraph
            nodeIcon={nodeIcon}
            nodeFill={nodeFill}
            nodeStroke={nodeStroke}
            nodeStrokeWidth={1}
            nodeLabel={nodeLabel}
          />
        </VisSingleContainer>
      ) : (
        <Center>
          {error ? (
            <div>
              <IconWrapper
                color="dark"
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
