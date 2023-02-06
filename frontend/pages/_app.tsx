import type { AppProps } from "next/app";
import NavigationBar, { NavigationRoute } from "../components/core/navigation";
import {
  ExclamationTriangleIcon,
  HomeIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";
import { ApplicationShell, MainContainer } from "../components/core/layout";
import GlobalStyles from "../styles/GlobalStyles";
import { useRouter } from "next/router";
import React from "react";
import { Toaster } from "react-hot-toast";

const navigation: NavigationRoute[] = [
  {
    description: "Home",
    href: "/",
    icon: <HomeIcon />,
  },
  {
    description: "Search",
    href: "/search",
    icon: <MagnifyingGlassIcon />,
  },
  {
    description: "Issues",
    href: "/issues",
    icon: <ExclamationTriangleIcon />,
  },
];

function MyApp({ Component, pageProps }: AppProps) {
  const router = useRouter();

  return (
    <>
      <GlobalStyles />
      <ApplicationShell id="shell">
        <Toaster position="top-center" reverseOrder={false} />
        <NavigationBar routes={navigation} currentPath={router.route} />
        <MainContainer>
          <Component {...pageProps} />
        </MainContainer>
      </ApplicationShell>
    </>
  );
}

export default MyApp;
