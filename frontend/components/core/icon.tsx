// Icon-related components

import React from "react";

import tw from 'twin.macro';

import { IconWrapperProps } from "../../types/components/core/icon";

const IconWrapper: React.FC<IconWrapperProps> = ({size, color, icon}) => {
  const sizes = { sm: tw`h-6 w-6`, md: tw`h-12 w-12`, lg: tw`h-12 w-12` }
  const colors = { light: tw`text-gray-400`, dark: tw`text-gray-700`}

  return (
    <div css={[sizes[size], colors[color], tw`mx-auto`]}>{icon}</div>
  )
}

export { IconWrapper };
