import React from "react";

import tw from "twin.macro";
import { Form, Formik } from "formik";

import { Button } from "../core/button";
import { Card } from "../core/card";
import { FileUploadSection, InputSection, TextAreaSection } from "../core/form";
import { Heading, DetailText } from "../core/text";

/**
 * Form values type for NewGraphForm
 */
interface NewGraphFormValues {
  name: string;
  description: string;
  files: File[];
}

/**
 * Error values type for NewGraphForm
 */
interface NewGraphFormErrors {
  name?: string;
  description?: string;
  files?: string;
}

/**
 *
 * @constructor
 */
const NewGraphForm: React.FC = () => {
  const initialValues: NewGraphFormValues = {
    name: "",
    description: "",
    files: [],
  };

  return (
    <Formik
      initialValues={initialValues}
      // @ts-ignore
      onSubmit={(values, actions) => {
        alert(values.files[0].name);
      }}
      validate={(values) => {
        const errors: NewGraphFormErrors = {};

        if (!values.name) {
          errors.name = "Please give your graph a name";
        }

        if (!values.description) {
          errors.description = "Please provide a description";
        }

        if (!values.files || values.files.length === 0) {
          errors.files = "You must upload at least one repository";
        }

        return errors;
      }}
    >
      <Form tw="max-h-full overflow-clip">
        <div tw="w-full min-h-full grid grid-cols-2 grid-rows-2 gap-8">
          <Card
            size={tw`w-full max-h-full row-span-2 col-span-2 px-6 py-6 overflow-hidden`}
          >
            <div tw="space-y-6">
              <div>
                <Heading>1. Add Graph Information</Heading>
                <DetailText tw="mt-1">
                  Describe the purpose of your graph.
                </DetailText>

                <InputSection
                  id="name"
                  name="name"
                  label="Graph Name"
                  placeholder=""
                  helpMessage="Give your graph a unique name."
                  errorMessage="Please enter a unique name."
                />

                <TextAreaSection
                  id="description"
                  name="description"
                  label="Description"
                  placeholder=""
                  helpMessage="Write a few sentences about your graph."
                  errorMessage="Please add a few sentences about your graph."
                />
              </div>

              <div tw="border-t pt-6">
                <Heading>2. Upload Repositories</Heading>
                <DetailText tw="mt-1">
                  Add repositories you wish to add to the graph.
                </DetailText>
                <FileUploadSection
                  id="files"
                  name="files"
                  label="Repositories"
                  helpMessage="ZIP files up to 30MB"
                  errorMessage="Please upload a file."
                />
              </div>

              <div tw="pt-6">
                <Button primary text="Create" />
              </div>
            </div>
          </Card>
        </div>
      </Form>
    </Formik>
  );
};

export default NewGraphForm;
