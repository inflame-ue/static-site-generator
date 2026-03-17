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
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        
        if not self.tag:
            return self.value

        props_string = self.props_to_html()
        return f"<{self.tag}{props_string if props_string else ''}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    


