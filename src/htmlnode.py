from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return (
            " "
            + " ".join(
                f'{attribute}="{value}"' for attribute, value in self.props.items()
            )
            if self.props
            else ""
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if not self.tag:
            return self.value

        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        html_output = []
        for child in self.children:
            html_output.append(child.to_html())

        parent_props = self.props_to_html()
        return f"<{self.tag}{parent_props}>{''.join(html_output)}</{self.tag}>"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(tag=None, value=text_node.text)  # type: ignore
        case TextType.BOLD_TEXT:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": text_node.url},  # type: ignore
            )
        case TextType.IMAGE_TEXT:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},  # type: ignore
            )
