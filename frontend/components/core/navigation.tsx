import tw from "twin.macro";
import { SideBar } from "./layout";
import Link from "next/link";

import { Graph } from "phosphor-react"
import { useState } from "react";

export type NavIconProps = {
  href: string;
  icon: any;
  active: boolean;
};

export type NavigationRoute = {
  description: string;
  href: string;
  icon: any;
};

export type NavigationBarProps = {
  routes: NavigationRoute[];
  currentPath: string;
};

const NavIcon = ({ icon, href, active }: NavIconProps) => {
  return (
    <Link href={href}>
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

const NavLogo = () => {
  const [active, setActive] = useState(false);

  return (
    <div
      onMouseEnter={() => setActive(true)}
      onMouseLeave={() => setActive(false)}
      tw="flex h-10 items-center justify-center hover:cursor-pointer"
    >
      <Graph size={48} color="#454545" weight={active ? "duotone" : "light"} />
    </div>
  )
}


const NavigationBar = ({ routes, currentPath }: NavigationBarProps) => (
  <SideBar>
    <NavLogo />
    {routes.map((route, index) => (
      <NavIcon
        key={index}
        href={route.href}
        icon={route.icon}
        active={route.href === currentPath}
      />
    ))}
  </SideBar>
);

export default NavigationBar;
