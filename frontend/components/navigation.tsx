import tw from "twin.macro";
import { SideBar } from "./layout";

import {
  HomeIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";

const NavIcon = tw.div`flex h-10`;

const NavigationBar = () => (
  <SideBar>
    <NavIcon>
      <HomeIcon tw="m-auto h-6 w-6" />
    </NavIcon>
    <NavIcon>
      <MagnifyingGlassIcon tw="m-auto h-6 w-6" />
    </NavIcon>
    <NavIcon>
      <ExclamationTriangleIcon tw="m-auto h-6 w-6" />
    </NavIcon>
  </SideBar>
);

export default NavigationBar;
