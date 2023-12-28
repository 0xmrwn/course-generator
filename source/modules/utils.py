import json
import os

import yaml


def get_specs(subchapter_id: str) -> str:
    with open(
        os.path.join(".", "courses", "seconde", "maths", "specs", f"{subchapter_id}.md")
    ) as file:
        specs = file.read()
    return specs


def get_subchapter_identity(chapter_id: str, subchapter_id: str) -> tuple:
    chapter_id = chapter_id.lower()
    subchapter_id = subchapter_id.lower()
    with open(
        os.path.join(".", "courses", "seconde", "maths", "structure", "structure.yaml")
    ) as file:
        structure = yaml.safe_load(file)
    chapter_name = structure["maths_seconde_2019"][chapter_id]["chapter_name"]
    subchapter_name = structure["maths_seconde_2019"][chapter_id]["sub_chapters"][
        subchapter_id
    ]["name"]
    return (chapter_name, subchapter_name)


def get_spec_json(subchapter_id: str) -> dict:
    with open(
        os.path.join(
            ".",
            "courses",
            "seconde",
            "maths",
            "specs",
            f"{subchapter_id}_objectives.json",
        )
    ) as file:
        specs = json.load(file)
    return specs


def get_input_scope(chapter_id: str, subchapter_id: str) -> str:
    chapter_id = chapter_id.lower()
    subchapter_id = subchapter_id.lower()
    with open(
        os.path.join(".", "courses", "seconde", "maths", "structure", "structure.yaml")
    ) as file:
        structure = yaml.safe_load(file)
    chapter_name = structure["maths_seconde_2019"][chapter_id]["chapter_name"]
    subchapter = structure["maths_seconde_2019"][chapter_id]["sub_chapters"][
        subchapter_id
    ]

    # Start with the chapter name
    markdown_string = f"# Chapitre: {chapter_name}\n"
    markdown_string += f"## Sous-chapitre: {subchapter['name']}"

    # Iterate over subchapter items
    for item in subchapter["content"]:
        markdown_string += f"### {item}\n"

    return markdown_string
