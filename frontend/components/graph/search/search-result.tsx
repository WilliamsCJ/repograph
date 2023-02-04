import React from "react";

import tw from "twin.macro";

// Components
import { Card } from "../../core/card";
import { BlockText } from "../../core/text";

// Types
import { SearchResult } from "../../../types/search";
import { JustifiedRow } from "../../core/layout";

// Syntax highlighting
import "highlight.js/styles/github.css";
import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
hljs.registerLanguage("python", python);

export type SearchResultCardProps = {
  result: SearchResult;
  index: number;
};

const SearchResultCard: React.FC<SearchResultCardProps> = ({
  result,
  index,
}) => {
  const code = result.function.source_code
    ? hljs.highlight(result.function.source_code, { language: "python" }).value
    : undefined;

  return (
    <div tw="w-full">
      <JustifiedRow tw="mb-1 mx-2">
        <BlockText>{`${result.repository} > ${result.function.canonical_name}`}</BlockText>
        <BlockText>{`#${index} (${result.score})`}</BlockText>
      </JustifiedRow>
      <Card size={tw`w-full h-56`}>
        <div tw="w-full h-full grid grid-cols-3 grid-rows-1 divide-x">
          <div tw="py-1 px-2">
            <div tw="mb-2">
              <p tw="contents text-sm font-semibold text-gray-900">Details</p>
            </div>
            <div tw="flex flex-col space-y-2">
              <p tw="block text-sm font-medium text-gray-700">
                Type{" "}
                <span tw="inline-flex items-center rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-800">
                  METHOD
                </span>{" "}
                <span tw="inline-flex items-center rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-800">
                  METHOD
                </span>
              </p>
              <p tw="block text-sm font-medium text-gray-700">
                Line numbers <span tw="text-sm text-gray-700">12-14</span>
              </p>
              <p tw="block text-sm font-medium text-gray-700">Summary</p>
              <p tw="block text-sm text-gray-700">{result.summarization}</p>
            </div>
          </div>
          <div tw="px-2 max-h-full my-2 flex flex-col space-y-2 ">
            <p tw="block text-sm font-medium text-gray-700">Source Code</p>
            <pre tw="text-xs mt-1 pb-6 max-h-full max-w-full overflow-x-auto scrollbar-hide overflow-y-auto p-1 border rounded-lg grow">
              {code && <code dangerouslySetInnerHTML={{ __html: code }} />}
            </pre>
            <a tw="block text-xs font-medium text-primary-700">Expand</a>
          </div>
          <div tw="py-1 px-2">
            <p tw="block text-sm font-medium text-gray-700">Subgraph</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export { SearchResultCard };
