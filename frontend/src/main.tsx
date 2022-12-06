import React from "react";
import ReactDOM from "react-dom/client";

// Router and routes
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import { Error, Home, Issues, Search } from "./routes";

// Styling
import GlobalStyles from "./styles/GlobalStyles";

// Components
import NavigationBar, { NavigationRoute } from "./components/core/navigation";
import { ApplicationShell, MainContainer } from "./components/core/layout";
import {
  ExclamationTriangleIcon,
  HomeIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";

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

const Layout = () => (
  <ApplicationShell>
    <NavigationBar routes={navigation} />
    <MainContainer>
      <Outlet />
    </MainContainer>
  </ApplicationShell>
);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    {/* Global styles for twin.macro */}
    <GlobalStyles />
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path={"search"} element={<Search />} />
          <Route path={"issues"} element={<Issues />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
