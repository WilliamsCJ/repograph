"""Function search.

The FunctionSummarizer class implements the CodeT5 model for function search.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
# Base imports
from logging import getLogger
from typing import List, Optional

# pip imports
from sentence_transformers import SentenceTransformer, util

# Model imports
from repograph.models.search import SemanticSearchResult

# Graph entity imports
from repograph.entities.graph.service import GraphService

# Utils imports


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

    def find_similar_functions_by_query(self, query: str) -> List[SemanticSearchResult]:
        """Finds similar functions using semantic search of function summarizations.

        Args:
            query (str): The semantic query.

        Return:
            List[SemanticSearchResult]: Top 5

        """
        query_embedding = self.model.encode(query)
        summarizations_map = self.graph.get_function_summarizations()
        summarizations = list(summarizations_map.keys())
        summarization_embeddings = self.model.encode(summarizations)

        scores = util.dot_score(query_embedding, summarization_embeddings)[0].cpu().tolist()
        score_pairs = list(zip(summarizations, scores))
        score_pairs = sorted(score_pairs, key=lambda x: x[1], reverse=True)

        return list(map(lambda x: SemanticSearchResult(
            function=summarizations_map[x[0]],
            summarization=x[0],
            score=x[1]
        ), score_pairs))[:5]
