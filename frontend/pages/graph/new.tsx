import React from 'react';
import { NextPage } from "next";
import { DefaultLayout } from "../../components/core/layout";
import tw from 'twin.macro';
import { Button } from "../../components/core/button";
import { CheckIcon, CloudArrowUpIcon } from "@heroicons/react/24/outline";
import { Card } from "../../components/core/card";
import { Title, Text, Heading, TextLight } from "../../components/core/text";
import { FileUploadSection, InputSection, TextAreaSection } from "../../components/core/form";
import { Formik, Form, FormikProps } from "formik";

interface NewGraphFormValues {
  name: string
  description: string
  files: any[]
}

interface NewGraphFormErrors {
  name?: string
  description?: string
  files?: string
}

const New: NextPage = () => {
  const initialValues: NewGraphFormValues = {
    name: '',
    description: '',
    files: []
  }

  return (
  <DefaultLayout
  buttons={[]}
  heading="Create Graph"
  >
    <Formik
      initialValues={initialValues}
      onSubmit={(values, actions) => {
        alert(JSON.stringify(values))
      }}
      validate={(values) => {
        const errors: NewGraphFormErrors = {};

        if (!values.name) {
          errors.name = 'Please give your graph a name';
        }

        if (!values.description) {
          errors.description = 'Please provide a description';
        }

        if (!values.files || values.files.length === 0) {
          errors.files = 'You must upload at least one repository';
        }

        return errors
      }}
    >
      <Form tw="max-h-full overflow-clip">
        <div tw="w-full bg-red-100 min-h-full grid grid-cols-2 grid-rows-2 gap-8">
          <Card size={tw`w-full max-h-full row-span-2 col-span-2 px-6 py-6 overflow-hidden`}>
            <div tw="space-y-6">
              <div>
                <Heading>1. Add Graph Information</Heading>
                <TextLight tw="mt-1">Describe the purpose of your graph.</TextLight>

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
                <TextLight tw="mt-1">Add repositories you wish to add to the graph.</TextLight>
                <FileUploadSection
                id="files"
                name="files"
                label="Repositories"
                helpMessage="ZIP files up to 30MB"
                errorMessage="Please upload a file."
                />
              </div>

              <div tw="pt-6">
                <Button primary text="Create"/>
              </div>

            </div>
          </Card>
        </div>
      </Form>
    </Formik>
  </DefaultLayout>
  )
}

export default New;
