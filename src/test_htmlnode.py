import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        self.assertEqual(parent_node.to_html(), '<div><span class="child-span">child</span></div>')
    
    def test_to_html_with_props_everywhere(self):
        child_node = LeafNode("span", "child", props={"class": "child-span"})
        parent_node = ParentNode("div", [child_node], props={"class": "parent-div"})
        self.assertEqual(parent_node.to_html(), '<div class="parent-div"><span class="child-span">child</span></div>')
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child", props={"class": "child-span"})
        parent_node = ParentNode(None, [child_node], props={"class": "parent-div"})

        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None, props={"class": "parent-div"})

        with self.assertRaises(ValueError):
            parent_node.to_html()

    
         
 

       