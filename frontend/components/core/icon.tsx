// Icon-related components

import React from "react";

import tw, { TwStyle } from "twin.macro";

export type IconWrapperProps = {
  additional: TwStyle;
  size: "sm" | "md" | "lg";
  color: "light" | "dark";
  icon: any;
};

const IconWrapper: React.FC<IconWrapperProps> = ({
  size,
  color,
  icon,
  additional,
}) => {
  const sizes = { sm: tw`h-5 w-5`, md: tw`h-12 w-12`, lg: tw`h-12 w-12` };
  const colors = { light: tw`text-gray-400`, dark: tw`text-gray-700` };

  return (
    <div css={[sizes[size], colors[color], tw`mx-auto`, additional]}>
      {icon}
    </div>
  );
};

export { IconWrapper };
