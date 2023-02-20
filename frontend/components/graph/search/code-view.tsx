import React, { Dispatch, SetStateAction, useRef } from "react";
import Modal from "../../core/modal";
import { CodeBlock } from "../../core/code";

export type CodeViewModalProps = {
  source_code: string;
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
};

const CodeViewModal: React.FC<CodeViewModalProps> = ({
  source_code,
  open,
  setOpen,
}) => {
  const cancelButtonRef = useRef(null);

  return (
    <Modal
      open={open}
      setOpen={setOpen}
      cancelButtonRef={cancelButtonRef}
      title="Code View"
    >
      <CodeBlock source_code={source_code} hideScrollBar={false} />
    </Modal>
  );
};

export default CodeViewModal;
