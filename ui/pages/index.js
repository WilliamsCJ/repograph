// const ResizableGraph = dynamic(() => import('../components/Graph'), {
//   ssr: false,
// })

import Graph from "../components/Graph"

export default function Home() {
  return (
    <div className="h-screen w-screen">
      <Graph />
    </div>
  )
}
