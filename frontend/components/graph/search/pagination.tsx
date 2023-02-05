import React from "react";

import tw from "twin.macro";

const Pagination = () => {
  return (
  <nav
  tw="flex items-center justify-between py-4"
  aria-label="Pagination"
  >
    <div tw="hidden sm:block">
      <p tw="text-sm text-gray-700">
        Showing <span tw="font-medium">1</span> to <span tw="font-medium">10</span> of{' '}
        <span tw="font-medium">20</span> results
      </p>
    </div>
    <div tw="flex flex-1 justify-between sm:justify-end">
      <a
      href="#"
      tw="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
      >
        Previous
      </a>
      <a
      href="#"
      tw="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
      >
        Next
      </a>
    </div>
  </nav>
  )
}

export { Pagination };