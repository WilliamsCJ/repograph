import React from 'react';

// Styling
import tw from 'twin.macro';
import { Card } from "./card";
import { Divide } from "./constants";

export const Table = ({ children }: { children: JSX.Element[] | JSX.Element }) => (
  <Card size={tw`w-full rounded-lg`}>
    <table tw="table-fixed w-full rounded-lg overflow-hidden">
      {children}
    </table>
  </Card>
)

export const TableHeader= ({ children }: { children: JSX.Element[] | JSX.Element }) => (
  <thead tw="w-full rounded-t-lg">
    <tr tw="min-w-full rounded-t-lg bg-zinc-200/75 ">
      {children}
    </tr>
  </thead>
)

export const TableHeaderCell = ({ children }: { children: string }) => (
  <th scope="col" tw="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 grow">
    {children}
  </th>
)

export const TableBody = ({ children }: { children: JSX.Element[] | JSX.Element }) => (
  <tbody css={[Divide, tw`rounded-b-lg divide-y`]}>
  { children }
  </tbody>
)

export const TableRow = ({ children, key }: { children: JSX.Element[] | JSX.Element, key: number}) => (
  <tr key={key} tw="w-full text-clip">
    {children}
  </tr>
)

export const TableCell = ({ children }: { children: string }) => (
  <td tw="text-clip overflow-hidden px-3 py-4 text-sm text-gray-500 text-clip">
    {children}
  </td>
)