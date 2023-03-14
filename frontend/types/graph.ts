export type GraphSummary = {
  is_empty: boolean;
  nodes_total: number;
  relationships_total: number;
  repositories: number;
  classes: number;
  functions: number;
  modules: number;
  packages: number;
  readmes: number;
};

export type CallGraphFunction = {
  id: number;
  name: string;
  canonical_name: string;
  type: string;
};

export type CallGraphRelationship = {
  from: number;
  to: number;
  type: string;
};

export type CallGraph = {
  nodes: CallGraphFunction[];
  edges: CallGraphRelationship[];
};

enum GraphListingStatus {
  PENDING = "PENDING",
  CREATED = "CREATED",
}

export type GraphListing = {
  neo4j_name: string;
  name: string;
  description: string;
  created: string;
  status: GraphListingStatus;
};

export type GraphInfo = {
  summary: GraphSummary;
  graph: CallGraph;
};

export interface IssuesResult {
  columns: string[]
  data: any[]
}

export type CircularDependency = {
  files: string;
  length: number;
}

export type CircularDependencyResult = {
  columns: string[]
  data: CircularDependency[]
}