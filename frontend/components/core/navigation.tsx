import tw from "twin.macro";
import { SideBar } from "./layout";
import Link from "next/link";

import { Graph } from "phosphor-react";
import { useEffect, useState } from "react";
import IconWrapper from "./icon";
import { MoonIcon, SunIcon } from "@heroicons/react/24/outline";
import { useTheme } from "next-themes";
import colors from "tailwindcss/colors";
import { act } from "react-dom/test-utils";
import graph from "./graph";

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
  graphName: string | string[] | undefined;
};

const NavIcon = ({ icon, href, active }: NavIconProps) => {
  return (
    <Link href={href}>
      <div tw="flex h-10">
        <div
          css={[
            tw`flex m-auto w-10 h-full rounded-lg space-y-4`,
            active ? tw`bg-gray-100 hover:bg-gray-200` : tw`hover:bg-gray-200`,
          ]}
        >
          <IconWrapper size="md" color="strong" icon={icon} />
        </div>
      </div>
    </Link>
  );
};

const NavLogo = () => {
  const [active, setActive] = useState(false);
  const { theme } = useTheme();

  return (
    <Link
      href="/"
      onMouseEnter={() => setActive(true)}
      onMouseLeave={() => setActive(false)}
      tw="flex h-10 items-center justify-center hover:cursor-pointer"
    >
      <Graph
        size={36}
        color={theme === "dark" ? colors.white : colors.zinc[800]}
        weight={active ? "duotone" : "light"}
      />
    </Link>
  );
};

const DarkModeToggle = () => {
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  // useEffect only runs on the client, so now we can safely show the UI
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <>
      <button
        aria-label="Toggle dark mode"
        type="button"
        tw="dark:hidden"
        onClick={() => setTheme("dark")}
      >
        <IconWrapper size="md" color="strong" icon={<MoonIcon />} />
      </button>
      <button
        tw="hidden dark:block"
        aria-label="Toggle dark mode"
        type="button"
        onClick={() => setTheme("light")}
      >
        <IconWrapper size="md" color="detail" icon={<SunIcon />} />
      </button>
    </>
  );
};

const NavigationBar = ({ routes, currentPath, graphName }: NavigationBarProps) => {
  console.log(currentPath)
  console.log(graphName)
  return (
    <SideBar>
      <div tw="flex flex-col justify-between h-full">
        <div tw="flex flex-col space-y-8">
          <NavLogo/>
          <div tw="flex flex-col space-y-4">
            {currentPath !== "/" &&
            routes.map((route, index) => (
              <NavIcon
              key={index}
              href={`/graph/${graphName}` + route.href}
              icon={route.icon}
              active={currentPath === '/graph/[name]' ? route.href === '/' : currentPath.endsWith(route.href)}
              />
            ))
            }
          </div>
        </div>
        <DarkModeToggle/>
      </div>
    </SideBar>
)};

export default NavigationBar;
