import React from 'react';

// Styling
import"twin.macro";

// Components
import { ComboSearchBarInputSection } from "../../core/form";
import { Button } from "../../core/button";

// Forms
import { Form, Formik } from "formik";

// Types
import { AvailableSearchQuery } from "../../../types/search";
import { SearchBarProps } from "./searchbar";

/**
 * Props for ComboSearchBar component.
 */
export type ComboSearchBarProps = {
  available: AvailableSearchQuery[]
} & SearchBarProps;

/**
 * Formik form values
 */
type ComboSearchBarValues = {
  query: AvailableSearchQuery | null;
};

/**
 * Combobox-style search bar for choosing from a list of available queries.
 * @param props
 * @constructor
 */
const ComboSearchBar: React.FC<ComboSearchBarProps> = (props) => {
  const initialValues: ComboSearchBarValues = {
    query: null,
  };

  return (
    <Formik
      // @ts-ignore
      initialValues={initialValues}
      // @ts-ignore
      onSubmit={async (values, actions) => {
        alert(JSON.stringify(values))

        props.executeQuery(values.query);
      }}
    >
      <Form>
        <div tw="flex flex-row grid grid-cols-8 gap-4 items-start mt-6 justify-between">
          <ComboSearchBarInputSection
          id="query"
          name="query"
          label={props.label}
          placeholder={props.placeholder}
          options={props.available}
          />
          <div tw="col-span-1">
            <Button text="Search" />
          </div>
        </div>
      </Form>
    </Formik>
  )
}

export default ComboSearchBar;