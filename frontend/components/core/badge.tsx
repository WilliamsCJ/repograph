import React from "react";
import tw from "twin.macro";

const Badge = tw.span`inline-flex items-center rounded px-2 py-0.5 text-xs font-medium`;

const FunctionBadge = () => (
  <Badge tw="mt-2 bg-blue-100 text-blue-800 dark:(bg-blue-400/25 text-blue-300)">
    Function
  </Badge>
);
const MethodBadge = () => (
  <Badge tw="mt-2 bg-purple-100 text-orange-800 dark:(bg-purple-400/25 text-purple-300)">
    Method
  </Badge>
);
const ClassBadge = () => (
  <Badge tw="mt-2 bg-yellow-100 text-yellow-800 dark:(bg-yellow-400/25 text-yellow-300)">
    Class
  </Badge>
);
const BuiltInBadge = () => (
  <Badge tw="mt-2 bg-orange-100 text-orange-800 dark:(bg-orange-400/25 text-orange-300)">
    Built-in
  </Badge>
);

export { FunctionBadge, MethodBadge, ClassBadge, BuiltInBadge };
