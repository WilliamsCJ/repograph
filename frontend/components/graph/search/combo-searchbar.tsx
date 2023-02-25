import React, { Fragment, useState } from 'react';
import { SearchBarProps } from "./searchbar";
import"twin.macro";
import { ComboSearchBarInputSection } from "../../core/form";
import { Button } from "../../core/button";
import { Form, Formik } from "formik";

export type ComboSearchBarProps = {
  options?: string[]
} & SearchBarProps;

type ComboSearchBarValues = {
  query: string;
};

type ComboSearchBarErrors = {
  query?: string;
};

const people = [
  'Durward Reynolds',
  'Kenton Towne',
  'Therese Wunsch',
  'Benedict Kessler',
  'Katelyn Rohan',
]

const ComboSearchBar: React.FC<ComboSearchBarProps> = (props) => {
  const initialValues: ComboSearchBarValues = {
    query: "",
  };

  const [query, setQuery] = useState('')

  const filteredQueries =
    query === ''
      ? people
      : people.filter((person) => {
        return person.toLowerCase().includes(query.toLowerCase())
  })

  return (
    <Formik
      // @ts-ignore
      initialValues={initialValues}
      // @ts-ignore
      onSubmit={async (values, actions) => {
        alert(values)
        // props.executeQuery(values.query);
      }}
      validate={(values) => {
        const errors: ComboSearchBarErrors = {};

        if (!values.query) {
          errors.query = "Please enter a query";
        }

        return errors;
      }}
    >
      <Form>
        <div tw="flex flex-row grid grid-cols-8 gap-4 items-start mt-6 justify-between">
          <ComboSearchBarInputSection
          id="query"
          name="query"
          label={props.label}
          placeholder={props.placeholder}
          options={people}
          />
          <div tw="col-span-1 mt-1">
            <Button text="Search" />
          </div>
        </div>
      </Form>
    </Formik>
  )
}

export default ComboSearchBar;