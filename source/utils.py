import re
from collections import OrderedDict

import yaml


def parse_markdown(file_path):
    with open(file_path, "r") as file:
        content = file.readlines()

    main_topic_pattern = re.compile(r"^##\s+(.+)")  # Pattern for main topics
    subtopic_pattern = re.compile(r"^###\s+(.+)")  # Pattern for subtopics
    list_item_pattern = re.compile(r"^\d+\.\s+(.+)")  # Pattern for list items

    structure = OrderedDict()
    current_topic = None
    current_subtopic = None

    for line in content:
        main_topic_match = main_topic_pattern.match(line)
        subtopic_match = subtopic_pattern.match(line)
        list_item_match = list_item_pattern.match(line)

        if main_topic_match:
            current_topic = main_topic_match.group(1).strip()
            structure[current_topic] = OrderedDict()
        elif subtopic_match:
            current_subtopic = subtopic_match.group(1).strip()
            structure[current_topic][current_subtopic] = []
        elif list_item_match:
            item = list_item_match.group(1).strip()
            structure[current_topic][current_subtopic].append(item)

    return structure


def markdown_to_yaml(markdown_path, yaml_path):
    structure = parse_markdown(markdown_path)
    with open(yaml_path, "w") as file:
        yaml.dump(structure, file, allow_unicode=True)


def parse_md_to_yaml(md_content):
    lines = md_content.split("\n")
    result = []
    current_chapter = None
    current_section = None

    for line in lines:
        if line.startswith("## "):  # New chapter
            if current_chapter:
                result.append(current_chapter)
            current_chapter = {"name": line[3:], "sections": []}
        elif line.startswith("### "):  # New section
            if current_section:
                current_chapter["sections"].append(current_section)
            current_section = {"name": line[4:], "subsections": []}
        elif line.startswith("1. "):  # New subsection
            current_section["subsections"].append(line[3:])
        else:
            continue

    # Append the last section and chapter
    if current_section:
        current_chapter["sections"].append(current_section)
    if current_chapter:
        result.append(current_chapter)

    return result


with open("raw_courses/raw_structure.md", "r") as file:
    md_content = file.read()
parsed_data = parse_md_to_yaml(md_content)
with open("output.yaml", "w") as outfile:
    yaml.dump(parsed_data, outfile, default_flow_style=False)

# Example usage
# markdown_to_yaml("./raw_courses/raw_structure.md", "structure.yaml")
