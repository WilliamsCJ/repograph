import React from "react";

import tw from 'twin.macro';
import { Field, FieldProps } from "formik";
import { IconWrapper } from "./icon";
import { ArrowUpTrayIcon, FolderPlusIcon } from "@heroicons/react/24/outline";


/**
 * InputProps type for InputSection component.
 */
export type InputProps = {
  id: string
  name: string
  label: string
  placeholder: string
  helpMessage: string
  errorMessage: string
}


/**
 * InputSection component contains a Formik input field
 * along with label, helper text and error handling.
 * @param props
 * @constructor
 */
const InputSection: React.FC<InputProps> = (props) => {
  return <Field
    id={props.id}
    name={props.name}
  >
    {({
        field,
        meta,
      }: FieldProps) => (
        <div tw="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 pt-6">
        {(meta.touched && meta.error) ?
          <>
          <Label>{props.label}</Label>
          <div tw="sm:col-span-2 sm:mt-0">
            <ErrorInput placeholder={props.placeholder} {...field} />
            <ErrorText>{meta.error}</ErrorText>
          </div>
          </>
        :
          <>
          <Label>{props.label}</Label>
            <div tw="sm:col-span-2 sm:mt-0">
              <Input placeholder={props.placeholder} {...field} />
              <HelpText>{props.helpMessage}</HelpText>
            </div>
          </>
        }
        </div>

    )}
  </Field>
}


/**
 * TextAreaProps type for TextAreaSection component.
 */
export type TextAreaProps = {
  id: string
  name: string
  label: string
  placeholder: string
  helpMessage: string
  errorMessage: string
}


/**
 * TextAreaSection component contains a Formik textarea field
 * along with label, helper text and error handling.
 * @param props
 * @constructor
 */
const TextAreaSection: React.FC<TextAreaProps> = (props) => {
  return <Field name={props.name} id={props.id}>
    {({
        field,
        form,
        meta,
      }: FieldProps) => (
    <div tw="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 pt-6">
      {meta.touched && meta.error ?
      <>
        <Label>{props.label}</Label>
        <div tw="sm:col-span-2 sm:mt-0">
          <ErrorTextArea
            rows={3}
            placeholder={props.placeholder}
            {...field}
          />
          <ErrorText>{meta.error}</ErrorText>
        </div>
      </>
      :
      <>
        <Label>{props.label}</Label>
        <div tw="sm:col-span-2 sm:mt-0">
          <TextArea placeholder={props.placeholder} {...field} />
          <HelpText>{props.helpMessage}</HelpText>
        </div>
      </>
      }
    </div>

    )}
  </Field>
}


/**
 * FileUploadProps type for FileUploadSection
 */
export type FileUploadProps = {
  id: string
  name: string
  label: string
  helpMessage: string
  errorMessage: string
}


/**
 * FileUploadSection component contains a Formik-compatible file upload input
 * along with label, helper text and error handling.
 * @param props
 * @constructor
 */
const FileUploadSection: React.FC<FileUploadProps> = (props) => {
  return <Field name={props.name} id={props.id}>
    {({
        field,
        form: { setFieldValue },
        meta,
      }: FieldProps) => (
    <div tw="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 pt-6">
      <Label>{props.label}</Label>
      <div tw="sm:col-span-2 sm:mt-0">
        <div tw="
        flex flex-col max-w-lg justify-center rounded-md
        border border-dashed border-gray-300 text-center space-y-1 p-4"
        >
          <IconWrapper size="md" color="light" icon={<ArrowUpTrayIcon />} />
          <Label tw="cursor-pointer">
            <span tw="text-primary-700">Upload a file</span>
            <input
              type="file"
              tw="sr-only"
              onChange={(event) => {
                // @ts-ignore
                const updated = field.value.concat(Object.values(event.currentTarget.files));
                setFieldValue(props.id, updated);
              }}
            />
            <span tw="text-sm text-gray-500"> or drag and drop</span>
          </Label>
          <HelpText>{props.helpMessage}</HelpText>
        </div>
        {field.value.length === 0 ?
          meta.touched && meta.error ? <ErrorText>{meta.error}</ErrorText>
          :
          <span>No files uploaded</span>
        :
          <Label tw="truncate max-w-lg">{field.value.map((file: File) => {return file.name}).join(", ")}</Label>
        }
      </div>
    </div>

    )}
  </Field>
}



// Styled components

const TextArea = tw.textarea`
  block w-full min-w-0 rounded-md shadow-sm
  text-gray-700 placeholder-gray-300 border-gray-300
  focus:border-primary-500 focus:ring-primary-500
  resize-none
`
const ErrorTextArea = tw.textarea`
  block w-full min-w-0 rounded-md border border-gray-300
  text-red-900 placeholder-red-300 focus:border-red-500 
  focus:outline-none focus:ring-red-500
  resize-none
 `
const Input = tw.input`
  block w-full min-w-0 rounded-lg shadow-sm border p-2
  text-gray-700 placeholder-gray-300 border-gray-300
  focus:border-primary-500 focus:ring-primary-500
`
const ErrorInput = tw.input`
  block w-full min-w-0 rounded-lg shadow-sm border p-2
  text-gray-700 placeholder-gray-300 border-gray-300
  focus:border-red-500 focus:ring-red-500
 `
const Label = tw.label`block text-sm font-medium text-gray-700`;
const HelpText = tw.p`text-sm text-gray-400 mt-2`;
const ErrorText = tw.p`text-sm text-red-700 mt-2`;


export { InputSection, TextAreaSection, FileUploadSection };