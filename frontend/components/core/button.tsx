import tw from "twin.macro";

import Link from "next/link";
import {
  AccentBackground,
  AccentBorder,
  AccentHover,
  AccentText,
  Background,
  Border,
  ButtonText,
  Hover,
} from "./constants";
import { DetailText } from "./text";

const ButtonStyles = tw`px-4 py-2 mx-auto flex flex-row justify-center items-center space-x-2`;

// Button

/**
 * Props type for Button component.
 */
export type ButtonProps = {
  icon?: any;
  text: string;
  type?: "submit" | "button";
};

export const Button = ({ icon, text, type }: ButtonProps) => (
  <button
    css={[Background, ButtonText, Border, ButtonStyles, Hover]}
    type={type}
  >
    <span>{text}</span>
  </button>
);

export const AccentButton = ({ icon, text, type }: ButtonProps) => (
  <button
    css={[
      AccentBackground,
      AccentText,
      AccentBorder,
      ButtonStyles,
      AccentHover,
    ]}
    type={type}
  >
    <span>{text}</span>
  </button>
);

// /**
//  * Base Button
//  * @param icon {any} Icon to display
//  * @param text {string} Button text
//  * @param primary
//  * @param type
//  * @constructor
//  */
// const Button = ({ icon, text, primary, type }: ButtonProps) => {
//   return (
//     <button
//       type={type}
//       css={[
//         tw`bg-white bg-emerald-400/25 font-semibold`,
//         tw`text-emerald-600 dark:text-emerald-400 dark:hover:text-emerald-300`,
//         tw`border border-emerald-400 dark:hover:border-emerald-200 dark:border-emerald-700 rounded-lg`,
//         tw`mx-auto flex flex-row justify-center items-center space-x-2`,
//         // tw`focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500`,
//       ]}
//     >
//       <span>{text}</span>
//     </button>
//   );
// };

// Link Button

/**
 * Props type for LinkButton component.
 */
export type LinkButtonProps = ButtonProps & {
  href: string;
};

/**
 * LinkButton redirects to a ReactRouter Link
 * @param href {string} The URL path to redirect to
 * @param children {React.ReactNode[]} Child nodes
 * @param props
 * @constructor
 */
export const LinkButton = ({ href, ...props }: LinkButtonProps) => (
  <Link href={href}>
    <Button {...props} />
  </Link>
);

/**
 * LinkButton redirects to a ReactRouter Link. Accent color.
 * @param href {string} The URL path to redirect to
 * @param children {React.ReactNode[]} Child nodes
 * @param props
 * @constructor
 */
export const AccentLinkButton = ({ href, ...props }: LinkButtonProps) => (
  <Link href={href}>
    <AccentButton {...props} />
  </Link>
);

/**
 * ButtonGroup is a horizontal group of Buttons.
 */
export const ButtonGroup = tw.div`flex flex-row justify-center space-x-4`;

export const TextButton = tw.button`
  relative inline-flex items-center rounded-md border border-gray-300 bg-white
  px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50
 `;
