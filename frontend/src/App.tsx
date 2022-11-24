import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { HomeIcon, MagnifyingGlassIcon, ExclamationTriangleIcon, CloudArrowDownIcon } from "@heroicons/react/24/outline";

function App() {
  const [count, setCount] = useState(0)

  return (
    <body className="w-screen min-h-screen max-h-screen bg-gray-100">
      <div className="h-screen w-16 fixed inset-y-0 bg-white border-r-2 flex flex-col py-8 space-y-8">
        <div className="flex h-10">
          <HomeIcon className="h-6 w-6 m-auto"/>
        </div>
        <div className="flex  h-10">
          <MagnifyingGlassIcon className="h-6 w-6 m-auto"/>
        </div>
        <div className="flex h-10">
          <ExclamationTriangleIcon className="h-6 w-6 m-auto"/>
        </div>
      </div>
      <div className="w-full h-screen overscroll-contain overflow-y-auto flex flex-col space-y-20 pl-24 pr-8 py-8">
        <div className="w-full h-full">
          <div className="w-full flex flex-row justify-between bg-red-200">
            <h1 className="font-semibold text-3xl align-text-top">Your Repository</h1>
            <button
            type="button"
            className="h-10 flex flex-row space-x-2 items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
            <CloudArrowDownIcon className="h-5 w-5"/><span>Export</span>
            </button>
          </div>
        </div>
      </div>
    </body>
  )
}

export default App
