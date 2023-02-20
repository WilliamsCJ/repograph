export type Function = {
  id: number;
  name: string;
  type: string; // TODO: Enum
  builtin: boolean;
  repository_name: string;
  canonical_name?: string;
  source_code?: string;
  min_line_number?: number;
  max_line_number?: number;
};

export type SearchResult = {
  repository?: string;
  function: Function;
  summarization: string;
  score: number;
};

export type SearchResultSet = {
  results: SearchResult[];
  offset: number;
  limit: number;
  total: number;
};
