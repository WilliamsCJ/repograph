"""Function search.

The FunctionSummarizer class implements the CodeT5 model for function search.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
# Base imports
from logging import getLogger
from typing import Optional

# pip imports
from sentence_transformers import SentenceTransformer

# Model imports
from repograph.models.nodes import Function

# Graph entity imports
from repograph.entities.graph.service import GraphService

# Utils imports


# Setup logging
log = getLogger('repograph.entities.search.service')


class SearchService:
    graph: GraphService
    model: Optional[SentenceTransformer] = None

    def __init__(self, graph: GraphService, active: bool = False):
        """Constructor

        Args:
        """
        self.graph = graph

        if active:
            log.info("Initialising model...")
            self.model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')

    def find_similar_functions_by_query(self, query: str) -> any:
        self.model.encode(query)

    def test(self):
        self.graph.repository.get_all_nodes(label='Function', type=Function)
