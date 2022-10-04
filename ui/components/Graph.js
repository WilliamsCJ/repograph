import { ForceGraph2D } from 'react-force-graph';
import { withResizeDetector } from 'react-resize-detector';

const graph = {
  nodes: [
    {
      nodeRelSize: 2,
    },
    {
      nodeRelSize: 2,
    }
  ],
  links: []
}

function Graph({ width, height, targetRef }) {
  return (
    <div className="h-full w-full" ref={targetRef}>
      <ForceGraph2D
        graphData={graph}
        height={200}
        width={200}
        showNavInfo={true}
      />
    </div>
  )
}

const ResizableGraph = withResizeDetector(Graph);

export default Graph;