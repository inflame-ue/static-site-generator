import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


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


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is a quote
> with **bolded** text inside
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bolded</b> text inside</blockquote></div>"
        )

        