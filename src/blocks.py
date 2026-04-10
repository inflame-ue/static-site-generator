from enum import Enum
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from inline import text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(handle_paragraph(block))
            case BlockType.HEADING:
                html_nodes.append(handle_heading(block))
            case BlockType.CODE:
                html_nodes.append(handle_code(block))
            case BlockType.QUOTE:
                html_nodes.append(handle_quote(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(handle_unordered_list(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(handle_ordered_list(block))

    return ParentNode("div", html_nodes)

def handle_paragraph(block: str) -> ParentNode:
    lines = block.split("\n")
    text = " ".join(lines)

    children = text_to_children(text)
    return ParentNode("p", children)  # type: ignore


def handle_heading(block: str) -> ParentNode:
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break

    text = block[heading_level:].lstrip()
    children = text_to_children(text)

    return ParentNode(f"h{heading_level}", children) # type: ignore


def handle_code(block: str) -> ParentNode:
    text = block[4:-3]
    child_html_node = text_node_to_html_node(TextNode(text, TextType.PLAIN_TEXT))

    return ParentNode("pre", [ParentNode("code", [child_html_node])]) # type: ignore


def handle_quote(block: str) -> ParentNode:
    text = " ".join(line[1:].lstrip() for line in block.split("\n"))
    children = text_to_children(text)

    return ParentNode("blockquote", children) # type: ignore


def handle_unordered_list(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []

    for line in lines:
        text = line[1:].lstrip()
        children = text_to_children(text)

        list_items.append(ParentNode("li", children)) # type: ignore

    return ParentNode("ul", list_items)


def handle_ordered_list(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []

    for line in lines:
        _, text = line.split(".", 1)
        text = text.lstrip()
        children = text_to_children(text)

        list_items.append(ParentNode("li", children)) # type: ignore
    
    return ParentNode("ol", list_items)


def text_to_children(text):
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]


def block_to_block_type(markdown_block: str) -> BlockType:
    heading_symbol_count = 0

    for char in markdown_block:
        if char == "#":
            heading_symbol_count += 1
        else:
            break

    if 1 <= heading_symbol_count <= 6 and markdown_block[
        heading_symbol_count:
    ].startswith(" "):
        return BlockType.HEADING

    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE

    unordered, ordered, quote = True, True, True
    for index, line in enumerate(markdown_block.split("\n")):
        if not line.startswith("- "):
            unordered = False
        if not line.startswith(f"{index + 1}. "):
            ordered = False
        if not line.startswith(">"):
            quote = False

    if quote:
        return BlockType.QUOTE

    if unordered:
        return BlockType.UNORDERED_LIST

    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [line.strip() for line in markdown.split("\n\n") if line.strip()]
