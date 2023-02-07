export type GraphSummary = {
  is_empty: boolean;
  nodes_total: number;
  relationships_total: number;
  repositories: number;
  classes: number;
  functions: number;
  modules: number;
  packages: number;
};

export type CallGraphFunction = {
  id: number;
  label: string;
  title: string;
};

export type CallGraphRelationship = {
  from: number;
  to: number;
};

export type CallGraph = {
  nodes: CallGraphFunction[];
  edges: CallGraphRelationship[];
};
