from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax, the number of delimiters is not balanced.")
        
        for index, section in enumerate(old_node.text.split(delimiter)):
            if section == "":
                continue

            if index % 2 == 0:
                new_nodes.append(TextNode(section, TextType.PLAIN_TEXT)) 
                continue

            new_nodes.append(TextNode(section, text_type))
    
    return new_nodes


node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
print(new_nodes)
        


