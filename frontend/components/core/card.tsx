import React from "react";

/* External dependencies */
import tw, { TwStyle } from "twin.macro";
import {
  Background,
  Border,
  GreenBackground,
  GreenBorder,
  RedBackground,
  RedBorder,
} from "./constants";

/**
 * Props for all Card components.
 */
type CardProps = {
  children: React.ReactNode;
  ref?: string;
};

/**
 * Props for the DefaultCard component.
 */
type DefaultCardProps = CardProps & {
  size?: TwStyle;
};

/**
 * Generic card.
 * Should NOT be exported, as requires defined size
 * @constructor
 * @param children
 * @param props
 */
export const Card: React.FC<DefaultCardProps> = ({ children, ...props }) => (
  <div ref={props.ref} css={[Background, Border, props.size]}>
    {children}
  </div>
);

/**
 * Green card for success.
 * @constructor
 * @param children
 * @param props
 */
const GreenCard: React.FC<DefaultCardProps> = ({ children, ...props }) => (
  <div ref={props.ref} css={[GreenBackground, GreenBorder, props.size]}>
    {children}
  </div>
);

/**
 * Red card for errors
 * @constructor
 * @param children
 * @param props
 */
const RedCard: React.FC<DefaultCardProps> = ({ children, ...props }) => (
  <div ref={props.ref} css={[RedBackground, RedBorder, props.size]}>
    {children}
  </div>
);

export { GreenCard, RedCard };
