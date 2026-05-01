import unittest
from shutil import ExecError

from markdown import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_with_title(self):
        markdown = """
# This is the title
Some other markdown text, some **bolded**, just for funsies
Ohhh
"""
        expected = "This is the title"
        self.assertEqual(expected, extract_title(markdown))

    def test_extract_title_no_title(self):
        markdown = "This is an invalid markdown string with *no title*!!"

        with self.assertRaises(Exception):
            extract_title(markdown)
