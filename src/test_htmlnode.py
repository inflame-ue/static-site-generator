import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        html_node = HTMLNode(props=props)

        expected = ' href="https://www.google.com" target="_blank"'
        actual = html_node.props_to_html()

        self.assertEqual(expected, actual)

    def test_empty_props_to_html(self):
        props = {}
        html_node = HTMLNode(props=props)

        expected = ""
        actual = html_node.props_to_html()

        self.assertEqual(expected, actual)

    def test_none_props_to_html(self):
        html_node = HTMLNode()

        expected = ""
        actual = html_node.props_to_html()

        self.assertEqual(expected, actual)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_empty_value(self):
        node = LeafNode("p", None)  # type: ignore

        with self.assertRaises(ValueError):
            node.to_html()

    def test_left_empty_tag(self):
        node = LeafNode(None, "This is a node with an empty tag")  # type: ignore

        self.assertEqual(node.to_html(), "This is a node with an empty tag")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_children_props(self):
        child_node = LeafNode("span", "child", props={"class": "child-span"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), '<div><span class="child-span">child</span></div>'
        )

    def test_to_html_with_props_everywhere(self):
        child_node = LeafNode("span", "child", props={"class": "child-span"})
        parent_node = ParentNode("div", [child_node], props={"class": "parent-div"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent-div"><span class="child-span">child</span></div>',
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child", props={"class": "child-span"})
        parent_node = ParentNode(None, [child_node], props={"class": "parent-div"})  # type: ignore

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None, props={"class": "parent-div"})  # type: ignore

        with self.assertRaises(ValueError):
            parent_node.to_html()


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, node.text)

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, node.text)

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, node.text)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, node.text)

    def test_link(self):
        node = TextNode(
            "This is a link node", TextType.LINK_TEXT, url="https://example.com"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props, {"href": node.url})

    def test_image(self):
        node = TextNode(
            "This is an image node", TextType.IMAGE_TEXT, url="https://example.com"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})

    def test_uknown(self):
        node = TextNode("This is a dummy node", "some text here")  # type: ignore

        with self.assertRaises(Exception):
            text_node_to_html_node(node)
