import React from "react";

// Styling
import tw from "twin.macro";

// Prop types
import type { DefaultLayoutProps } from "../types/layout";

// Other components
import { Heading } from "./text";
import { ButtonGroup } from "./button";

/**
 * ApplicationShell wraps the entire application and prevents overscrolling
 */
const ApplicationShell = tw.div`w-screen min-h-screen max-h-screen bg-gray-100`;

/**
 * CenteredLayout centers content both horizontally and vertically
 */
const CenteredLayout = tw.div`m-auto flex flex-col items-center space-y-4`;

/**
 * DefaultLayout is the default page/route layout that contains a header row and then the actual content
 * @param buttons {React.ReactNode[]} Array of Buttons to display on the right
 * @param children {React.ReactNode[]} The child nodes i.e. the content
 * @param heading {string} The page heading
 * @constructor
 */
const DefaultLayout: React.FC<DefaultLayoutProps> = ({
  buttons,
  children,
  heading,
}) => {
  return (
    <RowLayout>
      <HeadingRow>
        <Heading>{heading}</Heading>
        <ButtonGroup>{buttons}</ButtonGroup>
      </HeadingRow>
      {children}
    </RowLayout>
  );
};

/**
 * FullContainer is used to fill the entire height/width of the parent element
 */
const FullContainer = tw.div`flex h-full w-full`;

/**
 * HeadingRow is used for displaying the top row of a page
 */
const HeadingRow = tw.div`flex w-full flex-row justify-between`;

/**
 * MainContainer is the content for the main portion of the application (i.e. not including the sidebar)
 */
const MainContainer = tw.div`flex h-screen w-full flex-col space-y-20 overflow-y-auto overflow-x-hidden overscroll-contain py-8 pl-24 pr-8`;

/**
RowLayout displays an array of components with consistent spacing
 */
const RowLayout = tw.div`flex h-full w-full flex-col space-y-8`;

/**
Fixed sidebar for navigation
 */
const SideBar = tw.div`h-screen w-16 fixed inset-y-0 bg-white border-r-2 flex flex-col py-8 space-y-8`;

/* Export */
export {
  ApplicationShell,
  CenteredLayout,
  DefaultLayout,
  FullContainer,
  MainContainer,
  SideBar,
};
