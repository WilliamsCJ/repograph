// Empty state component.

import React from "react";

import tw from "twin.macro";

import { Text, TextLight } from "./text";
import { IconWrapper } from "./icon";
import { Button } from "./button";

/**
 * EmptyStateProps for EmptyState component.
 */
export type EmptyStateProps = {
  icon: any;
  heading: string;
  description: string;
  buttonText: string;
  buttonIcon: any;
};


/**
 * EmptyState component
 * @param props
 * @constructor
 */
const EmptyState: React.FC<EmptyStateProps> = (props) => {
  return (
    <div tw="w-full h-full flex text-center border-dashed">
      <div tw="m-auto text-center">
        <IconWrapper size="lg" color="light" icon={props.icon} />
        <Text tw="mt-2">{props.heading}</Text>
        <TextLight tw="mt-2">{props.description}</TextLight>
        <div tw="mt-6">
          <Button icon={props.buttonIcon} text={props.buttonText} />
        </div>
      </div>
    </div>
  );
};

export { EmptyState };
