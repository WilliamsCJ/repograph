import tw from "twin.macro";
import React from "react";

/**
 * Heading text, used at the top of pages.
 * @constructor
 */
const Title = tw.h1`font-semibold text-3xl align-text-top text-gray-900`;
const Heading = tw.h2`font-medium text-lg text-gray-900`;
const SmallHeading = tw.h2`text-sm font-semibold text-gray-900`;
const Text = tw.h3`text-sm font-medium text-gray-700`;
const BlockText = tw.h4`block text-sm font-medium text-gray-700`;
const BlockTextLight = tw.p`block text-sm text-gray-700`;
const TextAccent = tw.h3`text-sm font-medium text-primary-600`;

const BlockTextAccent = tw.h3`block text-xs font-medium text-primary-700`;

const TextLight = tw.p`text-sm text-gray-500`;

export { Title, Heading, SmallHeading, Text, BlockText, BlockTextLight, BlockTextAccent, TextAccent, TextLight };
