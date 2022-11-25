import React from "react";

// Styling
import "twin.macro";

// Components
import { CenteredLayout, FullContainer } from "../components/layout";
import { Heading } from "../components/text";
import { LinkButton } from "../components/button";

// Icons
import { HomeIcon } from "@heroicons/react/24/outline";

function Error() {
  return (
    <FullContainer>
      <CenteredLayout>
        <Heading>Something went wrong...</Heading>
        <LinkButton href="/" icon={<HomeIcon />} text="Home" />
      </CenteredLayout>
    </FullContainer>
  );
}

export default Error;
