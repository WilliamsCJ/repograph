import React, { Fragment, useState } from "react";

import tw from "twin.macro";
import { Field, FieldProps } from "formik";
import IconWrapper, { SearchBarIcon } from "./icon";
import {
  ArrowUpTrayIcon,
  CheckIcon,
  ChevronUpDownIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";
import {
  Background,
  Border,
  BorderError,
  Divide,
  Focus,
  FocusError,
  Placeholder,
  PlaceholderError,
} from "./constants";
import { AccentText, BoldDetailText, DetailText } from "./text";
import { Combobox, Listbox } from "@headlessui/react";
import { Relative } from "./layout";
import { AvailableSearchQuery } from "../../types/search";
import { useTheme } from "next-themes";

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
            <Input
              placeholder={props.placeholder}
              {...field}
              error={meta.touched && meta.error !== undefined}
            />
            {meta.touched && meta.error ? (
              <ErrorText>{meta.error}</ErrorText>
            ) : (
              <HelpText>{props.helpMessage}</HelpText>
            )}
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
            <TextArea
              placeholder={props.placeholder}
              {...field}
              rows={3}
              error={meta.touched && meta.error !== undefined}
            />
            {meta.touched && meta.error ? (
              <ErrorText>{meta.error}</ErrorText>
            ) : (
              <HelpText>{props.helpMessage}</HelpText>
            )}
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
        <div tw="relative grow col-span-4 sm:col-span-5 md:col-span-7">
          <Relative>
            <SearchBarIcon />
            <SearchBarInput
              required
              placeholder={props.placeholder}
              {...field}
            />
          </Relative>
        </div>
      )}
    </Field>
  );
};

export interface ComboOption {
  id: number;
  name: string;
}

export type ComboSearchBarInputSectionProps = {
  name: string;
  id: string;
  placeholder: string;
  label: string;
  options: ComboOption[];
};

/**
 *
 * @param props
 * @constructor
 */
const ComboSearchBarInputSection: React.FC<ComboSearchBarInputSectionProps> = (
  props
) => {
  const [query, setQuery] = useState("");

  // Filter the queries
  // Modified from:
  // https://headlessui.com/react/combobox
  const filteredQueries =
    query === ""
      ? props.options
      : props.options.filter((option: ComboOption) => {
          return option.name.toLowerCase().includes(query.toLowerCase());
        });

  return (
    <Field name={props.name} id={props.id}>
      {({ field, form: { setFieldValue }, meta }: FieldProps) => (
        <div
          css={[
            tw`relative w-full grow transform divide-y overflow-hidden transition-all`,
            Border,
            Background,
            Divide,
            Focus,
          ]}
        >
          <Combobox
            value={field.value}
            onChange={(e) => setFieldValue(field.name, e, false)}
          >
            <Relative>
              <SearchBarIcon />
              <ComboSearchBarInput
                placeholder={props.placeholder}
                displayValue={(query: AvailableSearchQuery) =>
                  query ? query.name : null
                }
                // @ts-ignore
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                  setQuery(event.target.value);
                }}
              />
            </Relative>

            <Combobox.Options tw="scroll-py-2 overflow-y-auto">
              {filteredQueries.length === 0 && query !== "" ? (
                <div tw="relative py-2 pl-11 pr-4">
                  <BoldDetailText>No matching queries.</BoldDetailText>
                </div>
              ) : (
                filteredQueries.map((query: AvailableSearchQuery) => (
                  <Combobox.Option key={query.id} value={query}>
                    {/* @ts-ignore */}
                    {({ active, selected }) => (
                      <Option
                        label={query.name}
                        active={active}
                        selected={selected}
                        leftAlign
                      />
                    )}
                  </Combobox.Option>
                ))
              )}
            </Combobox.Options>
          </Combobox>
        </div>
      )}
    </Field>
  );
};

export type SelectSectionProps = {
  name: string;
  id: string;
  placeholder: string;
  label: string;
  options: string[];
  setRepository: any;
};

const SelectInputSection: React.FC<SelectSectionProps> = (props) => {
  return (
    <Field name={props.name} id={props.id}>
      {({ field, form: { setFieldValue }, meta }: FieldProps) => (
        <div
          css={[
            tw`relative w-96 transform divide-y overflow-hidden transition-all text-left`,
            Border,
            Background,
            Divide,
            Focus,
          ]}
        >
          <Listbox
            value={field.value}
            onChange={(e) => {
              setFieldValue(field.name, e, false);
              props.setRepository(e);
            }}
          >
            <Listbox.Button
              css={[
                tw`relative py-2 px-4 w-full bg-transparent border-0 focus:ring-0 text-left`,
                Placeholder,
              ]}
            >
              <span>{field.value ? field.value : "All"}</span>
              <span tw="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                <ChevronUpDownIcon
                  tw="h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
              </span>
            </Listbox.Button>
            <Listbox.Options>
              <Listbox.Option key={0} value={null}>
                {/* @ts-ignore */}
                {({ active, selected }) => (
                  <Option label={"All"} active={active} selected={selected} />
                )}
              </Listbox.Option>
              {props.options.map((option: string, index: number) => (
                <Listbox.Option key={index + 1} value={option}>
                  {/* @ts-ignore */}
                  {({ active, selected }) => (
                    <Option
                      label={option}
                      active={active}
                      selected={selected}
                    />
                  )}
                </Listbox.Option>
              ))}
            </Listbox.Options>
          </Listbox>
        </div>
      )}
    </Field>
  );
};

/**
 * TextArea component.
 */
const TextArea = (
  props: React.HTMLProps<HTMLTextAreaElement> & { error: boolean }
) => (
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
const Input = (
  props: React.HTMLProps<HTMLInputElement> & { error: boolean }
) => (
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
      tw`py-2 w-full bg-transparent border-0 pl-11 pr-4 focus:ring-0`,
      Background,
      Border,
      Placeholder,
      Focus,
    ]}
    {...props}
  />
);

/**
 * ComboSearchBar input component
 * @param placeholder
 * @param onChange
 * @param displayValue
 * @constructor
 */
const ComboSearchBarInput = ({
  placeholder,
  onChange,
  displayValue,
}: {
  placeholder: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  displayValue: any;
}) => (
  <Combobox.Input
    css={[
      tw`py-2 w-full bg-transparent border-0 pl-11 pr-4 focus:ring-0`,
      Placeholder,
    ]}
    displayValue={displayValue}
    placeholder={placeholder}
    // @ts-ignore
    onChange={onChange}
  />
);

const Option = ({
  active,
  selected,
  label,
  leftAlign,
}: {
  active: boolean;
  selected: boolean;
  label: string;
  leftAlign?: boolean;
}) => {
  const { theme } = useTheme();

  let bg;
  if (active) {
    bg = tw`bg-accent-400/25`;
  } else {
    bg = tw`bg-white dark:bg-zinc-800/50`;
  }

  return (
    <div
      css={[
        tw`cursor-pointer relative py-2 px-4`,
        leftAlign && tw`pl-11 pr-4`,
        bg,
      ]}
    >
      {selected && (
        <CheckIcon
          css={[
            tw`pointer-events-none absolute top-2 right-2 h-5 w-5 text-zinc-700`,
            active && tw`text-accent-800`,
          ]}
          aria-hidden="true"
        />
      )}
      {selected ? (
        <BoldDetailText>{label}</BoldDetailText>
      ) : (
        <DetailText>{label}</DetailText>
      )}
    </div>
  );
};

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
  ComboSearchBarInputSection,
  SelectInputSection,
};
