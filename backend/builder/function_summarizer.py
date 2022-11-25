"""Function summarization.

The FunctionSummarizer class implements the CodeT5 model for function summarization.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
from logging import getLogger
from transformers import RobertaTokenizerFast, T5ForConditionalGeneration

from backend.repograph.models.nodes import Function


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

    def summarize_function(self, function: Function) -> str:
        """Summarize a function

        Args:
            function (Function): The function node to summarize.

        Returns:
            str: The summarization
        """
        log.debug(f'Create Docstring node for function `{function.name}`...')
        return self._summarize_code(function.source_code)

    def _summarize_code(self, source_code: str) -> str:
        """Summarize code.

        Args:
            source_code (str): The source code to summarize.

        Returns:
            str: The summarization.
        """
        log.debug("Tokenizing...")
        input_ids = self.tokenizer(source_code, return_tensors="pt").input_ids

        log.debug("Summarizing...")
        generated_ids = self.model.generate(input_ids, max_length=200)

        return self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
