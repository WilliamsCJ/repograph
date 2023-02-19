import React, { Dispatch, SetStateAction, useRef, useState } from 'react';

// Next.js
import { useRouter } from "next/router";

// Styling
import 'twin.macro';

// Components
import Modal from "../core/modal";
import { Button, RedButton } from "../core/button";
import { deleteGraph } from "../../lib/delete";

/**
 * Props for DeleteModal component
 */
type DeleteModalProps = {
  graphName: string
  open: boolean
  setOpen: Dispatch<SetStateAction<boolean>>
}

/**
 * Specific modal for warning on graph deletion
 * @param graphName
 * @param open
 * @param setOpen
 * @constructor
 */
const DeleteModal: React.FC<DeleteModalProps> = ({ graphName, open, setOpen }) => {
  const cancelButtonRef = useRef(null);
  const router = useRouter();

  return (
    <Modal
      open={open}
      setOpen={setOpen}
      cancelButtonRef={cancelButtonRef}
      title="Delete Graph"
      description="Are you sure you want to delete this graph? It cannot be recovered."
    >
      <div tw="flex flex-row space-x-4">
        <Button
          text="Cancel"
          onClick={() => setOpen(false)}
        />
        <RedButton
          text="Delete"
          onClick={async () => {
            await deleteGraph(graphName)
            setOpen(false)
            await router.push("/")
          }}
          ref={cancelButtonRef}
        />
      </div>
    </Modal>
  )
}

/**
 * Delete graph button
 * @constructor
 */
const DeleteGraphButton = ({ graphName }: { graphName: string }) => {
  const [ modalOpen, setModalOpen ] = useState(false);

  return (
    <>
      <RedButton
        text="Delete"
        onClick={() => setModalOpen(true)}/>
      <DeleteModal
        graphName={graphName}
        open={modalOpen}
        setOpen={setModalOpen}
      />
    </>
  )
}

export default DeleteGraphButton;