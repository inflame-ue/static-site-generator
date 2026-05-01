import os
import pathlib
import shutil
import sys

from page import generate_page


def copy_dir(source: str, destination: str) -> None:
    # we need to ensure that the copy is clean
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)

    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination)
        else:
            dest_file_path = os.path.join(destination, filename)
            os.makedirs(dest_file_path)
            copy_dir(file_path, dest_file_path)


def generate_pages(
    dir_path_content: str, template_path: str, dir_path_public: str, basepath: str
) -> None:
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        dest_file_path = os.path.join(dir_path_public, filename)
        if os.path.isfile(file_path) and os.path.split(file_path)[1].endswith(".md"):
            dest_file_path = pathlib.Path(dest_file_path).with_suffix(".html")
            generate_page(file_path, template_path, dest_file_path, basepath)  # type: ignore
        else:
            generate_pages(file_path, template_path, dest_file_path, basepath)


def main():
    basepath = "/"
    if len(sys.argv) > 2:
        basepath = sys.argv[1]

    

    copy_dir("static", "public")
    generate_pages("content/", "template.html", "public/")


if __name__ == "__main__":
    main()
