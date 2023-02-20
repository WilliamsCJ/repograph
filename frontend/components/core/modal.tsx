import React, { SetStateAction, Dispatch } from "react";

// Styling
import "twin.macro";

// Dependencies
import { Dialog } from "@headlessui/react";
import { Card } from "./card";
import tw from "twin.macro";
import { DetailText, Heading } from "./text";

/**
 * Props for Modal component.
 */
export type ModalProps = {
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  children: JSX.Element;
  cancelButtonRef: React.MutableRefObject<null>;
  title: string;
  description?: string;
};

/**
 * Generic modal component
 * @param open
 * @param setOpen
 * @param children
 * @param cancelButtonRef
 * @param title
 * @param description
 * @constructor
 */
const Modal: React.FC<ModalProps> = ({
  open,
  setOpen,
  children,
  cancelButtonRef,
  title,
  description,
}) => {
  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
      tw="relative z-50 px-6"
      initialFocus={cancelButtonRef}
    >
      <div tw="fixed inset-0 bg-gray-800 bg-opacity-25 transition-opacity" />
      <div tw="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel>
          <div tw="px-12 py-6 max-h-screen w-screen flex items-center justify-center">
            <Card size={tw`max-h-screen w-full flex flex-col space-y-4 px-6 py-4`}>
              {/* @ts-ignore*/}
              <Heading as={Dialog.Title}>{title}</Heading>
              {/* @ts-ignore*/}
              {description && <DetailText as={Dialog.Description}>{description}</DetailText>}
              {children}
            </Card>
          </div>
        </Dialog.Panel>
      </div>
    </Dialog>
  );
};

export default Modal;
