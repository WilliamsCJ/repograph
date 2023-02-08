import React, { useEffect } from "react";

import tw, { TwStyle } from "twin.macro";

// Syntax highlighting
import "highlight.js/styles/stackoverflow-light.css";
import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
hljs.registerLanguage("python", python);

// Components
import { InteriorBorder } from "./constants";

/**
 * Props for the CodeBlock component.
 */
export type CodeBlockProps = {
  source_code: string;
  styles?: TwStyle;
};

/**
 * CodeBlock component
 * @param source_code
 * @param styles
 * @constructor
 */
const CodeBlock: React.FC<CodeBlockProps> = ({ source_code, styles }) => {
  const code = hljs.highlight(source_code, { language: "python" }).value;

  return (
    <>
      <pre
      css={[
        tw`max-h-full max-w-full overflow-x-auto overflow-y-auto scrollbar-hide text-xs p-1`,
        InteriorBorder,
        styles,
      ]}
      >
      {code && <code dangerouslySetInnerHTML={{ __html: code }} />}
    </pre>
    </>
  );
};

export { CodeBlock };
