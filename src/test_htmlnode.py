import unittest

from htmlnode import HTMLNode, LeafNode

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
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_empty_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_left_empty_tag(self):
        node = LeafNode(None, "This is a node with an empty tag")

        self.assertEqual(node.to_html(), "This is a node with an empty tag")