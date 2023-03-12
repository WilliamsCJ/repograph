"""Function search.

The FunctionSummarizer class implements the CodeT5 model for function search.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
# Base imports
from logging import getLogger
from typing import Optional, Tuple, List

# pip imports
from sentence_transformers import SentenceTransformer, util

# Model imports
from repograph.entities.search.models import (
    AvailableSearchQuery,
    SemanticSearchResult,
    SemanticSearchResultSet,
    SearchQueryResult,
)

# Graph entity imports
from repograph.entities.graph.service import GraphService

# Utils imports
from repograph.entities.search.utils import remove_stop_words

# Setup logging
log = getLogger("repograph.entities.search.service")


class SearchService:
    graph: GraphService
    model: Optional[SentenceTransformer] = None

    def __init__(self, graph: GraphService, active: bool = True):
        """Constructor

        Args:
        """
        self.graph = graph
        log.info("Initialising model...")
        if active:
            self.model = SentenceTransformer(
                "sentence-transformers/multi-qa-distilbert-cos-v1"
            )

    def find_similar_functions_by_query(
        self,
        graph: str,
        query: str,
        offset: int,
        limit: int,
    ) -> SemanticSearchResultSet:
        """Finds similar functions using semantic search of function summarizations.

        Args:
            graph (str): The graph name.
            query (str): The semantic query.
            offset (int): Where to start when slicing the total set of results. For pagination.
            limit (int): The maximum number of results to return in the result set. For pagination.

        Return:
            SemanticSearchResultSet
        """
        query = remove_stop_words(query)
        query_embedding = self.model.encode(query)
        summarizations_map = self.graph.get_function_summarizations(graph)
        summarizations_extended = list(
            [f"{v.canonical_name} k" for k, v in summarizations_map.items()]
        )
        summarizations = summarizations_map.keys()

        summarization_embeddings = self.model.encode(summarizations_extended)

        scores = (
            util.dot_score(query_embedding, summarization_embeddings)[0].cpu().tolist()
        )
        score_pairs = list(zip(summarizations, scores))
        score_pairs = sorted(score_pairs, key=lambda x: x[1], reverse=True)

        results = list(
            map(
                lambda x: SemanticSearchResult(
                    function=summarizations_map[x[0]], summarization=x[0], score=x[1]
                ),
                score_pairs,
            )
        )[offset : offset + limit]

        return SemanticSearchResultSet(
            total=len(score_pairs), limit=limit, offset=offset, results=results
        )

    def find_possible_incorrect_docstrings(self, graph: str) -> Tuple[int, int]:
        """Find the number of possibly incorrect docstrings.

        Cosine similarity between docstring and generated summarization is less than 0.5

        Args:
            graph (str): The graph name.

        Returns:
            int: The number of low scores
            int: The number of functions that were missing docstrings to compare against
        """
        docstrings = self.graph.get_docstrings(graph)
        docstrings_with_summarizations = list(
            filter(lambda x: x.summarization is not None, docstrings)
        )
        total = len(docstrings_with_summarizations)

        docstrings_with_original = list(
            filter(
                lambda x: x.short_description is not None
                or x.long_description is not None,
                docstrings_with_summarizations,
            )
        )
        missing_docstring = total - len(docstrings_with_original)

        pairs = list(
            map(
                lambda x: (
                    x.summarization,
                    str(x.short_description or "") + str(x.long_description or ""),
                ),
                docstrings_with_original,
            )
        )
        low_scores = 0

        for summarization, docstring in pairs:
            embedding_1 = self.model.encode(summarization)
            embedding_2 = self.model.encode([docstring, ""])
            score = util.dot_score(embedding_1, embedding_2)[0].cpu().tolist()[0]

            if score < 0.5:
                low_scores += 1

        return low_scores, missing_docstring

    def get_available_search_queries(self) -> List[AvailableSearchQuery]:
        available = [
            AvailableSearchQuery(
                id=0,
                name="Search repository requirements",
                function=self.search_requirements,
            ),
            AvailableSearchQuery(
                id=1, name="Search README files", function=self.search_readmes
            ),
            AvailableSearchQuery(
                id=2,
                name="Search license files and types",
                function=self.search_licenses,
            ),
            AvailableSearchQuery(
                id=3, name="Search file names", function=self.search_files
            ),
            AvailableSearchQuery(
                id=4,
                name="Search extracted docstrings",
                function=self.search_docstrings,
            ),
            AvailableSearchQuery(
                id=5,
                name="Search function summarizations",
                function=self.search_summarizations,
            ),
            AvailableSearchQuery(
                id=6,
                name="Search function and classes",
                function=self.search_functions_and_classes,
            ),
        ]
        return available

    def search_requirements(
        self, graph_name: str, repository: Optional[str] = None
    ) -> SearchQueryResult:
        """Construct the results for the requirements query.

        Args:
            graph_name (str): The graph to search.
            repository (str, optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_requirements(graph_name, repository=repository)

        return SearchQueryResult(
            columns=["Repository", "Dependency", "Specifications"],
            data=results,
            size=len(results),
        )

    def search_readmes(self, graph_name: str, repository: Optional[str] = None):
        """Construct the results for the READMEs query.

        Args:
            graph_name (str): The graph to search.
            repository (str, Optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_readme_files(graph_name, repository=repository)

        return SearchQueryResult(
            columns=["Repository", "File", "Contents"], data=results, size=len(results)
        )

    def search_licenses(self, graph_name: str, repository: Optional[str] = None):
        """Construct the results for the licenses query.

        Args:
            graph_name (str): The graph to search.
            repository (str, Optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_licenses(graph_name, repository=repository)

        return SearchQueryResult(
            columns=["Repository", "License", "Confidence", "Content"],
            data=results,
            size=len(results),
        )

    def search_docstrings(self, graph_name: str, repository: Optional[str] = None):
        """Construct the results for the docstrings query.

        Args:
            graph_name (str): The graph to search.
            repository (str, Optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_docstrings_full(graph_name, repository=repository)

        return SearchQueryResult(
            columns=["Repository", "Function", "Docstring Summary", "Docstring Body"],
            data=results,
            size=len(results),
        )

    def search_summarizations(self, graph_name: str, repository: Optional[str] = None):
        """Construct the results for the summarizations query.

        Args:
            graph_name (str): The graph to search.
            repository (str, Optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_summarizations(graph_name, repository=repository)

        return SearchQueryResult(
            columns=["Repository", "Function", "Summarization"],
            data=results,
            size=len(results),
        )

    def search_files(self, graph_name: str, repository: Optional[str] = None):
        """Construct the results for the files query.

        Args:
            graph_name (str): The graph to search.
            repository (str, Optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_files(graph_name, repository=repository)

        return SearchQueryResult(
            columns=["Filename", "Repository"], data=results, size=len(results)
        )

    def search_functions_and_classes(
        self, graph_name: str, repository: Optional[str] = None
    ):
        """Construct the results for the functions and classes query.

        Args:
            graph_name (str): The graph to search.
            repository (str, Optional): Repository to filter by.

        Returns:
            SearchQueryResult
        """
        results = self.graph.get_functions_and_classes(
            graph_name, repository=repository
        )

        return SearchQueryResult(
            columns=["Repository", "Name", "Type"], data=results, size=len(results)
        )
