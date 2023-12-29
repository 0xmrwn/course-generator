import os

import yaml


def get_gen_team_prompt_kwargs(chapter_id: str, subchapter_id: str) -> dict:
    """
    Generate prompt keyword arguments for the course generation team based on chapter and subchapter IDs.

    Args:
        chapter_id (str): The ID of the chapter.
        subchapter_id (str): The ID of the subchapter.

    Returns:
        dict: The prompt keyword arguments containing chapter name, subchapter name, input scope, and input specs.
    """
    input_specs_md = _get_specs(subchapter_id)
    input_scope_md = _get_input_scope(chapter_id, subchapter_id)
    chapter_name, subchapter_name = _get_subchapter_identity(chapter_id, subchapter_id)
    prompt_kwargs = {
        "chapter_name": chapter_name,
        "subchapter_name": subchapter_name,
        "input_scope": input_scope_md,
        "input_specs": input_specs_md,
    }
    return prompt_kwargs


def save_raw_course(session_id: str, content: str) -> None:
    """
    Write content to a file.

    Args:
        session_id (str): The ID of the session.
        content (str): The content to write to the file.
    """
    filepath = os.path.join(
        ".", "courses", "seconde", "maths", "raw_courses", f"{session_id}.md"
    )
    with open(filepath, "w") as f:
        f.write(content)


def _get_specs(subchapter_id: str) -> str:
    """
    Retrieve the specifications for a given subchapter.

    Args:
        subchapter_id (str): The ID of the subchapter.

    Returns:
        str: The specifications for the specified subchapter.
    """
    with open(
        os.path.join(".", "courses", "seconde", "maths", "specs", f"{subchapter_id}.md")
    ) as file:
        specs = file.read()
    return specs


def _get_subchapter_identity(chapter_id: str, subchapter_id: str) -> tuple:
    """
    Retrieve the identity of a subchapter.

    Args:
        chapter_id (str): The ID of the chapter.
        subchapter_id (str): The ID of the subchapter.

    Returns:
        tuple: A tuple containing the chapter name and subchapter name.
    """
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


def _get_input_scope(chapter_id: str, subchapter_id: str) -> str:
    """
    Retrieve the input scope for a given chapter and subchapter.

    Args:
        chapter_id (str): The ID of the chapter.
        subchapter_id (str): The ID of the subchapter.

    Returns:
        str: The input scope markdown string.
    """
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
