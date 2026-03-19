import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(
                "Invalid markdown syntax, the number of delimiters is not balanced."
            )

        for index, section in enumerate(old_node.text.split(delimiter)):
            if section == "":
                continue

            if index % 2 == 0:
                new_nodes.append(TextNode(section, TextType.PLAIN_TEXT))
                continue

            new_nodes.append(TextNode(section, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        original_text = old_node.text
        images_information = extract_markdown_images(original_text)

        if not images_information:
            new_nodes.append(old_node)
            continue

        for image_information in images_information:
            image_alt, image_link = image_information
            before_section, after_section = original_text.split(
                f"![{image_alt}]({image_link})"
            )

            if before_section:
                new_nodes.append(TextNode(before_section, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE_TEXT, url=image_link))

            original_text = after_section

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for old_node in old_nodes:
        original_text = old_node.text
        links_information = extract_markdown_links(original_text)

        if not links_information:
            new_nodes.append(old_node)
            continue

        for link_information in links_information:
            link_alt, links_link = link_information
            before_section, after_section = original_text.split(
                f"[{link_alt}]({links_link})"
            )

            if before_section:
                new_nodes.append(TextNode(before_section, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK_TEXT, url=links_link))

            original_text = after_section

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))

    return new_nodes


def extract_markdown_images(text) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
