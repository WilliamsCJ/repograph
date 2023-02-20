import React from "react";

/* Next */
import Script from "next/script";

/* Styling */
import tw, { TwStyle } from "twin.macro";
const colors = require('tailwindcss/colors')

/* External dependencies */
import ClipLoader from "react-spinners/ClipLoader";
import useDimensions from "react-use-dimensions";
import { VisGraph, VisSingleContainer } from "@unovis/react";
import { useTheme } from "next-themes";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";

/* Components */
import { InteriorBorder } from "./constants";
import { Center } from "./layout";
import IconWrapper from "./icon";
import { BoldDetailText } from "./text";

/* Types */
import { CallGraph, CallGraphFunction, CallGraphRelationship } from "../../types/graph";

/**
 * GraphCard props
 */
type GraphCardProps = {
  data: CallGraph;
  error: boolean;
  styles?: TwStyle;
  root_id: number;
};

/**
 * Card to display graph of data.
 * @param data
 * @param styles
 * @param error
 * @param root_id
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

  console.log(data)

  const nodeIcon = (n: CallGraphFunction) => {
    if (n.type === "Method") return 'Me';
    if (n.type === "Class") return 'C';
    if (n.type === "Module") return 'Mo';
    return 'F';
  }

  const nodeFill = (n: CallGraphFunction) => {
    if (n.id == root_id) {
      if (n.type === "Method") return dark ? colors.purple[400] : colors.purple[100];
      if (n.type === "Class") return dark ? colors.yellow[400] : colors.yellow[100];
      if (n.type === "Module") return dark ? colors.green[400] : colors.green[100];
      return dark ? colors.blue[400] : colors.blue[100];
    } else {
      return colors.zinc[200]
    }
  }

  const nodeStroke = (n: CallGraphFunction) => {
    if (n.type === "Method") return dark ? colors.purple[300] : colors.purple[800];
    if (n.type === "Class") return dark ? colors.yellow[300] : colors.yellow[800];
    if (n.type === "Module") return dark ? colors.green[300] : colors.green[800];
    return dark ? colors.blue[300] : colors.blue[800];
  }

  const linkLabel = (l: CallGraphRelationship) => ({
    text: l.type
  })


  const nodeLabel = (n: CallGraphFunction) => n.name;

  console.log(data)

  return (
    <div ref={ref} css={[styles, tw`flex h-14`, InteriorBorder]}>
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
            linkFlow={true}
            linkFlowParticleSize={3}
            linkFlowAnimDuration={10000}
            // @ts-ignore
            linkLabel={linkLabel}
            linkWidth={2}
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
