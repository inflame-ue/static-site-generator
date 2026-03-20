import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_valid_heading_block(self):
        md = "### Valid H3 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(md))
    
    def test_invalid_heading_block(self):
        md = "###Invalid H3 Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))
    
    def test_valid_code_block(self):
        md = """```\ncode here```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(md))
    
    def test_invalid_code_block(self):
        md = """
``
code here
```
"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

    def test_valid_quote(self):
        md = "> This is a quote\n>The quote is continuing"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(md))
    
    def test_invalid_quote(self):
        md = "> This is a quote\nThis is not a quote"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))
    
    def test_valid_unordered_list(self):
        md = "- Item 1\n- Item 2"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(md))
    
    def test_invalid_unordered_list(self):
        md = "-Item 1\n- Item 2"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))
    
    def test_valid_ordered_list(self):
        md = "1. Item 1\n2. Item 2"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(md))

    def test_invalid_ordered_list(self):
        md = "1.Item 1\n2. Item 2"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))




        