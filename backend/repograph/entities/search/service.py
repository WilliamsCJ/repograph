"""Function search.

The FunctionSummarizer class implements the CodeT5 model for function search.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
# Base imports
from logging import getLogger
from typing import Optional

# pip imports
from sentence_transformers import SentenceTransformer, util

# Model imports
from repograph.models.search import SemanticSearchResult, SemanticSearchResultSet

# Graph entity imports
from repograph.entities.graph.service import GraphService

# Utils imports
from repograph.entities.search.utils import remove_stop_words

# Setup logging
log = getLogger('repograph.entities.search.service')


class SearchService:
    graph: GraphService
    model: Optional[SentenceTransformer] = None

    def __init__(self, graph: GraphService):
        """Constructor

        Args:
        """
        self.graph = graph
        log.info("Initialising model...")
        self.model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')

    def find_similar_functions_by_query(
        self,
        query: str,
        offset: int,
        limit: int,
    ) -> SemanticSearchResultSet:
        """Finds similar functions using semantic search of function summarizations.

        Args:
            query (str): The semantic query.
            offset (int): Where to start when slicing the total set of results. For pagination.
            limit (int): The maximum number of results to return in the result set. For pagination.

        Return:
            SemanticSearchResultSet
        """
        query = remove_stop_words(query)
        query_embedding = self.model.encode(query)
        summarizations_map = self.graph.get_function_summarizations()
        summarizations_extended = list(
            [f"{v.canonical_name} k" for k, v in summarizations_map.items()]
        )
        summarizations = summarizations_map.keys()
        summarization_embeddings = self.model.encode(summarizations_extended)

        scores = util.dot_score(query_embedding, summarization_embeddings)[0].cpu().tolist()
        score_pairs = list(zip(summarizations, scores))
        score_pairs = sorted(score_pairs, key=lambda x: x[1], reverse=True)

        results = list(map(lambda x: SemanticSearchResult(
            function=summarizations_map[x[0]],
            summarization=x[0],
            score=x[1]
        ), score_pairs))[offset:offset+limit]

        return SemanticSearchResultSet(
            total=len(score_pairs),
            limit=limit,
            offset=offset,
            results=results
        )
