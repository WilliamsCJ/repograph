import React from "react";

import tw from "twin.macro";
import { Field, FieldProps } from "formik";
import IconWrapper from "./icon";
import {
  ArrowUpTrayIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";
import {
  Background,
  Border, BorderError,
  Focus,
  FocusError,
  Placeholder,
  PlaceholderError,
} from "./constants";
import { AccentText, BoldDetailText, DetailText } from "./text";

/**
 * InputProps type for InputSection component.
 */
export type InputProps = {
  id: string;
  name: string;
  label: string;
  placeholder: string;
  helpMessage: string;
  errorMessage: string;
};

/**
 * InputSection component contains a Formik input field
 * along with BoldDetailText, helper text and error handling.
 * @param props
 * @constructor
 */
const InputSection: React.FC<InputProps> = (props) => {
  return (
    <Field id={props.id} name={props.name}>
      {({ field, meta }: FieldProps) => (
        <div tw="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 pt-6">
          <BoldDetailText>{props.label}</BoldDetailText>
          <div tw="sm:col-span-2 sm:mt-0">
            <Input placeholder={props.placeholder} {...field} error={meta.touched && meta.error !== undefined} />
            {meta.touched && meta.error ?
              <ErrorText>{meta.error}</ErrorText>
            :
              <HelpText>{props.helpMessage}</HelpText>
            }
          </div>
        </div>
      )}
    </Field>
  );
};

/**
 * TextAreaProps type for TextAreaSection component.
 */
export type TextAreaProps = {
  id: string;
  name: string;
  label: string;
  placeholder: string;
  helpMessage: string;
  errorMessage: string;
};

/**
 * TextAreaSection component contains a Formik textarea field
 * along with BoldDetailText, helper text and error handling.
 * @param props
 * @constructor
 */
const TextAreaSection: React.FC<TextAreaProps> = (props) => {
  return (
    <Field name={props.name} id={props.id}>
      {({ field, form, meta }: FieldProps) => (
        <div tw="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 pt-6">
          <BoldDetailText>{props.label}</BoldDetailText>
          <div tw="sm:col-span-2 sm:mt-0">
            <TextArea placeholder={props.placeholder} {...field} rows={3} error={meta.touched && meta.error !== undefined} />
            {meta.touched && meta.error ?
              <ErrorText>{meta.error}</ErrorText>
            :
              <HelpText>{props.helpMessage}</HelpText>
            }
          </div>
        </div>
      )}
    </Field>
  );
};

/**
 * FileUploadProps type for FileUploadSection
 */
export type FileUploadProps = {
  id: string;
  name: string;
  label: string;
  helpMessage: string;
  errorMessage: string;
};

/**
 * FileUploadSection component contains a Formik-compatible file upload input
 * along with BoldDetailText, helper text and error handling.
 * @param props
 * @constructor
 */
const FileUploadSection: React.FC<FileUploadProps> = (props) => {
  return (
    <Field name={props.name} id={props.id}>
      {({ field, form: { setFieldValue }, meta }: FieldProps) => (
        <div tw="sm:grid sm:grid-cols-3 sm:items-start sm:gap-4 pt-6">
          <BoldDetailText as="label">{props.label}</BoldDetailText>
          <div tw="sm:col-span-2 sm:mt-0">
            <div
              css={[
                Border,
                tw`border-dashed text-center space-y-1 p-4`,
                tw`flex flex-col max-w-lg justify-center`,
                tw`dark:border-zinc-700`,
              ]}
            >
              <IconWrapper
                size="md"
                color="detail"
                icon={<ArrowUpTrayIcon />}
              />
              <label tw="cursor-pointer">
                <AccentText as="span">Upload a file</AccentText>
                <input
                  type="file"
                  tw="sr-only"
                  onChange={(event) => {
                    const updated = field.value.concat(
                      // @ts-ignore
                      Object.values(event.currentTarget.files)
                    );
                    setFieldValue(props.id, updated);
                  }}
                />
                <DetailText as="span"> or drag and drop</DetailText>
              </label>
              <HelpText>{props.helpMessage}</HelpText>
            </div>
            <div tw="mt-1">
              {field.value.length === 0 ? (
                meta.touched && meta.error ? (
                  <ErrorText>{meta.error}</ErrorText>
                ) : (
                  <BoldDetailText as="span">No files uploaded</BoldDetailText>
                )
              ) : (
                <BoldDetailText tw="truncate max-w-lg">
                  {field.value
                    .map((file: File) => {
                      return file.name;
                    })
                    .join(", ")}
                </BoldDetailText>
              )}
            </div>
          </div>
        </div>
      )}
    </Field>
  );
};

/**
 * SearchBarInputProps for SearchBarInput
 */
export type SearchBarInputSectionProps = {
  name: string;
  id: string;
  placeholder: string;
  label: string;
};

/**
 * SearchBarInput is used as the input section for a SearchBar form.
 * @param props {SearchBarInputSectionProps}
 * @constructor
 */
const SearchBarInputSection: React.FC<SearchBarInputSectionProps> = (props) => {
  return (
    <Field name={props.name} id={props.id}>
      {({ field, form: { setFieldValue }, meta }: FieldProps) => (
        <div tw="relative col-span-4 sm:col-span-5 md:col-span-7">
          <div tw="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
            <MagnifyingGlassIcon tw="h-6 w-6" />
          </div>
          <SearchBarInput required placeholder={props.placeholder} {...field} />
        </div>
      )}
    </Field>
  );
};

/**
 * TextArea component.
 */
const TextArea = (props: React.HTMLProps<HTMLTextAreaElement> & { error: boolean }) => (
  <textarea
    css={[
      tw`block w-full min-w-0 resize-none`,
      props.error ? BorderError : Border,
      Background,
      props.error ? FocusError : Focus,
      props.error ? PlaceholderError : Placeholder,
    ]}
    {...props}
  />
);

/**
 * Error version of TextArea component.
 */
const ErrorTextArea = (props: React.HTMLProps<HTMLTextAreaElement>) => (
  <textarea
    css={[
      tw`block w-full min-w-0 resize-none`,
      Border,
      Background,
      FocusError,
      PlaceholderError,
    ]}
    {...props}
  />
);

/**
 * Input component
 */
const Input = (props: React.HTMLProps<HTMLInputElement> & { error: boolean }) => (
  <input
    css={[
      tw`block w-full min-w-0 resize-none p-2`,
      props.error ? BorderError : Border,
      Background,
      props.error ? FocusError : Focus,
      props.error ? PlaceholderError : Placeholder,
    ]}
    {...props}
  />
);

/**
 * SearchBarInput component
 */
const SearchBarInput = (props: React.HTMLProps<HTMLInputElement>) => (
  <input
    css={[
      tw`block w-full px-4 py-2 pl-12`,
      Background,
      Border,
      Placeholder,
      Focus,
    ]}
    {...props}
  />
);

/**
 * Form help/hint text.
 */
const HelpText = tw.p`text-sm text-gray-400 mt-2`;

/**
 * Form error text.
 */
const ErrorText = tw.p`text-sm text-red-700 mt-2`;

export {
  InputSection,
  TextAreaSection,
  FileUploadSection,
  SearchBarInputSection,
};
