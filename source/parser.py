import os
import re
import sys
from collections import OrderedDict

import yaml
from loguru import logger

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    filter="my_module",
)


def represent_ordereddict(dumper, data):
    return dumper.represent_dict(data.items())


def represent_str(dumper, data):
    if ":" in data or any(c in data for c in "{}[],&*#?|-<>=!%@\\"):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(OrderedDict, represent_ordereddict)
yaml.add_representer(str, represent_str)


def parse_line(line):
    """
    Parses a single line of Markdown and returns its type and content.
    """
    if line.startswith("# "):
        return "main_topic", re.findall(r"^# (.+)$", line)[0]
    elif line.startswith("## "):
        return "chapter", re.findall(r"^## (.+)$", line)[0]
    elif line.startswith("### "):
        return "subchapter", re.findall(r"^### (.+)$", line)[0]
    elif re.match(r"^\d+\. ", line):
        return "content", re.findall(r"^\d+\. (.+)$", line)[0]
    elif line.strip() == "":
        return "empty", line  # Handling empty lines
    else:
        return "unknown", line


def build_yaml_structure(markdown_text):
    """
    Converts the Markdown text to a structured YAML format using OrderedDict.
    """
    yaml_structure = OrderedDict()
    current_chapter = None
    current_subchapter = None

    for line in markdown_text.splitlines():
        line_type, content = parse_line(line)

        if line_type == "main_topic":
            main_topic = content.lower().replace(" ", "_")
            yaml_structure[main_topic] = OrderedDict()
        elif line_type == "chapter":
            current_chapter, chapter_name = re.findall(r"^(.+?)\s*:\s*(.+)$", content)[
                0
            ]
            current_chapter = current_chapter.lower().replace(" ", "_")
            yaml_structure[main_topic][current_chapter] = {
                "chapter_name": chapter_name,
                "sub_chapters": OrderedDict(),
            }
        elif line_type == "subchapter":
            current_subchapter, subchapter_name = re.findall(
                r"^(.+?)\s*:\s*(.+)$", content
            )[0]
            subchapter_name = subchapter_name.replace("’", "'")
            current_subchapter = current_subchapter.lower().replace(" ", "_")
            yaml_structure[main_topic][current_chapter]["sub_chapters"][
                current_subchapter
            ] = OrderedDict([("name", subchapter_name), ("content", [])])
        elif line_type == "content":
            yaml_structure[main_topic][current_chapter]["sub_chapters"][
                current_subchapter
            ]["content"].append(content.replace("’", "'"))
        elif line_type == "empty":
            continue
        elif line_type == "unknown":
            logger.warning(f"Unknown line type encountered: {content}")

    return yaml_structure


def save_to_yaml(data, filename):
    """
    Saves the structured data to a YAML file with UTF-8 encoding.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            yaml.dump(data, file, allow_unicode=True)
        logger.info(f"YAML file saved successfully: {filename}")
    except Exception as e:
        logger.error(f"Error while saving YAML file: {e}")


if __name__ == "__main__":
    input_filepath = os.path.join(
        ".", "courses", "seconde", "maths", "structure", "raw_structure.md"
    )
    output_filepath = os.path.join(
        ".", "courses", "seconde", "maths", "structure", "structure.yaml"
    )
    with open(input_filepath, "r") as file:
        md_content = file.read()
    yaml_data = build_yaml_structure(md_content)
    save_to_yaml(yaml_data, output_filepath)
