export type Function = {
  name: string;
  type: string; // TODO: Enum
  builtin: boolean;
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

export type SearchResultSet = SearchResult[];
