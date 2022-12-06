import React from 'react';

/* External dependencies */
import tw, { TwStyle } from 'twin.macro';


/**
 * Props for all Card components.
 */
type CardProps = {
  children: React.ReactNode
  ref?: string
}


/**
 * Props for the DefaultCard component.
 */
type DefaultCardProps = CardProps & {
  size: TwStyle
}


/**
 * Generic card.
 * Should NOT be exported, as requires defined size
 * @constructor
 * @param children
 * @param props
 */
const Card: React.FC<DefaultCardProps> = ({children, ...props}) => (
  <div
    ref={props.ref}
    css={[tw`bg-white rounded-lg border border-gray-300`, props.size]}
  >
    {children}
  </div>
);


/**
 * Full-width card that covers whole width of the container
 * @param children
 * @param props
 * @constructor
 */
const FullWidthCard: React.FC<CardProps> = ({children, ...props}) => (
    <Card {...props} size={tw`w-full h-1/2`}>{children}</Card>
)


export { FullWidthCard, Card };