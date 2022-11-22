"""Function summarization.

The FunctionSummarizer class implements the CodeT5 model for function summarization.

Typical usage:

    docstring_node = FunctionSummarizer.create_docstring_node(function_node)
"""
from transformers import AutoTokenizer, T5ForConditionalGeneration
from typing import Tuple

from repograph.models.nodes import Docstring, Function
from repograph.models.relationships import Documents


class FunctionSummarizer:
    """Summarise functions using CodeT5.

    Attributes:
        tokenizer: The function tokenizer.
        model: The specific CodeT5 that summarises tokenized functions.
    """
    tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large-ntp-py")
    model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large-ntp-py")

    @classmethod
    def create_docstring_node(cls, function: Function) -> Tuple[Docstring, Documents]:
        """Generate a Docstring node.

        Uses generated function summarization.

        Args:
            function (Function): The Function node to generate a Docstring node for.

        Returns:
            Tuple[Docstring, Relationship]: The new Docstring node and Documents
                                            relationship with Function node.
        """
        input_ids = cls.tokenizer(function.source_code, return_tensors="pt").input_ids
        generated_ids = cls.model.generate(input_ids, max_length=128)

        docstring = Docstring(
            summary=cls.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        )
        relationship = Documents(docstring, function)

        return docstring, relationship
