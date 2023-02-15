"""Function summarization.

The FunctionSummarizer class implements the CodeT5 model for function summarization.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
# Base imports
from logging import getLogger

# pip imports
import torch
from transformers import RobertaTokenizerFast, T5ForConditionalGeneration

# Model imports
from repograph.models.nodes import Function

# Utils imports
from repograph.entities.summarization.utils import clean_source_code


# Setup logging
log = getLogger('repograph.entities.summarization.service')


class SummarizationService:
    tokenizer: any = None
    model: any = None
    active: bool

    def __init__(self, summarize: bool = False):
        """Constructor

        Args:
            summarize (bool): Whether to initialise model and tokenizer.
        """
        self.active = summarize
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"


        if summarize:
            log.info("Initialising CodeT5 model...")
            self.tokenizer = RobertaTokenizerFast.from_pretrained("Salesforce/codet5-base")
            self.model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base-multi-sum")  # noqa: 501
            self.model = self.model.to(self.device)
            log.info("Ready!")
        else:
            log.info("Summarization flag not set. Skipping setup.")

    def summarize_function(self, function: Function) -> str:
        """Summarize a function.

        Args:
            function (Function): The function node to summarization.

        Returns:
            str: The summarization
        """
        if not self.model or not self.tokenizer:
            log.warning("No model or tokenizer initialised!")
            return ""

        log.debug(f'Create Docstring node for function `{function.name}`...')
        source_code = clean_source_code(function.source_code)
        return self._summarize_code(source_code)

    def _summarize_code(self, source_code: str) -> str:
        """Summarize code.

        Args:
            source_code (str): The source code to summarization.

        Returns:
            str: The summarization.
        """
        log.debug("Tokenizing...")
        input_ids = self.tokenizer(source_code, return_tensors="pt").to(self.device).input_ids

        log.debug("Summarizing...")
        generated_ids = self.model.generate(input_ids, max_length=200)

        return self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
