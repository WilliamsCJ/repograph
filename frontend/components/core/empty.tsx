// Empty state component.

import React from "react";

import tw from "twin.macro";

import { DetailText, Text } from "./text";
import IconWrapper from "./icon";
import { LinkButton } from "./button";

/**
 * EmptyStateProps for EmptyState component.
 */
export type EmptyStateProps = {
  icon: any;
  heading: string;
  href: string
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
        <IconWrapper size="lg" color="detail" icon={props.icon} />
        <Text tw="mt-2">{props.heading}</Text>
        <DetailText tw="mt-2">{props.description}</DetailText>
        <div tw="mt-6">
          <LinkButton icon={props.buttonIcon} text={props.buttonText} href={props.href} />
        </div>
      </div>
    </div>
  );
};

export { EmptyState };
