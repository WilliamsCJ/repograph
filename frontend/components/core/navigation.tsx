import tw from "twin.macro";
import { SideBar } from "./layout";
import Link from "next/link";

import { Graph } from "phosphor-react";
import { useEffect, useState } from "react";
import IconWrapper from "./icon";
import { MoonIcon, SunIcon } from "@heroicons/react/24/outline";
import { useTheme } from "next-themes";
import colors from "tailwindcss/colors";

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
  const { theme, setTheme } = useTheme();

  return (
    <div
      onMouseEnter={() => setActive(true)}
      onMouseLeave={() => setActive(false)}
      tw="flex h-10 items-center justify-center hover:cursor-pointer"
    >
      <Graph
        size={48}
        color={theme === "dark" ? colors.white : colors.zinc[800]}
        weight={active ? "duotone" : "light"}
      />
    </div>
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
        <IconWrapper size="md" color="dark" icon={<MoonIcon />} />
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

const NavigationBar = ({ routes, currentPath }: NavigationBarProps) => (
  <SideBar>
    <div tw="flex flex-col justify-between h-full">
      <div tw="">
        <NavLogo />
        {currentPath !== "/" &&
          routes.map((route, index) => (
            <NavIcon
              key={index}
              href={route.href}
              icon={route.icon}
              active={route.href === currentPath}
            />
          ))}
      </div>
      <DarkModeToggle />
    </div>
  </SideBar>
);

export default NavigationBar;
