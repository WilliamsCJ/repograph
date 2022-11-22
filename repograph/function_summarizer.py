"""Function summarization.

The FunctionSummarizer class implements the CodeT5 model for function summarization.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
from logging import getLogger
from transformers import RobertaTokenizerFast, T5ForConditionalGeneration
from typing import Tuple

from repograph.models.nodes import Docstring, Function
from repograph.models.relationships import Documents


log = getLogger('repograph.function_summarizer')


class FunctionSummarizer:
    """Summarise functions using CodeT5.

    Attributes:
        tokenizer: The function tokenizer.
        model: The specific CodeT5 that summarises tokenized functions.
    """
    tokenizer: any
    model: any

    def __init__(self):
        log.info("Initialising CodeT5 model...")
        self.tokenizer = RobertaTokenizerFast.from_pretrained("Salesforce/codet5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base-multi-sum")
        log.info("Ready!")

    def create_docstring_node(self, function: Function) -> Tuple[Docstring, Documents]:
        """Generate a Docstring node.

        Uses generated function summarization.

        Args:
            function (Function): The Function node to generate a Docstring node for.

        Returns:
            Tuple[Docstring, Relationship]: The new Docstring node and Documents
                                            relationship with Function node.
        """
        log.debug(f'Create Docstring node for function `{function.name}`...')

        log.debug("Tokenizing...")
        input_ids = self.tokenizer(function.source_code, return_tensors="pt").input_ids

        log.debug("Summarizing...")
        generated_ids = self.model.generate(input_ids, max_length=200)

        log.debug("Creating Node/Relationship and returning!")
        docstring = Docstring(
            summary=self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        )
        relationship = Documents(docstring, function)

        return docstring, relationship
