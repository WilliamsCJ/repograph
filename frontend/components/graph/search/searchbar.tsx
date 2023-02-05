import React from "react";

// Styling
import tw from "twin.macro";

// External dependencies
import { Formik, Form } from "formik";
import toast from 'react-hot-toast';

// Components
import { Button } from "../../core/button";
import { SearchBarInputSection } from "../../core/form";

export type SearchBarProps = {
  label: string;
  placeholder: string;
  executeQuery: any;
  setResults: any;
};

type SearchBarValues = {
  query: string;
};

type SearchBarErrors = {
  query?: string;
};

const SearchBar: React.FC<SearchBarProps> = (props) => {
  const initialValues: SearchBarValues = {
    query: "",
  };

  return (
    <Formik
      initialValues={initialValues}
      // @ts-ignore
      onSubmit={async (values, actions) => {
        try {
          const results = await props.executeQuery("any", values.query);
          props.setResults(results);
        } catch (e) {
          toast.error("An error occurred!", {duration: 6000})
        }
      }}
      validate={(values) => {
        const errors: SearchBarErrors = {};

        if (!values.query) {
          errors.query = "Please enter a query";
        }

        return errors;
      }}
    >
      <Form>
        <div tw="flex flex-row grid grid-cols-8 gap-4 items-center mt-6 justify-between">
          <SearchBarInputSection
            id="query"
            name="query"
            label={props.label}
            placeholder={props.placeholder}
          />
          <div tw="col-span-1">
            <Button text="Search" primary={true} />
          </div>
        </div>
      </Form>
    </Formik>
  );
};

export { SearchBar };
