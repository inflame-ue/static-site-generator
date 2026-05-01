def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        heading_level = 0
        for char in line:
            if char == "#":
                heading_level += 1
            else:
                break
        if heading_level == 1:
            return line.lstrip("#")

    raise Exception("No title found in the markdown document")
