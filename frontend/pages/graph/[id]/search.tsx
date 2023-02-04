import { NextPage } from "next";
import { DefaultLayout } from "../../../components/core/layout";

import tw from "twin.macro";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

import { Tab } from "@headlessui/react";
import React from "react";
import { Button } from "../../../components/core/button";

const Input = tw.input`
  block w-full min-w-0 rounded-lg shadow-sm border p-4
  text-gray-700 placeholder-gray-300 border-gray-300
  focus:border-primary-500 focus:ring-primary-500
`;

export type SearchBarProps = {
  placeholder: string;
};

const SearchBar: React.FC<SearchBarProps> = ({ placeholder }) => {
  return (
    <div tw="grid grid-cols-8 gap-4 items-center mt-6">
      <div tw="relative col-span-4 sm:col-span-5 md:col-span-7">
        <div tw="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
          <MagnifyingGlassIcon tw="h-6 w-6" />
        </div>
        <input
          id="default-search"
          tw="block w-full p-4 pl-12 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white
          focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400
          dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500
          "
          placeholder={placeholder}
          required
          onChange={()}
        />
      </div>
      <div tw="col-span-1">
        <Button type="submit" text="Search" primary={true} />
      </div>
    </div>
  );
};

export function SearchTabs() {
  let options = ["Natural", "Favourites", "Manual"];
  let searchBars = [
    { placeholder: "Functions that do..." },
    { placeholder: "Select a query" },
    { placeholder: "MATCH ()-[]-() RETURN ..." },
  ];

  return (
    <div className="w-full max-w-md px-2 sm:px-0">
      <Tab.Group defaultIndex={1}>
        <Tab.List>
          {options.map((option, index) => (
            <Tab
              key={index}
              css={[
                tw`px-3 py-2 font-medium text-sm rounded-md`,
                tw`ui-selected:(bg-indigo-100 text-indigo-700)`,
                tw`ui-not-selected:(text-gray-500 hover:text-gray-700)`,
              ]}
            >
              {option}
            </Tab>
          ))}
        </Tab.List>
        <Tab.Panels>
          {searchBars.map((searchBar, index) => (
            <Tab.Panel>
              <SearchBar key={index} placeholder={searchBar.placeholder} />
            </Tab.Panel>
          ))}
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
}

const Search: NextPage = () => {
  return (
    <DefaultLayout buttons={[]} heading="Search">
      <SearchTabs />
    </DefaultLayout>
  );
};

export default Search;
