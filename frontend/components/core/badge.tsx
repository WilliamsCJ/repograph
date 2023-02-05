import React from "react";
import tw from "twin.macro";

const Badge =  tw.span`inline-flex items-center rounded px-2 py-0.5 text-xs font-medium`

const FunctionBadge = () => <Badge tw="bg-blue-100 text-blue-800">Function</Badge>;
const MethodBadge = () => <Badge tw="bg-green-100 text-green-800">Method</Badge>;
const ClassBadge = () => <Badge tw="bg-yellow-100 text-yellow-800">Class</Badge>;
const BuiltInBadge = () => <Badge tw="bg-gray-100 text-gray-800">Built-in</Badge>;

export { FunctionBadge, MethodBadge, ClassBadge, BuiltInBadge }