import tw from "twin.macro";
import { SideBar } from "./layout";

import {
  HomeIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";
import { Link, useLocation } from "react-router-dom";

export type NavIconProps = {
  href: string;
  icon: any;
};

export type NavigationRoute = {
  description: string;
  href: string;
  icon: any;
};

export type NavigationBarProps = {
  routes: NavigationRoute[];
};

const NavIcon = ({ icon, href }: NavIconProps) => {
  const location = useLocation();

  const active = location.pathname === href;

  return (
    <Link to={href}>
      <div tw="flex h-10">
        <div
          css={[
            tw`flex m-auto w-10 h-full rounded-lg`,
            active ? tw`bg-gray-100 hover:bg-gray-200` : tw`hover:bg-gray-200`,
          ]}
        >
          <div tw="m-auto h-6 w-6">{icon}</div>
        </div>
      </div>
    </Link>
  );
};

const NavigationBar = ({ routes }: NavigationBarProps) => (
  <SideBar>
    {routes.map((route, index) => (
      <NavIcon href={route.href} icon={route.icon} />
    ))}
  </SideBar>
);

export default NavigationBar;
