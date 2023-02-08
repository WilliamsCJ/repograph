import React from "react";

// Styling and base components
import { Tab } from "@headlessui/react";
import tw from "twin.macro";
import {
  AccentBackground,
  AccentBorder,
  AccentText,
  Border,
  Focus,
  SelectedTab,
  UnselectedTab,
} from "./constants";

/**
 * TabGroupProps for TabGroup component.
 */
export type TabGroupProps = {
  titles: string[];
  panels: any[];
};

/**
 * TabGroup
 * @param titles {string[]} The tab titles
 * @param panels {any[]} The components for each tab
 * @constructor
 */
const TabGroup: React.FC<TabGroupProps> = ({ titles, panels }) => {
  return (
    <div tw="min-w-full max-w-md px-2 sm:px-0">
      <Tab.Group defaultIndex={0}>
        <Tab.List>
          {titles.map((title, index) => (
            <Tab
              key={title}
              css={[
                SelectedTab,
                UnselectedTab,
                Focus,
                tw`px-3 py-2 font-medium text-sm rounded-md`,
                // tw`ui-not-selected:(text-gray-500 hover:text-emerald-700)`,
              ]}
            >
              {title}
            </Tab>
          ))}
        </Tab.List>
        <Tab.Panels>
          {panels.map((panel, index) => (
            <Tab.Panel>{panel}</Tab.Panel>
          ))}
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};

export { TabGroup };
