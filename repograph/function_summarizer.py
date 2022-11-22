from transformers import AutoTokenizer, T5ForConditionalGeneration

from repograph.models.nodes import Function


class FunctionSummarizer:
    """Summarise functions using CodeT5.

    Attributes:
        tokenizer: The function tokenizer.
        model: The specific CodeT5 that summarises tokenized functions.
    """
    tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large-ntp-py")
    model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large-ntp-py")

    @classmethod
    def create_docstring_node(cls, node: Function) -> str:
        """Generate a Docstring node.

        Uses generated function summarisation.

        Args:
            node (Function): The Function node to generate a Docstring node for.

        Returns:
            str
        """
        input_ids = cls.tokenizer(node.source_code, return_tensors="pt").input_ids
        generated_ids = cls.model.generate(input_ids, max_length=128)
        return cls.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
