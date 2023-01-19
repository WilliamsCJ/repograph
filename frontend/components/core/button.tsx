import tw from "twin.macro";
import Link from "next/link";


// Button

/**
 * Props type for Button component.
 */
export type ButtonProps = {
  icon?: any
  text: string
  primary: boolean
};

/**
 * Base Button
 * @param icon {any} Icon to display
 * @param text {string} Button text
 * @param primary
 * @constructor
 */
const Button = ({ icon, text, primary }: ButtonProps) => {
  const color = primary ? tw`bg-primary-500 text-white hover:bg-primary-600 border-transparent` : tw`bg-white hover:bg-gray-50 text-gray-700 border-gray-300`;

  return (
    <button
      css={[
        color,
        tw`h-10 w-28 mx-auto flex flex-row justify-center items-center space-x-2`,
        tw`rounded-md border text-sm font-semibold shadow-sm`,
        tw`px-4 py-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500`
      ]}
    >
      {icon && <div tw="h-5 w-5">{icon}</div>}
      <span>{text}</span>
    </button>
  );
};


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