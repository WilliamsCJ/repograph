import tw from "twin.macro";
import React from "react";

/**
 * Heading text, used at the top of pages.
 * @constructor
 */
export const Title = tw.h1`text-3xl font-semibold align-text-top text-zinc-900 dark:text-zinc-100`;
export const Heading = tw.h2`text-lg font-medium text-zinc-900 dark:text-zinc-100`;
export const SmallHeading = tw.h3`text-base font-semibold text-zinc-900 dark:text-zinc-100`;
export const Text = tw.p`text-base font-medium text-zinc-800 dark:text-zinc-200`;
export const DetailText = tw.p`text-sm text-zinc-700 dark:text-zinc-300`;
export const BoldDetailText = tw.h4`text-sm font-medium text-zinc-700 dark:text-zinc-300`;
export const NumericalValue = tw.p`text-3xl font-semibold tracking-tight text-zinc-800 dark:text-zinc-200`;