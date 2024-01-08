import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

from loguru import logger
from pydantic import BaseModel, Field

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class SubTheme(BaseModel):
    name: str
    content: List[str] = Field(..., alias="Contenu")
    context: Optional[str] = Field(None, alias="Contexte")
    skills: Optional[List[str]] = Field(None, alias="Capacités attendues")
    demos: Optional[List[str]] = Field(None, alias="Démonstrations")
    algos: Optional[List[str]] = Field(None, alias="Exemples d'algorithmes")
    extensions: Optional[List[str]] = Field(None, alias="Approfondissements possibles")


class Theme(BaseModel):
    name: str = Field(..., alias="Nom")
    objective: str = Field(..., alias="Objectifs")
    subthemes: List[SubTheme]


def parse_json_to_pydantic(json_data: Dict) -> Theme:
    subthemes = []
    for name, details in json_data["Sous Thèmes"].items():
        subtheme_data = {"name": name, **details}
        subtheme = SubTheme.model_validate(subtheme_data)
        subthemes.append(subtheme)

    theme_data = {
        "Objectifs": json_data["Objectifs"],
        "Nom": json_data["Nom"],
        "subthemes": subthemes,
    }
    theme = Theme.model_validate(theme_data)
    return theme


def load_json_string(filepath: os.PathLike) -> Tuple[bool, str]:
    try:
        with open(filepath, "r") as file:
            json_str = file.read()
            logger.info(
                f"Successfully loaded string from file: {os.path.basename(filepath)}"
            )
            return True, json_str
    except FileNotFoundError as e:
        logger.error(e)
        return False, None


def clean_raw_string(text: str, old_char: str = "\u2019", new_char: str = "'") -> str:
    """
    Replaces specified characters in a JSON file.

    Args:
    text (str): Text to clean.
    old_char (str): Character to be replaced.
    new_char (str): Character to replace with.

    Returns:
    clean_text: Cleaned text.
    """
    cleaned_text = text.replace(old_char, new_char)
    logger.info(f"Replaced characters: '{old_char}' -> '{new_char}'")
    return cleaned_text


def load_dict_from_string(text: str) -> Union[bool, dict]:
    """
    Load a dictionary from a JSON string.

    Args:
        text (str): JSON string to load.

    Returns:
        Union[bool, dict]: True and the loaded dictionary if successful, False and None otherwise.
    """
    try:
        json_data = json.loads(text)
        logger.info("JSON loaded")
        return True, json_data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        return False, None


def _trim_trailing_spaces(text: str) -> str:
    """Remove trailing spaces from a string."""
    return text.strip()


def _remove_markdown_formatting(text: str) -> str:
    """Remove specific markdown formatting: list formatting and asterisks."""
    text = re.sub(r"\[\'(.*?)\'\]", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    return text


def _clean_json_keys(data: Union[Dict, List, str, Any]) -> Union[Dict, List, str, Any]:
    """Recursively clean the keys in a JSON object."""
    if isinstance(data, dict):
        return {
            _trim_trailing_spaces(_remove_markdown_formatting(k)): _clean_json_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_clean_json_keys(item) for item in data]
    else:
        return data


def _clean_json_values(
    data: Union[Dict, List, str, Any]
) -> Union[Dict, List, str, Any]:
    """Recursively clean the string values in a JSON object."""
    if isinstance(data, dict):
        return {k: _clean_json_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_clean_json_values(item) for item in data]
    elif isinstance(data, str):
        return _trim_trailing_spaces(_remove_markdown_formatting(data))
    else:
        return data


def clean_json_content(json_data: dict) -> dict:
    """Clean a JSON string with specific markdown formats."""
    cleaned_json = _clean_json_keys(json_data)
    cleaned_json = _clean_json_values(cleaned_json)
    logger.info("Cleaned keys and values")
    return cleaned_json


def _contains_odd_number_of_dollars(s: str) -> bool:
    """
    Check if a string contains an odd number of dollar signs.

    :param s: A string
    :return: True if the string contains an odd number of dollar signs, False otherwise
    """
    return s.count("$") % 2 != 0


def _count_latex_snippets(s: str) -> int:
    """
    Count the number of separate LaTeX snippets in a string.

    :param s: A string
    :return: Number of LaTeX snippets
    """
    # Split the string by dollar signs and count non-empty segments
    # as this would indicate a LaTeX snippet
    return sum(1 for segment in s.split("$") if segment.strip())


def _contains_latex(s: str) -> bool:
    """
    Check if a string contains LaTeX syntax enclosed within dollar signs.

    :param s: A string
    :return: True if the string contains LaTeX, False otherwise
    """
    return bool(re.search(r"\$.*?\$", s))


def get_latex_analysis(json_obj: dict) -> bool:
    analysis = _check_json_for_latex(json_obj)
    logger.info(f"Analyzed objects: {analysis['elements_analyzed']}")
    logger.info(f"Analyzed strings: {analysis['strings_analyzed']}")
    logger.info(f"Valid LaTeX snippets: {analysis['valid_latex_snippets']}")
    if analysis["potential_anomalies"] == 0:
        logger.info("No LaTeX anomalies detected")
        latex_is_clean = True
    else:
        logger.warning(f"Detected {analysis['potential_anomalies']} LaTeX anomalies")
        latex_is_clean = False
    return latex_is_clean


def _check_json_for_latex(json_obj, analysis=None) -> bool:
    """
    Analyze a JSON object for LaTeX syntax, counting the total elements,
    valid LaTeX strings, and potential anomalies (strings with odd number of dollar signs).

    :param json_obj: A JSON object (dict, list, string)
    :param analysis: A dict to store analysis results
    :return: Analysis results (dict)
    """
    if analysis is None:
        analysis = {
            "elements_analyzed": 0,
            "strings_analyzed": 0,
            "valid_latex_snippets": 0,
            "potential_anomalies": 0,
        }

    if isinstance(json_obj, dict):
        analysis["elements_analyzed"] += 1
        for value in json_obj.values():
            _check_json_for_latex(value, analysis)
    elif isinstance(json_obj, list):
        analysis["elements_analyzed"] += 1
        for item in json_obj:
            _check_json_for_latex(item, analysis)
    elif isinstance(json_obj, str):
        analysis["elements_analyzed"] += 1
        analysis["strings_analyzed"] += 1
        if _contains_latex(json_obj):
            analysis["valid_latex_snippets"] += _count_latex_snippets(json_obj)
        if _contains_odd_number_of_dollars(json_obj):
            analysis["potential_anomalies"] += 1

    return analysis


def validate_json_keys(json_dict) -> Tuple[bool, list]:
    required_top_level_keys = ["Nom", "Objectifs", "Sous Thèmes"]
    allowed_sous_theme_keys = [
        "Contenu",
        "Contexte",
        "Capacités attendues",
        "Démonstrations",
        "Exemples d'algorithmes",
        "Approfondissements possibles",
    ]
    foreign_keys = []

    try:
        # Check top-level keys
        for key in required_top_level_keys:
            if key not in json_dict:
                raise KeyError(f"Missing required key: {key}")

        # Validate "Sous Thèmes"
        for theme, details in json_dict["Sous Thèmes"].items():
            if not isinstance(details, dict):
                raise TypeError(f"Expected a dictionary for 'Sous Thème': {theme}")
            if "Contenu" not in details:
                raise KeyError(
                    f"Missing mandatory key 'Contenu' in 'Sous Thème': {theme}"
                )

            # Check for unexpected keys
            for key in details:
                if key not in allowed_sous_theme_keys:
                    logger.warning(f"Unexpected key '{key}' in 'Sous Thème': {theme}")
                    foreign_keys.append((theme, key))
        if foreign_keys:
            status = False
        else:
            status = True
        return status

    except Exception as e:
        logger.error(e)
        return False


def main():
    base_path = os.path.join(".", "courses", "seconde", "maths", "specs", "json")
    json_files = [f for f in os.listdir(base_path) if f.endswith(".json")]
    themes = []
    for json_file in json_files:
        json_file_path = os.path.join(base_path, json_file)
        status, json_str = load_json_string(json_file_path)
        if not status:
            continue

        # Load string as dict
        clean_json_str = clean_raw_string(json_str)
        status, json_data = load_dict_from_string(clean_json_str)
        if not status:
            continue

        # Clean keys and values
        json_data = clean_json_content(json_data)

        # Validate keys
        kay_status = validate_json_keys(json_data)
        if not kay_status:
            logger.error("Failed JSON key structure validation")
            continue
        logger.info("JSON structure is valid")

        # Validate LaTeX
        latex_status = get_latex_analysis(json_data)
        if not latex_status:
            logger.error("Failed LaTeX integrity validation")
            continue
        logger.info("LaTeX integrity is verified")

        # Save output

        with open(json_file_path, "w") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

        theme_object = parse_json_to_pydantic(json_data)
        themes.append(theme_object)
    print(len(themes))


if __name__ == "__main__":
    main()
