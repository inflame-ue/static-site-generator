from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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
