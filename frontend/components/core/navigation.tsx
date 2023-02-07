import tw, { TwStyle } from "twin.macro";
import { SideBar } from "./layout";
import Link from "next/link";

import { Graph } from "phosphor-react";
import { useEffect, useState } from "react";
import IconWrapper from "./icon";
import { MoonIcon, SunIcon } from "@heroicons/react/24/outline";
import { useTheme } from "next-themes";
import colors from "tailwindcss/colors";

/**
 * Props for NavIcon Component
 */
export type NavIconProps = {
  href: string;
  icon: any;
  active: boolean;
};

/**
 * Icon in the Navigation Bar. Provides link to respective page.
 * @param icon
 * @param href
 * @param active
 * @constructor
 */
const NavIcon = ({ icon, href, active }: NavIconProps) => {
  return (
  <Link href={href}>
    <div tw="flex flex-col">
      <div tw="p-2 flex flex-col m-auto w-10 h-full rounded-lg space-y-2 hover:bg-zinc-200 dark:hover:bg-zinc-700">
        <IconWrapper size="md" color="strong" icon={icon}/>
        {active &&  <div tw="h-2 w-2 m-auto">
            <svg className="h-2 w-2 fill-transparent" fill="currentColor" viewBox="0 0 8 8">
                <circle cx={4} cy={4} r={3}/>
            </svg>
        </div>}
      </div>
    </div>
  </Link>
  );
}

/**
 * Repograph logo for navigation bar. Also a link to the homepage.
 * @constructor
 */
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

/**
 * Toggle switch for dark mode.
 * @constructor
 */
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

/**
 * Navigation route used in NavigationBarProps
 */
export type NavigationRoute = {
  description: string;
  href: string;
  icon: any;
};

/**
 * Props for NavigationBar
 */
export type NavigationBarProps = {
  routes: NavigationRoute[];
  currentPath: string;
  graphName: string | string[] | undefined;
};

/**
 * Navigation sidebar component. Displayed on the side of the screen and contains links.
 * @param routes
 * @param currentPath
 * @param graphName
 * @constructor
 */
const NavigationBar = ({ routes, currentPath, graphName }: NavigationBarProps) => {
  return (
    <SideBar>
      <div tw="flex flex-col justify-between h-full">
        <div tw="flex flex-col space-y-8">
          <NavLogo/>
          <div tw="flex flex-col space-y-4">
            {currentPath !== "/" && currentPath !== "/graph/new" &&
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
