import unittest

from htmlnode import HTMLNode

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
