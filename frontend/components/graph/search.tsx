import React from 'react';

import tw from "twin.macro";
import { Button } from "../core/button";
import { SearchBarInputSection } from "../core/form";
import { Formik, Form } from "formik";

export type SearchBarProps = {
  label: string
  placeholder: string
}

type SearchBarValues = {
  query: string
}

type SearchBarErrors = {
  query?: string
}

const SearchBar: React.FC<SearchBarProps> = (props) => {
  const initialValues: SearchBarValues = {
    query: "",
  };

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={(values, actions) => {

      }}
      validate={(values) => {
        const errors: SearchBarErrors = {};

        if (!values.query) {
          errors.query = "Please enter a query";
        }

        return errors;
      }}
    >
      <Form tw="grid grid-cols-8 gap-4 items-center mt-6">
          <SearchBarInputSection
          id="query"
          name="query"
          label={props.label}
          placeholder={props.placeholder}
          />
          <div tw="col-span-1">
            <Button text="Search" primary={true} />
          </div>
      </Form>
    </Formik>

  )
}