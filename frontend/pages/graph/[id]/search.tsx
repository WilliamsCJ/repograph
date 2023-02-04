import { NextPage } from "next";
import { DefaultLayout } from "../../../components/core/layout";

import tw from "twin.macro";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

import { Tab } from "@headlessui/react";
import React, { useState } from "react";

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
  const [results, setResults] = useState([]);

  return (
    <DefaultLayout buttons={[]} heading="Search">
      <SearchTabs />
      {/* TODO: Render results */}
    </DefaultLayout>
  );
};

export default Search;
