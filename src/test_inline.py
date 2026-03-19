import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_italic_block(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        expected = [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_bold_block(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_multiple_bold_blocks(self):
        node = TextNode(
            "This is a **bold word1** and this is a **bold word2**", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        expected = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("bold word1", TextType.BOLD_TEXT),
            TextNode(" and this is a ", TextType.PLAIN_TEXT),
            TextNode("bold word2", TextType.BOLD_TEXT),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_no_matching_delimiter(self):
        node = TextNode("This is a broken **bold word", TextType.PLAIN_TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)


class TestSplitImageLinkDelimiter(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode(
                    "image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE_TEXT,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second link", TextType.LINK_TEXT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_all_syntax(self):
        markdown_text = """This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ]

        self.assertListEqual(text_to_textnodes(markdown_text), expected)

