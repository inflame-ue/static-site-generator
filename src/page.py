import os

from blocks import markdown_to_html_node
from markdown import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    output = output.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as content_file:
        content_file.write(output)

