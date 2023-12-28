import json
import os

import yaml


def get_specs(subchapter_id: str) -> str:
    subchapter_id = subchapter_id.lower()
    with open(
        os.path.join(".", "courses", "seconde", "maths", "specs", f"{subchapter_id}.md")
    ) as file:
        specs = file.read()
    return specs


def get_subchapter(chapter_id: str, subchapter_id: str) -> tuple:
    subchapter_id = subchapter_id.lower()
    chapter_id = chapter_id.lower()
    with open(
        os.path.join(".", "courses", "seconde", "maths", "structure", "structure.yaml")
    ) as file:
        structure = yaml.safe_load(file)
    chapter_name = structure["maths_seconde_2019"][chapter_id]["chapter_name"]
    subchapter_name = structure["maths_seconde_2019"][chapter_id]["sub_chapters"][
        subchapter_id
    ]["name"]
    subchapter_content = structure["maths_seconde_2019"][chapter_id]["sub_chapters"][
        subchapter_id
    ]["name"]
    return (chapter_name, subchapter_name, subchapter_content)


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


def count_files(dir: str):
    directory = os.path.join(".", "courses", "seconde", "maths", dir)
    file_count = len(
        [
            name
            for name in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, name))
        ]
    )
    return file_count


def get_latest_raw_response(subchapter_id: str) -> str:
    latest_version = count_files("raw_courses") - 1
    with open(
        os.path.join(
            ".",
            "courses",
            "seconde",
            "maths",
            "raw_courses",
            f"{subchapter_id}_response_{latest_version}.md",
        )
    ) as file:
        specs = file.read()
    return specs


def save_markdown_output(directory: str, version: str, content: str):
    with open(
        os.path.join(
            ".", "courses", "seconde", "maths", directory, f"c1s1_response_{version}.md"
        ),
        "w",
    ) as file:
        file.write(content)


if __name__ == "__main__":
    pass
