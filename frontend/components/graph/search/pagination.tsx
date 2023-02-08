import React, { Dispatch, SetStateAction } from "react";

// Styling
import tw from "twin.macro";

// Components
import { Button, TextButton } from "../../core/button";
import { Text, DetailText, BoldDetailText } from "../../core/text";

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
        <DetailText>
          Showing <BoldDetailText as={"span"}>{offset + 1}</BoldDetailText> to{" "}
          <BoldDetailText as={"span"}>
            {Math.min(limit + offset, total)}
          </BoldDetailText>{" "}
          of <BoldDetailText as={"span"}>{total}</BoldDetailText> results
        </DetailText>
      </div>
      <div tw="flex flex-1 justify-between sm:justify-end space-x-2">
        <Button
          text="Previous"
          onClick={() => {
            if (offset !== 0) setOffset(offset - limit);
          }}
        />
        <Button
          text="Next"
          onClick={() => {
            if (offset + limit <= total) setOffset(offset + limit);
          }}
        >
          Next
        </Button>
      </div>
    </nav>
  );
};

export { Pagination };
