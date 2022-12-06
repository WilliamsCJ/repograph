import tw from "twin.macro";
import { ButtonProps, LinkButtonProps } from "../../types/components/core/button";
import Link from "next/link";

/**
 * Base Button
 * @param icon {any} Icon to display
 * @param text {string} Button text
 * @constructor
 */
const Button = ({ icon, text }: ButtonProps) => {
  return (
    <button
      tw="flex h-10 flex-row justify-center items-center space-x-2 rounded-md border border-gray-300
        bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2
        focus:ring-indigo-500 focus:ring-offset-2 w-28"
    >
      <div tw="h-5 w-5">{icon}</div>
      <span>{text}</span>
    </button>
  );
};

/**
 * LinkButton redirects to a ReactRouter Link
 * @param href {string} The URL path to redirect to
 * @param children {React.ReactNode[]} Child nodes
 * @param props
 * @constructor
 */
const LinkButton = ({ href, ...props }: LinkButtonProps) => (
  <Link href={href}>
    <Button {...props} />
  </Link>
);

/**
 * ButtonGroup is a horizontal group of Buttons.
 */
const ButtonGroup = tw.div`flex flex-row justify-center space-x-4`;

export { Button, LinkButton, ButtonGroup };
