// Icon-related components

import React from "react";

import tw, { TwStyle } from "twin.macro";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

// Icon styling
export const StrongIcon = tw`text-zinc-900 dark:text-zinc-100`;
export const NormalIcon = tw`text-zinc-800 dark:text-zinc-200`;
export const DetailIcon = tw`text-zinc-700 dark:text-zinc-300`;
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

export const SearchBarIcon = () => (
  <MagnifyingGlassIcon
    tw="pointer-events-none absolute top-3.5 left-4 h-5 w-5 text-gray-400"
    aria-hidden="true"
  />
)

export default IconWrapper;
