import tw from "twin.macro";

const ApplicationShell = tw.body`w-screen min-h-screen max-h-screen bg-gray-100`;

const FullContainer = tw.div`h-full w-full`;

const HeadingRow = tw.div`flex w-full flex-row justify-between`;

const MainContainer = tw.div`flex h-screen w-full flex-col space-y-20 overflow-y-auto overflow-x-hidden overscroll-contain py-8 pl-24 pr-8`;

const MainLayout = tw.div`flex h-full w-full flex-col space-y-8`;

const SideBar = tw.div`h-screen w-16 fixed inset-y-0 bg-white border-r-2 flex flex-col py-8 space-y-8`;

export {
  ApplicationShell,
  FullContainer,
  HeadingRow,
  MainContainer,
  MainLayout,
  SideBar,
};
