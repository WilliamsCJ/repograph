import type { AppProps } from "next/app";
import NavigationBar, { NavigationRoute } from "../components/core/navigation";
import {
  ArrowLeftIcon,
  ExclamationTriangleIcon,
  HomeIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";
import { ApplicationShell, MainContainer } from "../components/core/layout";
import GlobalStyles from "../styles/GlobalStyles";
import { useRouter } from "next/router";
import React from "react";
import { Toaster } from "react-hot-toast";
import { ThemeProvider } from "next-themes";

const navigation: NavigationRoute[] = [
  {
    description: "Summary",
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
  const router = useRouter()
  const { name } = router.query

  return (
    <>
      <GlobalStyles />
      <ThemeProvider attribute="class">
        <ApplicationShell>
          <Toaster position="top-center" reverseOrder={false} />
          <NavigationBar routes={navigation} currentPath={router.route} graphName={name} />
          <MainContainer>
            <Component {...pageProps} />
          </MainContainer>
        </ApplicationShell>
      </ThemeProvider>
    </>
  );
}

export default MyApp;
