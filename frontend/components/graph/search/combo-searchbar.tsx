import React, { MutableRefObject, useRef } from "react";

// Styling
import "twin.macro";

// Components
import {
  ComboSearchBarInputSection,
  SelectInputSection,
} from "../../core/form";
import { Button } from "../../core/button";

// Forms
import { Form, Formik } from "formik";

// Types
import { AvailableSearchQuery } from "../../../types/search";
import { SearchBarProps } from "./searchbar";
import { Listbox } from "@headlessui/react";

/**
 * Props for ComboSearchBar component.
 */
export type ComboSearchBarProps = {
  available: AvailableSearchQuery[];
  repositories: string[];
  setRepository: any;
} & SearchBarProps;

/**
 * Formik form values
 */
type ComboSearchBarValues = {
  query: AvailableSearchQuery | null;
  repository: string | null;
};

/**
 * Combobox-style search bar for choosing from a list of available queries.
 * @param props
 * @constructor
 */
const ComboSearchBar: React.FC<ComboSearchBarProps> = (props) => {
  const initialValues: ComboSearchBarValues = {
    query: null,
    repository: null,
  };

  return (
    <Formik
      // @ts-ignore
      initialValues={initialValues}
      // @ts-ignore
      onSubmit={async (values, actions) => {
        props.executeQuery(values.query, values.repository);
      }}
      // @ts-ignore
      innerRef={props.formRef}
    >
      <Form>
        <div tw="flex flex-col sm:flex-row w-full gap-4 items-start mt-6">
          <ComboSearchBarInputSection
            id="query"
            name="query"
            label={props.label}
            placeholder={props.placeholder}
            options={props.available}
          />
          <SelectInputSection
            name="repository"
            id="repository"
            placeholder="All"
            label="Repository"
            options={props.repositories}
            setRepository={props.setRepository}
          />
          <Button text="Search" />
        </div>
      </Form>
    </Formik>
  );
};

export default ComboSearchBar;
