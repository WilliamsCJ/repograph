// Icon-related components

import React from "react";

import tw, { TwStyle } from "twin.macro";

// Icon styling
export const StrongIcon = tw`stroke-zinc-900 dark:stroke-zinc-100`;
export const NormalIcon = tw`stroke-zinc-800 dark:stroke-zinc-200`;
export const DetailIcon = tw`stroke-zinc-700 dark:stroke-zinc-300`;

/**
 * Props for IconWrapper component
 */
export type IconWrapperProps = {
  additional?: TwStyle;
  size: "sm" | "md" | "lg" | "xl";
  color: "strong" | "normal" | "detail";
  icon: any;
};

/**
 * Provides styling and sizing utilities for Heroicons Icons.
 * @param size
 * @param color
 * @param icon
 * @param additional
 * @constructor
 */
const IconWrapper: React.FC<IconWrapperProps> = ({
  size,
  color,
  icon,
  additional,
}) => {
  const sizes = {
    sm: tw`h-4 w-4`,
    md: tw`h-6 w-6`,
    lg: tw`h-8 w-8 font-light`,
    xl: tw`h-12 w-12`,
  };
  const colors = {
    strong: StrongIcon,
    normal: NormalIcon,
    detail: DetailIcon,
  };

  return (
    <div css={[sizes[size], colors[color], tw`m-auto`, additional]}>{icon}</div>
  );
};

export default IconWrapper;
