from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = 'plain'
    BOLD_TEXT = 'bold'
    ITALIC_TEXT = 'italic'
    CODE_TEXT = 'code'
    LINK_TEXT = 'link'
    IMAGE_TEXT = 'image'


class TextNode:

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: 'TextNode'):
        is_text_eq = self.text == other.text
        is_text_type_eq = self.text_type == other.text_type
        is_url_eq = self.url == other.url

        return all((is_text_eq, is_text_type_eq, is_url_eq))
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'



        


