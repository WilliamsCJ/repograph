import React from 'react';

import tw from "twin.macro";

import { Card } from "../core/card";
import { CalendarIcon, ChevronRightIcon } from "@heroicons/react/24/outline";

const GraphList: React.FC = () => {
  return (
    <Card size={tw`shadow-sm h-24`}>
      <div tw="overflow-hidden w-full">
        <ul role="list" tw="divide-y divide-gray-200">

        </ul>
      </div>
    </Card>
  )
}

// const GraphListRow = () => {
//   return (
//     <li key={}>
//       <a href={} tw="block hover:bg-gray-50">
//         <div tw="flex items-center px-4 py-4 sm:px-6">
//           <div tw="ml-5 flex-shrink-0">
//             <div tw="min-w-0 flex-1 sm:flex sm:items-center sm:justify-between">
//               <div tw="truncate">
//                 <div tw="flex text-sm">
//                   <p className="truncate font-medium text-indigo-600">{position.title}</p>
//                   <p className="ml-1 flex-shrink-0 font-normal text-gray-500">in {position.department}</p>
//                 </div>
//                 <div className="mt-2 flex">
//                   <div className="flex items-center text-sm text-gray-500">
//                     <CalendarIcon className="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
//                     <p>
//                       Closing on <time dateTime={position.closeDate}>{position.closeDateFull}</time>
//                     </p>
//                   </div>
//                 </div>
//               </div>
//             </div>
//             <ChevronRightIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
//           </div>
//         </div>
//       </a>
//     </li>
//   )
// }

export default GraphList;