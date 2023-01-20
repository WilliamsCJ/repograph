// Empty state component.

import React from "react";

import tw from "twin.macro";

import { Text, TextLight } from "./text";
import { EmptyStateProps } from "../../types/components/core/empty";
import { IconWrapper } from "./icon";
import { Button } from "./button";

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
