import unittest
from parameterized import parameterized
from repograph.entities.search.utils import remove_stop_words, clean_source_code


class TestSearchUtils(unittest.TestCase):
    @parameterized.expand(
        [
            [
                "This is a sample sentence, showing off the stop words filtration.",
                "This sample sentence showing stop words filtration",
            ],
            [
                "This sample sentence showing stop words filtration",
                "This sample sentence showing stop words filtration",
            ],
        ]
    )
    def test_remove_stop_words(self, original, target):
        output = remove_stop_words(original)
        self.assertEqual(output, target)

    @parameterized.expand(
        [
            [
                '''
            def square(n):
                """Takes in a number n, returns the square of n"""
                return n**2
            ''',
                "def square(n): return n**2",
            ],
        ]
    )
    def test_clean_source_code(self, original, target):
        output = clean_source_code(original)
        output = " ".join(output.split())
        self.assertEqual(output, target)
