"""
Code search utilities.
"""
# Base imports
import re

# pip imports
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk initialisation
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)


def clean_source_code(source_code: str) -> str:
    """Remove docstrings from source_code

    Args:
        source_code (str): The source code to clean.

    Returns:
        str: Cleaned source_code
    """
    return re.sub('(?s)""".*"""\n', "", source_code)


def remove_stop_words(sentence: str) -> str:
    """Remove stop words from a sentence

    Args:
        sentence (str): Unprocessed sentence.

    Returns:
        str: Cleaned sentence
    """
    tokens = word_tokenize(sentence)
    filtered_words = [
        word
        for word in tokens
        if (word.isalpha() and word not in set(stopwords.words("english")))
    ]
    return " ".join(filtered_words)
