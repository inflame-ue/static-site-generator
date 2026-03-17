class HTMLNode:

    def __init__(self, tag: str = None, value: str = None, children: list['HTMLNode'] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return " " + " ".join(f'{attribute}="{value}"' for attribute, value in self.props.items()) if self.props else ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, props)


