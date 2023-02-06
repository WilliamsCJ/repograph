import React, { Dispatch, SetStateAction } from "react";

// Styling
import tw from "twin.macro";

// Components
import { TextButton } from "../../core/button";
import { Text, TextLight } from "../../core/text";

/**
 * Props for Pagination component
 */
export type PaginationProps = {
  limit: number;
  offset: number;
  setOffset: Dispatch<SetStateAction<number>>;
  total: number;
};

/**
 * Pagination controls and information
 * @param limit
 * @param offset
 * @param setOffset
 * @param total
 * @constructor
 */
const Pagination: React.FC<PaginationProps> = ({
  limit,
  offset,
  setOffset,
  total,
}) => {
  return (
    <nav tw="flex items-center justify-between py-4" aria-label="Pagination">
      <div tw="hidden sm:block">
        <TextLight>
          Showing <Text as={"span"}>{offset + 1}</Text> to{" "}
          <Text as={"span"}>{Math.min(limit + offset, total)}</Text> of{" "}
          <Text as={"span"}>{total}</Text> results
        </TextLight>
      </div>
      <div tw="flex flex-1 justify-between sm:justify-end space-x-2">
        <TextButton
          onClick={() => {
            if (offset !== 0) setOffset(offset - limit);
          }}
        >
          Previous
        </TextButton>
        <TextButton
          onClick={() => {
            if (offset + limit <= total) setOffset(offset + limit);
          }}
        >
          Next
        </TextButton>
      </div>
    </nav>
  );
};

export { Pagination };
