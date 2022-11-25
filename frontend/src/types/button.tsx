import React from "react";

export type ButtonProps = {
  icon: any;
  text: string;
};

/**
 * Props type for LinkButton component.
 */
export type LinkButtonProps = ButtonProps & {
  href: string;
};
