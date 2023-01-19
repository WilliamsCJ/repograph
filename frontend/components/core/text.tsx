import tw from "twin.macro";
import React from "react";

/**
 * Heading text, used at the top of pages.
 * @constructor
 */
const Heading = tw.h1`font-semibold text-3xl align-text-top`;
const Text = tw.h3`text-sm font-medium`;
const TextLight = tw.p`text-sm text-gray-500`


export { Heading, Text, TextLight };
